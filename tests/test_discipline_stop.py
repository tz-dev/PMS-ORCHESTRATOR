from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.gate_reader import read_pre_analysis_disposition
from orchestrator.prompt_source import PromptSource
from orchestrator.storage import CaseStore


BASE_VALUES = {
    "title": "Discipline stop test",
    "description": "Test case",
    "source_status": "synthetic",
    "intended_use": "test",
}

STOP_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: stop
  hard_gate_status: triggered
  hard_gate_effect: stop_pipeline
"""

PROCEED_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: allow_with_limits
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: not_triggered
  hard_gate_effect: limit_requested_output
"""

FINAL_PIPELINE_STOP_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: triggered
  hard_gate_effect: refuse_requested_output
final_pre_analysis_status:
  pipeline_case_disposition: stop
  status: usable_for_core_on_permitted_target
  next_allowed_step: core_case_application_on_permitted_target
"""

FINAL_STATUS_STOP_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: triggered
  hard_gate_effect: refuse_requested_output
final_pre_analysis_status:
  pipeline_case_disposition: proceed_reframed
  status: stop_before_core
  next_allowed_step: core_case_application_on_permitted_target
"""

FINAL_NEXT_STEP_STOP_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: triggered
  hard_gate_effect: refuse_requested_output
final_pre_analysis_status:
  pipeline_case_disposition: proceed_reframed
  status: usable_for_core_on_permitted_target
  next_allowed_step: stop
"""

THREE_FINAL_STOPS_YAML = """scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: triggered
  hard_gate_effect: refuse_requested_output
final_pre_analysis_status:
  requested_output_disposition: refuse
  pipeline_case_disposition: stop
  status: stop_before_core
  reason: A prohibited person-level verdict is requested from insufficient material.
  next_allowed_step: stop
"""

MANDATORY_PERSON_NEAR_STOP_YAML = """input_status_discipline:
  input_strength: minimal
scope_boundary_matrix:
  whole_person_claim: not_allowed
  motive_claim: not_allowed
scope_and_pipeline_disposition:
  requested_output_disposition: refuse
  pipeline_case_disposition: proceed_reframed
  hard_gate_status: triggered
  hard_gate_effect: refuse_requested_output
pms_entry_condition_precheck:
  requested_output_entry_condition_status: not_satisfied
person_nearness_publicness_irreversibility:
  person_nearness_level: severe
  irreversibility_level: high
"""


class DisciplineStopContractTests(unittest.TestCase):
    def test_packaged_template_and_prompts_define_binding_stop(self) -> None:
        root = Path(__file__).resolve().parents[1]
        template = (root / "templates" / "pms_discipline_pre_analysis_template.yaml").read_text(encoding="utf-8")
        prompts = PromptSource(root / "resources" / "Prompts and Instructions.md")

        self.assertIn('pipeline_case_disposition: "<proceed | proceed_reframed | suspend | stop | unclear>"', template)
        self.assertIn("stop_before_core", template)
        self.assertIn('next_allowed_step: "<core_case_application | core_case_application_on_permitted_target | revise_pre_analysis | suspend | refuse | redirect | stop | unclear>"', template)
        self.assertIn("binding PMS-DISCIPLINE pipeline stop", prompts.get(2))
        self.assertIn("MANDATORY PERSON-NEAR STOP RULE", prompts.get(2))
        self.assertIn("must be corrected to `pipeline_case_disposition: stop`", prompts.get(3))
        self.assertIn("PMS-DISCIPLINE pipeline stop confirmed", prompts.get(3))

class PreAnalysisDispositionReaderTests(unittest.TestCase):
    def test_reads_authoritative_pipeline_stop(self) -> None:
        result = read_pre_analysis_disposition(STOP_YAML, source_step=2)
        self.assertTrue(result.is_pipeline_stop)
        self.assertTrue(result.explicit_pipeline_stop)
        self.assertEqual(result.stop_reason, "pipeline_case_disposition_stop")
        self.assertEqual(result.pipeline_case_disposition.key_path, "scope_and_pipeline_disposition.pipeline_case_disposition")
        self.assertEqual(result.requested_output_disposition.value, "refuse")
        self.assertEqual(result.hard_gate_effect.value, "stop_pipeline")

    def test_enforces_mandatory_person_near_stop_cross_field_rule(self) -> None:
        result = read_pre_analysis_disposition(MANDATORY_PERSON_NEAR_STOP_YAML, source_step=2)
        self.assertTrue(result.is_pipeline_stop)
        self.assertFalse(result.explicit_pipeline_stop)
        self.assertTrue(result.mandatory_person_near_stop)
        self.assertEqual(result.stop_reason, "mandatory_person_near_hard_stop")
        self.assertEqual(result.pipeline_case_disposition.value, "proceed_reframed")

    def test_each_authoritative_stop_path_overrides_proceed(self) -> None:
        cases = (
            (STOP_YAML, "scope_and_pipeline_disposition.pipeline_case_disposition", "stop"),
            (FINAL_PIPELINE_STOP_YAML, "final_pre_analysis_status.pipeline_case_disposition", "stop"),
            (FINAL_STATUS_STOP_YAML, "final_pre_analysis_status.status", "stop_before_core"),
            (FINAL_NEXT_STEP_STOP_YAML, "final_pre_analysis_status.next_allowed_step", "stop"),
        )
        for yaml_text, expected_path, expected_value in cases:
            with self.subTest(expected_path=expected_path):
                result = read_pre_analysis_disposition(yaml_text, source_step=2)
                self.assertTrue(result.is_pipeline_stop)
                self.assertTrue(result.explicit_pipeline_stop)
                self.assertIsNotNone(result.explicit_stop_signal)
                self.assertEqual(result.explicit_stop_signal.key_path, expected_path)
                self.assertEqual(result.explicit_stop_signal.value, expected_value)

    def test_three_final_stop_signals_are_detected(self) -> None:
        result = read_pre_analysis_disposition(THREE_FINAL_STOPS_YAML, source_step=2)
        self.assertTrue(result.is_pipeline_stop)
        self.assertEqual(
            result.explicit_stop_signal.key_path,
            "final_pre_analysis_status.pipeline_case_disposition",
        )


class DisciplineStopFlowTests(unittest.TestCase):
    def _project(self, root: Path) -> None:
        (root / "templates").mkdir(parents=True, exist_ok=True)
        (root / "templates" / "pms_discipline_pre_analysis_template.yaml").write_text(
            STOP_YAML,
            encoding="utf-8",
        )
        (root / "yaml_validation_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": "TEST",
                    "steps": {
                        "2": {
                            "reference": "templates/pms_discipline_pre_analysis_template.yaml",
                            "compare_keys": True,
                            "allow_extra_keys": False,
                            "extract_placeholder_enums": False,
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    def test_full_review_waits_for_step_3_then_stops_from_step_2(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)

            self.assertEqual(session.current_step_id(), 3)
            self.assertEqual(session.session_data["run_status"], "active")
            warning = session.pending_discipline_stop_warning
            self.assertIsNotNone(warning)
            self.assertEqual(warning["status"], "pending_semantic_review")
            self.assertEqual(warning["source_step"], 2)
            self.assertEqual(
                warning["key_path"],
                "scope_and_pipeline_disposition.pipeline_case_disposition",
            )
            self.assertEqual(warning["detected_value"], "stop")

            session.write_output(3, "Pre-Analysis YAML checked. PMS-DISCIPLINE pipeline stop confirmed.", complete=True)

            self.assertIsNone(session.current_step_id())
            self.assertEqual(session.session_data["run_status"], "pipeline_stopped_by_pre_analysis")
            self.assertEqual(session.discipline_stop["source_step"], 2)
            self.assertEqual(session.discipline_stop["revision_step"], 3)
            self.assertEqual(session.discipline_stop["key_path"], "scope_and_pipeline_disposition.pipeline_case_disposition")
            self.assertEqual(len(session.discipline_stop["source_output_sha256"]), 64)
            for step_id in range(4, 32):
                self.assertEqual(session.step_state(step_id)["status"], "locked")

    def test_full_review_without_stop_has_no_pending_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, PROCEED_YAML, complete=True)

            self.assertEqual(session.current_step_id(), 3)
            self.assertEqual(session.session_data["run_status"], "active")
            self.assertIsNone(session.pending_discipline_stop_warning)

    def test_full_review_mandatory_cross_field_stop_creates_pending_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, MANDATORY_PERSON_NEAR_STOP_YAML, complete=True)

            warning = session.pending_discipline_stop_warning
            self.assertIsNotNone(warning)
            self.assertEqual(warning["reason"], "mandatory_person_near_hard_stop")
            self.assertEqual(
                warning["key_path"],
                "cross_field_policy.mandatory_person_near_stop",
            )
            self.assertEqual(warning["detected_value"], "triggered")
            self.assertEqual(session.current_step_id(), 3)

    def test_full_review_corrected_yaml_can_remove_stop(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)
            session.write_output(3, f"CHECK STATUS: corrected\n```yaml\n{PROCEED_YAML}```", complete=True)

            self.assertEqual(session.current_step_id(), 4)
            self.assertEqual(session.session_data["run_status"], "active")
            self.assertIsNone(session.discipline_stop)
            self.assertIsNone(session.pending_discipline_stop_warning)

    def test_incomplete_corrected_yaml_cannot_clear_existing_stop(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)
            incomplete = "scope_and_pipeline_disposition:\n  requested_output_disposition: allow\n"
            session.write_output(3, f"CHECK STATUS: corrected\n```yaml\n{incomplete}```", complete=True)

            self.assertEqual(session.session_data["run_status"], "pipeline_stopped_by_pre_analysis")
            self.assertEqual(session.discipline_stop["source_step"], 2)

    def test_fast_mode_stops_immediately_after_step_2(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case({**BASE_VALUES, "ai_review_steps_enabled": False})
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)

            self.assertIsNone(session.current_step_id())
            self.assertEqual(session.session_data["run_status"], "pipeline_stopped_by_pre_analysis")
            self.assertEqual(session.discipline_stop["source_step"], 2)
            self.assertEqual(session.discipline_stop["revision_step"], 2)
            self.assertEqual(session.step_state(3)["status"], "skipped")
            self.assertEqual(session.step_state(4)["status"], "locked")


    def test_fast_mode_enforces_mandatory_person_near_stop_despite_proceed_reframed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case({**BASE_VALUES, "ai_review_steps_enabled": False})
            session.write_output(1, "read", complete=True)
            session.write_output(2, MANDATORY_PERSON_NEAR_STOP_YAML, complete=True)

            self.assertIsNone(session.current_step_id())
            self.assertEqual(session.session_data["run_status"], "pipeline_stopped_by_pre_analysis")
            self.assertEqual(session.discipline_stop["reason"], "mandatory_person_near_hard_stop")
            self.assertEqual(session.discipline_stop["key_path"], "cross_field_policy.mandatory_person_near_stop")
            self.assertEqual(session.discipline_stop["declared_pipeline_case_disposition"], "proceed_reframed")
            self.assertEqual(session.step_state(4)["status"], "locked")

    def test_fast_mode_stops_for_every_authoritative_stop_path(self) -> None:
        cases = (
            (STOP_YAML, "scope_and_pipeline_disposition.pipeline_case_disposition", "stop"),
            (FINAL_PIPELINE_STOP_YAML, "final_pre_analysis_status.pipeline_case_disposition", "stop"),
            (FINAL_STATUS_STOP_YAML, "final_pre_analysis_status.status", "stop_before_core"),
            (FINAL_NEXT_STEP_STOP_YAML, "final_pre_analysis_status.next_allowed_step", "stop"),
            (THREE_FINAL_STOPS_YAML, "final_pre_analysis_status.pipeline_case_disposition", "stop"),
        )
        for yaml_text, expected_path, expected_value in cases:
            with self.subTest(expected_path=expected_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    self._project(root)
                    session = CaseStore(root).create_case(
                        {**BASE_VALUES, "ai_review_steps_enabled": False}
                    )
                    session.write_output(1, "read", complete=True)
                    session.write_output(2, yaml_text, complete=True)

                    self.assertIsNone(session.current_step_id())
                    self.assertEqual(
                        session.session_data["run_status"],
                        "pipeline_stopped_by_pre_analysis",
                    )
                    self.assertEqual(session.discipline_stop["key_path"], expected_path)
                    self.assertEqual(session.discipline_stop["detected_value"], expected_value)
                    self.assertEqual(session.step_state(4)["status"], "locked")

    def test_full_review_corrected_yaml_with_final_stop_overrides_proceed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, PROCEED_YAML, complete=True)
            session.write_output(
                3,
                f"CHECK STATUS: corrected\n```yaml\n{FINAL_PIPELINE_STOP_YAML}```",
                complete=True,
            )

            self.assertIsNone(session.current_step_id())
            self.assertEqual(
                session.session_data["run_status"],
                "pipeline_stopped_by_pre_analysis",
            )
            self.assertEqual(session.discipline_stop["source_step"], 3)
            self.assertEqual(
                session.discipline_stop["key_path"],
                "final_pre_analysis_status.pipeline_case_disposition",
            )

    def test_reset_clears_stop_and_reopens_revision_step(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            session = CaseStore(root).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)
            session.write_output(3, "Pre-Analysis YAML checked. PMS-DISCIPLINE pipeline stop confirmed.", complete=True)

            session.reset_from_step(3)

            self.assertEqual(session.current_step_id(), 3)
            self.assertEqual(session.session_data["run_status"], "active")
            self.assertIsNone(session.discipline_stop)
            self.assertEqual(session.step_state(4)["status"], "open")

    def test_reopening_case_preserves_stop(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._project(root)
            store = CaseStore(root)
            session = store.create_case({**BASE_VALUES, "ai_review_steps_enabled": False})
            session.write_output(1, "read", complete=True)
            session.write_output(2, STOP_YAML, complete=True)

            reopened = store.load_case(session.case_dir)

            self.assertIsNone(reopened.current_step_id())
            self.assertEqual(reopened.session_data["run_status"], "pipeline_stopped_by_pre_analysis")
            self.assertEqual(reopened.discipline_stop["detected_value"], "stop")
            self.assertEqual(reopened.step_state(4)["status"], "locked")


if __name__ == "__main__":
    unittest.main()
