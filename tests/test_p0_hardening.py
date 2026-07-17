from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from orchestrator.article_patch import (
    ArticlePatchError,
    apply_article_patches,
    parse_article_patch_review,
)
from orchestrator.gate_reader import read_mip_recommendation
from orchestrator.prompt_source import PromptSource
from orchestrator.storage import CaseStore


CASE_VALUES = {
    "title": "P0 Case",
    "description": "Description",
    "source_status": "constructed",
    "intended_use": "test",
}


class PromptHardeningTests(unittest.TestCase):
    def test_all_yaml_generation_prompts_require_plain_single_yaml_fence(self) -> None:
        source = PromptSource(Path(__file__).resolve().parents[1] / "resources" / "Prompts and Instructions.md")
        yaml_steps = (2, 4, 6, 9, 11, 14, 16, 18, 20, 22, 24, 26)
        for step_id in yaml_steps:
            prompt = source.get(step_id)
            self.assertIn("FIELD-SPECIFIC VALUE RULE:", prompt, step_id)
            self.assertIn("Return exactly one plain fenced `yaml` code block.", prompt, step_id)
            self.assertIn("do not add an ID, title, attributes, or metadata", prompt, step_id)
            self.assertNotIn("if the chat interface requires separation", prompt, step_id)

    def test_mip_review_prompt_names_each_decision_field_without_new_route(self) -> None:
        source = PromptSource(Path(__file__).resolve().parents[1] / "resources" / "Prompts and Instructions.md")
        prompt = source.get(12)
        self.assertIn("mip_recommendation_output.recommendation_status", prompt)
        self.assertIn("MIP_source_read_recommendation.status", prompt)
        self.assertIn("MIP_case_application_recommendation.status", prompt)
        self.assertIn("does not create a separate runner route", prompt)

    def test_mip_generation_prompt_preserves_binary_runner_route(self) -> None:
        source = PromptSource(Path(__file__).resolve().parents[1] / "resources" / "Prompts and Instructions.md")
        prompt = source.get(11)
        self.assertIn("Runner routing remains binary", prompt)
        self.assertIn("No source-reading-only route is created", prompt)


class MipRoutingContractTests(unittest.TestCase):
    @staticmethod
    def _complete_through_step_12(session) -> None:
        for step_id in range(1, 8):
            session.write_output(step_id, f"output {step_id}", complete=True)
        session.set_route({"route_type": "core_only", "selected_addon": None, "selection_basis": "manual_user_route"})
        session.write_output(11, "mip gate", complete=True)
        session.write_output(12, "mip gate checked", complete=True)

    def test_overall_recommended_with_limits_preselects_mip_branch(self) -> None:
        text = """
mip_recommendation_output:
  recommendation_status: recommended_with_limits
  MIP_source_read_recommendation:
    status: recommended
  MIP_case_application_recommendation:
    status: possible_after_reading_MIP_source_yaml
"""
        recommendation = read_mip_recommendation(text)
        self.assertEqual(recommendation.value, "MIP")
        self.assertEqual(recommendation.key_path, "mip_recommendation_output.recommendation_status")

    def test_no_mip_still_skips_all_mip_and_ahp_steps(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "gate_recommended_no_mip"})
            self.assertEqual(session.current_step_id(), 20)
            for step_id in range(13, 20):
                self.assertEqual(session.step_state(step_id)["status"], "skipped")

    def test_use_mip_opens_source_read_and_then_application(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12(session)
            session.set_mip_route({"route_type": "use_mip", "selection_basis": "gate_recommended"})
            self.assertEqual(session.current_step_id(), 13)
            session.write_output(13, "source read", complete=True)
            self.assertEqual(session.current_step_id(), 14)
            self.assertEqual(session.step_state(14)["status"], "current")


class ArticlePatchHardeningTests(unittest.TestCase):
    REVIEW = """### Final check status

article_ready_after_minor_patch

### Main issues

- one issue

### Exact patches

**Patch 1 — Tighten sentence**

Find:

Old sentence.

Replace with:

New sentence.

**Patch 2 — Add boundary**

Insert after:

Anchor paragraph.

Insert:

Boundary paragraph.
"""

    def test_no_patch_status_parses_without_executable_patch(self) -> None:
        review = parse_article_patch_review(
            "### Final check status\n\narticle_ready_with_no_patch_required\n\n"
            "### Main issues\n\nnone\n\n### Exact patches\n\nnone\n"
        )
        self.assertEqual(review.status, "article_ready_with_no_patch_required")
        self.assertEqual(review.patches, ())

    def test_parse_and_apply_exact_patches(self) -> None:
        review = parse_article_patch_review(self.REVIEW)
        self.assertEqual(len(review.patches), 2)
        article = "Old sentence.\n\nAnchor paragraph.\n"
        patched = apply_article_patches(article, review.patches)
        self.assertEqual(patched, "New sentence.\n\nAnchor paragraph.\n\nBoundary paragraph.\n")

    def test_patch_application_rejects_zero_or_multiple_matches(self) -> None:
        review = parse_article_patch_review(self.REVIEW)
        with self.assertRaises(ArticlePatchError):
            apply_article_patches("Anchor paragraph.", review.patches)
        with self.assertRaises(ArticlePatchError):
            apply_article_patches("Old sentence. Old sentence.\n\nAnchor paragraph.", review.patches)

    def test_storage_archives_original_and_applies_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            article_path = session.output_path(30)
            article_path.parent.mkdir(parents=True, exist_ok=True)
            article_path.write_text("Old sentence.\n\nAnchor paragraph.\n", encoding="utf-8")
            archive = session.apply_final_article_patches(self.REVIEW)
            self.assertTrue((archive / article_path.name).is_file())
            self.assertEqual(
                article_path.read_text(encoding="utf-8"),
                "New sentence.\n\nAnchor paragraph.\n\nBoundary paragraph.\n",
            )
            state = session.step_state(30)
            self.assertEqual(state["article_patch_status"], "patches_applied")
            self.assertEqual(state["article_patch_count"], 2)


if __name__ == "__main__":
    unittest.main()
