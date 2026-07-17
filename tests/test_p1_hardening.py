from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.article_patch import (
    parse_article_patch_review,
    render_article_patch_diff,
)
from orchestrator.dialogs import build_binary_layer_route_result
from orchestrator.gate_reader import read_first_mip_gate_details, read_mip_gate_details
from orchestrator.storage import CaseStore, StorageError


CASE_VALUES = {
    "title": "Golden Full Run",
    "description": "Constructed benchmark case.",
    "source_status": "constructed illustrative scenario",
    "intended_use": "regression test",
}


MIP_GATE = """mip_recommendation_output:
  recommendation_status: recommended_with_limits
  MIP_source_read_recommendation:
    status: recommended
  MIP_case_application_recommendation:
    status: possible_after_reading_MIP_source_yaml
"""


PATCH_REVIEW = """### Final check status

article_ready_after_minor_patch

### Main issues

- Tighten one sentence.

### Exact patches

**Patch 1 — Tighten sentence**

Find:

Old sentence.

Replace with:

New sentence.
"""


class MipGatePresentationTests(unittest.TestCase):
    def test_all_mip_gate_decisions_are_read_and_saved_without_new_route(self) -> None:
        details = read_mip_gate_details(MIP_GATE, source_step=12)
        self.assertEqual(details.overall.value, "MIP")
        self.assertEqual(details.source_read.value, "recommended")
        self.assertEqual(details.case_application.value, "possible_after_reading_MIP_source_yaml")

        route = build_binary_layer_route_result(
            layer_name="MIP",
            recommendation=details.overall,
            route_type="use_mip",
            use_route="use_mip",
            no_route="no_mip",
            extra_recommendations={
                "source_read_recommendation": details.source_read,
                "case_application_recommendation": details.case_application,
            },
        )
        self.assertEqual(route["route_type"], "use_mip")
        self.assertEqual(route["selection_basis"], "gate_recommended")
        gate = route["gate_recommendation"]
        self.assertEqual(gate["source_read_recommendation"]["value"], "recommended")
        self.assertEqual(
            gate["case_application_recommendation"]["value"],
            "possible_after_reading_MIP_source_yaml",
        )

    def test_checked_ready_sentence_falls_back_to_mip_gate_yaml(self) -> None:
        details = read_first_mip_gate_details(((12, "MIP Gate YAML checked. Ready."), (11, MIP_GATE)))
        self.assertEqual(details.overall.value, "MIP")
        self.assertEqual(details.overall.source_step, 11)
        self.assertEqual(details.source_read.value, "recommended")


class ArticlePatchPreviewAndLogTests(unittest.TestCase):
    def test_unified_diff_preview_matches_atomic_patch_result(self) -> None:
        review = parse_article_patch_review(PATCH_REVIEW)
        patched, diff = render_article_patch_diff("Old sentence.\n", review.patches)
        self.assertEqual(patched, "New sentence.\n")
        self.assertIn("--- step_30_final_article.md", diff)
        self.assertIn("+++ step_30_final_article.patched.md", diff)
        self.assertIn("-Old sentence.", diff)
        self.assertIn("+New sentence.", diff)

    def test_declined_patch_is_written_to_internal_patch_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            session.output_path(30).parent.mkdir(parents=True, exist_ok=True)
            session.output_path(30).write_text("Old sentence.\n", encoding="utf-8")
            session.record_final_article_patch_decision(
                "patches_proposed_not_applied",
                1,
                review_text=PATCH_REVIEW,
            )
            log_path = session.case_dir / session.step_state(30)["article_patch_log"]
            log = json.loads(log_path.read_text(encoding="utf-8"))
            entry = log["entries"][-1]
            self.assertEqual(entry["status"], "patches_proposed_not_applied")
            self.assertEqual(entry["patch_count"], 1)
            self.assertEqual(entry["patches"][0]["title"], "Tighten sentence")
            self.assertEqual(entry["before_sha256"], entry["after_sha256"])

    def test_patch_application_rolls_back_when_patch_log_cannot_be_updated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            article_path = session.output_path(30)
            article_path.parent.mkdir(parents=True, exist_ok=True)
            article_path.write_text("Old sentence.\n", encoding="utf-8")
            log_path = session.case_dir / "history" / "article_patches" / "patch_log.json"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text('{"entries": "invalid"}', encoding="utf-8")

            with self.assertRaises(StorageError):
                session.apply_final_article_patches(PATCH_REVIEW)
            self.assertEqual(article_path.read_text(encoding="utf-8"), "Old sentence.\n")


class GoldenFullRunRegressionTests(unittest.TestCase):
    def test_full_checked_route_reaches_patched_article_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)

            for step_id in range(1, 8):
                session.write_output(step_id, f"checked output {step_id}", complete=True)

            session.set_route({
                "route_type": "selected_addon",
                "selected_addon": "EDEN",
                "selection_basis": "gate_recommended",
            })
            for step_id in range(8, 11):
                session.write_output(step_id, f"checked output {step_id}", complete=True)

            session.write_output(11, MIP_GATE, complete=True)
            session.write_output(12, MIP_GATE, complete=True)
            details = read_mip_gate_details(MIP_GATE, source_step=12)
            session.set_mip_route(build_binary_layer_route_result(
                layer_name="MIP",
                recommendation=details.overall,
                route_type="use_mip",
                use_route="use_mip",
                no_route="no_mip",
                extra_recommendations={
                    "source_read_recommendation": details.source_read,
                    "case_application_recommendation": details.case_application,
                },
            ))
            for step_id in range(13, 16):
                session.write_output(step_id, f"checked output {step_id}", complete=True)

            session.write_output(16, "AHP gate", complete=True)
            session.write_output(17, "AHP gate checked", complete=True)
            session.set_ahp_route({
                "route_type": "use_ahp",
                "selection_basis": "gate_recommended",
            })
            for step_id in range(18, 20):
                session.write_output(step_id, f"checked output {step_id}", complete=True)

            for step_id in range(20, 27):
                session.write_output(step_id, f"checked output {step_id}", complete=True)

            session.set_article_route({
                "route_type": "generate_article",
                "article_profile": "full_analysis_article",
            })
            session.write_output(27, "contract established", complete=True)
            session.write_output(28, "## Golden Full Run\n\nOld sentence.\n", complete=True)
            session.write_output(
                29,
                "### Example decision\n\nexamples_not_needed\n\n### Reason\n\nReadable.\n\n"
                "### Generated example\n\nnone\n",
                complete=True,
            )

            self.assertEqual(session.current_step_id(), 31)
            self.assertEqual(session.step_state(30)["status"], "completed_by_runner_no_examples")
            self.assertEqual(session.load_output(30), "## Golden Full Run\n\nOld sentence.\n")

            session.write_output(31, PATCH_REVIEW, complete=False)
            archive = session.apply_final_article_patches(PATCH_REVIEW)
            session.complete_step(31)

            self.assertEqual(session.session_data["run_status"], "pipeline_complete_with_article")
            self.assertIsNone(session.current_step_id())
            self.assertEqual(session.load_output(30), "## Golden Full Run\n\nNew sentence.\n")
            self.assertTrue((archive / session.output_path(30).name).is_file())
            self.assertEqual(session.session_data["route"]["selected_addon"], "EDEN")
            self.assertEqual(session.session_data["mip_route"]["route_type"], "use_mip")
            self.assertEqual(session.session_data["ahp_route"]["route_type"], "use_ahp")
            self.assertEqual(session.session_data["article_route"]["article_profile"], "full_analysis_article")
            self.assertEqual(session.step_state(30)["article_patch_status"], "patches_applied")
            self.assertTrue((session.case_dir / session.step_state(30)["article_patch_log"]).is_file())


if __name__ == "__main__":
    unittest.main()
