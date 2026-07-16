from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.registry import AI_REVIEW_STEP_IDS, REVIEW_SOURCE_STEP
from orchestrator.storage import CaseStore
from orchestrator.yaml_validator import LocalYamlValidator


BASE_VALUES = {
    "title": "Review Settings Case",
    "description": "Synthetic case material",
    "source_status": "synthetic",
    "intended_use": "test",
    "local_yaml_validation_enabled": True,
    "yaml_validation_behavior": "warn",
}


class OptionalReviewFlowTests(unittest.TestCase):
    def test_review_registry_covers_all_semantic_check_steps(self) -> None:
        self.assertEqual(
            AI_REVIEW_STEP_IDS,
            (3, 5, 7, 10, 12, 15, 17, 19, 21, 23, 25, 31),
        )
        self.assertEqual(set(REVIEW_SOURCE_STEP), set(AI_REVIEW_STEP_IDS))

    def test_fast_core_only_article_run_skips_all_ai_reviews(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            values = {**BASE_VALUES, "ai_review_steps_enabled": False}
            session = CaseStore(Path(temp_dir)).create_case(values)

            for step_id in AI_REVIEW_STEP_IDS:
                self.assertEqual(session.step_state(step_id)["status"], "skipped")

            for step_id in (1, 2, 4, 6):
                self.assertEqual(session.current_step_id(), step_id)
                session.write_output(step_id, f"output {step_id}", complete=True)

            self.assertEqual(session.session_data["run_status"], "awaiting_addon_route")
            self.assertTrue(session.route_ready("addon"))
            self.assertEqual(session.required_route_step("addon"), 6)

            session.set_route({
                "route_type": "core_only",
                "selected_addon": None,
                "selection_basis": "manual_user_route",
            })
            self.assertEqual(session.current_step_id(), 11)
            session.write_output(11, "mip gate", complete=True)
            self.assertEqual(session.session_data["run_status"], "awaiting_mip_route")
            self.assertTrue(session.route_ready("mip"))

            session.set_mip_route({
                "route_type": "no_mip",
                "selection_basis": "manual_user_route",
            })
            for step_id in (20, 22, 24):
                self.assertEqual(session.current_step_id(), step_id)
                session.write_output(step_id, f"output {step_id}", complete=True)

            self.assertEqual(session.current_step_id(), 26)
            session.write_output(26, "iteration handoff", complete=True)
            self.assertEqual(session.session_data["run_status"], "awaiting_article_route")
            self.assertEqual(session.required_route_step("article"), 26)
            session.set_article_route({
                "route_type": "generate_article",
                "selection_basis": "user_confirmed",
            })
            for step_id in (27, 28, 29, 30):
                self.assertEqual(session.current_step_id(), step_id)
                session.write_output(step_id, f"output {step_id}", complete=True)

            self.assertEqual(session.session_data["run_status"], "pipeline_complete_with_article")
            self.assertIsNone(session.current_step_id())
            self.assertEqual(session.step_state(31)["status"], "skipped")

    def test_disabling_current_unfinished_review_archives_and_advances(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "pre-analysis", complete=True)
            self.assertEqual(session.current_step_id(), 3)
            session.write_prompt(3, "review prompt")
            session.write_output(3, "unsaved-like draft", complete=False)

            session.update_case({**BASE_VALUES, "ai_review_steps_enabled": False})

            self.assertFalse(session.ai_review_steps_enabled)
            self.assertEqual(session.step_state(3)["status"], "skipped")
            self.assertEqual(session.current_step_id(), 4)
            self.assertEqual(session.step_state(4)["status"], "current")
            self.assertFalse(session.prompt_path(3).exists())
            self.assertFalse(session.output_path(3).exists())
            archives = list(session.history_dir.glob("*-ai-review-disabled"))
            self.assertEqual(len(archives), 1)

    def test_enabling_reviews_while_awaiting_route_reopens_review_step(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case({**BASE_VALUES, "ai_review_steps_enabled": False})
            for step_id in (1, 2, 4, 6):
                session.write_output(step_id, f"output {step_id}", complete=True)
            self.assertEqual(session.session_data["run_status"], "awaiting_addon_route")

            session.update_case({**BASE_VALUES, "ai_review_steps_enabled": True})

            self.assertTrue(session.ai_review_steps_enabled)
            self.assertEqual(session.current_step_id(), 7)
            self.assertEqual(session.step_state(7)["status"], "current")
            self.assertEqual(session.session_data["run_status"], "active")


    def test_past_unchecked_route_remains_reviewable_after_enabling_future_reviews(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case({**BASE_VALUES, "ai_review_steps_enabled": False})
            for step_id in (1, 2, 4, 6):
                session.write_output(step_id, f"output {step_id}", complete=True)
            session.set_route({
                "route_type": "core_only",
                "selected_addon": None,
                "selection_basis": "manual_user_route",
            })
            self.assertEqual(session.current_step_id(), 11)

            session.update_case({**BASE_VALUES, "ai_review_steps_enabled": True})

            self.assertTrue(session.route_ready("addon"))
            self.assertEqual(session.required_route_step("addon"), 6)
            self.assertEqual(session.step_state(7)["status"], "skipped")
            self.assertEqual(session.step_state(12)["status"], "open")

    def test_invalid_validation_behavior_is_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case({
                **BASE_VALUES,
                "yaml_validation_behavior": "unsupported",
            })
            self.assertEqual(session.yaml_validation_behavior, "warn")
            self.assertEqual(session.case_data["yaml_validation_behavior"], "warn")


class LocalYamlValidatorTests(unittest.TestCase):
    def _fixture(self, temp_dir: str) -> tuple[Path, LocalYamlValidator]:
        root = Path(temp_dir)
        (root / "templates").mkdir()
        (root / "templates" / "reference.yaml").write_text(
            """root:\n  flag: \"<true | false>\"\n  status: \"<active | inactive>\"\n  child:\n    required: \"<text>\"\n  mode: \"<text>\"\n""",
            encoding="utf-8",
        )
        manifest = {
            "schema_version": "TEST",
            "steps": {
                "2": {
                    "reference": "templates/reference.yaml",
                    "compare_keys": True,
                    "allow_extra_keys": False,
                    "extract_placeholder_enums": True,
                    "rules": [
                        {"path": "root.mode", "allowed_values": ["safe", "strict"]}
                    ],
                },
                "14": {
                    "reference": None,
                    "compare_keys": False,
                    "note": "syntax only",
                },
            },
        }
        manifest_path = root / "yaml_validation_manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return root, LocalYamlValidator(root, manifest_path)

    def test_valid_structure_and_enum_values_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            text = """root:\n  flag: true\n  status: active\n  child:\n    required: value\n  mode: safe\n"""
            result = validator.validate(
                step_id=2,
                text=text,
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertTrue(result.syntax_valid)
            self.assertTrue(result.reference_available)
            self.assertEqual(result.issues, [])

    def test_missing_unexpected_and_invalid_values_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            text = """root:\n  flag: false\n  status: maybe\n  child: {}\n  mode: dangerous\n  extra: value\n"""
            result = validator.validate(
                step_id=2,
                text=text,
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            categories = [issue.category for issue in result.issues]
            self.assertIn("missing_key", categories)
            self.assertIn("unexpected_key", categories)
            self.assertEqual(categories.count("invalid_value"), 2)


    def test_dynamic_identifier_placeholders_do_not_become_enums(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "templates").mkdir()
            (root / "templates" / "reference.yaml").write_text(
                "root:\n  source_target_id: \"<stable short id or null>\"\n  status: \"<approved | declined>\"\n",
                encoding="utf-8",
            )
            manifest = {
                "schema_version": "TEST",
                "steps": {
                    "26": {
                        "reference": "templates/reference.yaml",
                        "compare_keys": True,
                        "allow_extra_keys": False,
                        "extract_placeholder_enums": True,
                    }
                },
            }
            (root / "yaml_validation_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            validator = LocalYamlValidator(root, root / "yaml_validation_manifest.json")

            result = validator.validate(
                step_id=26,
                text="root:\n  source_target_id: detail_materiality\n  status: approved\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )

            self.assertEqual(result.issues, [])

    def test_invalid_yaml_reports_line_and_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            result = validator.validate(
                step_id=2,
                text="root:\n  broken: [\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertFalse(result.syntax_valid)
            self.assertIn("line", result.syntax_error or "")
            self.assertIn("column", result.syntax_error or "")

    def test_single_yaml_code_fence_is_unwrapped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            text = """```yaml\nroot:\n  flag: yes\n  status: inactive\n  child:\n    required: value\n  mode: strict\n```"""
            result = validator.validate(
                step_id=2,
                text=text,
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertTrue(result.clean)

    def test_syntax_only_profile_does_not_require_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            result = validator.validate(
                step_id=14,
                text="root:\n  value: ok\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertTrue(result.syntax_valid)
            self.assertFalse(result.reference_available)
            self.assertEqual(result.issues, [])
            self.assertIn("syntax only", result.short_summary())

    def test_non_yaml_step_and_disabled_validation_are_not_applied(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            non_yaml = validator.validate(
                step_id=2,
                text="not yaml: [",
                expects_yaml=False,
                enabled=True,
                selected_addon=None,
            )
            disabled = validator.validate(
                step_id=2,
                text="not yaml: [",
                expects_yaml=True,
                enabled=False,
                selected_addon=None,
            )
            self.assertFalse(non_yaml.applicable)
            self.assertFalse(disabled.enabled)


    def test_duplicate_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            result = validator.validate(
                step_id=2,
                text="root:\n  flag: true\n  flag: false\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertFalse(result.syntax_valid)
            self.assertIn("duplicate key", (result.syntax_error or "").lower())

    def test_packaged_mip_and_ahp_profiles_use_source_substructures(self) -> None:
        root = Path(__file__).resolve().parents[1]
        validator = LocalYamlValidator(root, root / "yaml_validation_manifest.json")
        self.assertIsNotNone(validator._manifest)
        mip = validator._manifest.step_config(14, None)
        ahp = validator._manifest.step_config(18, None)
        self.assertEqual(mip["reference_subpath"], "case")
        self.assertEqual(mip["reference_root_key"], "case")
        self.assertEqual(ahp["reference_subpath"], "case_schema_patch.merge_into_case")

    def test_packaged_manifest_resolves_selected_addon_template(self) -> None:
        root = Path(__file__).resolve().parents[1]
        validator = LocalYamlValidator(root, root / "yaml_validation_manifest.json")
        config = validator._manifest.step_config(9, "EDEN") if validator._manifest else None
        self.assertIsNotNone(config)
        self.assertEqual(
            config["reference"],
            "templates/pms_addon_eden_case_application_template.yaml",
        )

    def test_review_output_can_use_source_step_validation_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            result = validator.validate(
                step_id=3,
                profile_step_id=2,
                text="root:\n  flag: true\n  status: active\n  child:\n    required: value\n  mode: safe\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            self.assertTrue(result.clean)
            self.assertEqual(result.step_id, 3)
            self.assertEqual(result.validation_profile_step_id, 2)

    def test_complete_yaml_detection_requires_mapping_or_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = self._fixture(temp_dir)
            self.assertTrue(validator.is_complete_yaml_mapping_or_sequence("root:\n  value: ok\n"))
            self.assertTrue(validator.is_complete_yaml_mapping_or_sequence("- one\n- two\n"))
            self.assertFalse(validator.is_complete_yaml_mapping_or_sequence("CHECK STATUS: ready\nMore prose"))
            self.assertFalse(validator.is_complete_yaml_mapping_or_sequence("plain prose"))


class YamlValidationHandoffTests(unittest.TestCase):
    @staticmethod
    def _findings_report(step_id: int = 2) -> dict:
        return {
            "step_id": step_id,
            "status": "findings",
            "applicable": True,
            "enabled": True,
            "dependency_available": True,
            "syntax_valid": True,
            "reference_available": True,
            "reference_path": "templates/reference.yaml",
            "validation_profile_step_id": step_id,
            "syntax_error": None,
            "note": None,
            "empty": False,
            "summary": "YAML validation: Syntax valid · 1 missing · 1 unexpected · 0 type · 1 value",
            "counts": {
                "missing_keys": 1,
                "unexpected_keys": 1,
                "type_mismatches": 0,
                "invalid_values": 1,
                "total_findings": 3,
            },
            "issues": [
                {
                    "category": "missing_key",
                    "path": "root.required",
                    "message": "key is present in the supplied reference YAML",
                },
                {
                    "category": "unexpected_key",
                    "path": "root.extra",
                    "message": "key is not present in the supplied reference YAML",
                },
                {
                    "category": "invalid_value",
                    "path": "root.status",
                    "message": "value 'maybe' is not one of: 'active', 'inactive'",
                },
            ],
        }

    def test_validation_report_is_persisted_and_claimed_by_next_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: maybe\n", complete=True)
            path = session.save_yaml_validation_report(
                2,
                self._findings_report(),
                completion_state="completed",
            )

            self.assertTrue(path.is_file())
            self.assertTrue(session.step_has_unresolved_yaml_findings(2))
            self.assertEqual(session.step_state(2)["yaml_validation_issue_count"], 3)

            claimed = session.claim_yaml_validation_handoffs(3)
            self.assertEqual(len(claimed), 1)
            self.assertEqual(claimed[0]["handoff_target_step"], 3)
            self.assertEqual(session.step_state(2)["yaml_validation_handoff_target_step"], 3)

            claimed_again = session.claim_yaml_validation_handoffs(3)
            self.assertEqual(len(claimed_again), 1)
            self.assertEqual(session.claim_yaml_validation_handoffs(4), [])

    def test_clean_validation_replaces_findings_and_clears_yellow_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: active\n", complete=True)
            session.save_yaml_validation_report(2, self._findings_report(), completion_state="completed")
            session.claim_yaml_validation_handoffs(3)

            clean_report = self._findings_report()
            clean_report.update({
                "status": "clean",
                "summary": "YAML validation: Valid · keys and explicit values match the reference.",
                "issues": [],
                "counts": {
                    "missing_keys": 0,
                    "unexpected_keys": 0,
                    "type_mismatches": 0,
                    "invalid_values": 0,
                    "total_findings": 0,
                },
            })
            session.save_yaml_validation_report(2, clean_report, completion_state="completed")

            self.assertFalse(session.step_has_unresolved_yaml_findings(2))
            stored = session.load_yaml_validation_report(2)
            self.assertIsNotNone(stored)
            assert stored is not None
            self.assertIsNone(stored["handoff_target_step"])
            self.assertEqual(session.step_state(2)["yaml_validation_issue_count"], 0)

    def test_disabling_target_review_requeues_handoff_for_next_active_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: maybe\n", complete=True)
            session.save_yaml_validation_report(2, self._findings_report(), completion_state="completed")
            session.claim_yaml_validation_handoffs(3)
            session.write_prompt(3, "review prompt with handoff")

            session.update_case({**BASE_VALUES, "ai_review_steps_enabled": False})

            self.assertEqual(session.current_step_id(), 4)
            report = session.load_yaml_validation_report(2)
            self.assertIsNotNone(report)
            assert report is not None
            self.assertIsNone(report["handoff_target_step"])
            claimed = session.claim_yaml_validation_handoffs(4)
            self.assertEqual(len(claimed), 1)
            self.assertEqual(claimed[0]["handoff_target_step"], 4)

    def test_reset_archives_and_removes_validation_report_for_reset_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: maybe\n", complete=True)
            session.save_yaml_validation_report(2, self._findings_report(), completion_state="completed")

            archive = session.reset_from_step(2)

            self.assertIsNotNone(archive)
            assert archive is not None
            self.assertTrue((archive / "validation" / "step_02_yaml_validation.json").is_file())
            self.assertFalse(session.validation_report_path(2).exists())
            self.assertFalse(session.step_has_unresolved_yaml_findings(2))

    def test_clean_corrected_yaml_resolves_source_handoff_but_keeps_source_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: maybe\n", complete=True)
            source_report = self._findings_report(2)
            session.save_yaml_validation_report(2, source_report, completion_state="completed")
            session.claim_yaml_validation_handoffs(3)
            session.write_output(3, "root:\n  status: active\n", complete=True)

            clean_report = {
                **source_report,
                "step_id": 3,
                "validation_profile_step_id": 2,
                "status": "clean",
                "summary": "YAML validation: Valid · keys and explicit values match the reference.",
                "issues": [],
                "counts": {
                    "missing_keys": 0,
                    "unexpected_keys": 0,
                    "type_mismatches": 0,
                    "invalid_values": 0,
                    "total_findings": 0,
                },
            }
            session.save_yaml_validation_report(3, clean_report, completion_state="completed")

            self.assertTrue(session.step_has_yaml_findings(2))
            self.assertFalse(session.step_has_unresolved_yaml_findings(2))
            self.assertEqual(session.yaml_findings_resolution(2), 3)
            self.assertEqual(session.claim_yaml_validation_handoffs(4), [])
            stored = session.load_yaml_validation_report(2)
            assert stored is not None
            self.assertEqual(stored["resolved_by_step"], 3)

    def test_resetting_resolver_reopens_original_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(BASE_VALUES)
            session.write_output(1, "read", complete=True)
            session.write_output(2, "root:\n  status: maybe\n", complete=True)
            source_report = self._findings_report(2)
            session.save_yaml_validation_report(2, source_report, completion_state="completed")
            session.claim_yaml_validation_handoffs(3)
            session.write_output(3, "root:\n  status: active\n", complete=True)
            clean_report = {
                **source_report,
                "step_id": 3,
                "validation_profile_step_id": 2,
                "status": "clean",
                "issues": [],
                "counts": {
                    "missing_keys": 0,
                    "unexpected_keys": 0,
                    "type_mismatches": 0,
                    "invalid_values": 0,
                    "total_findings": 0,
                },
            }
            session.save_yaml_validation_report(3, clean_report, completion_state="completed")
            session.reset_from_step(3)

            self.assertTrue(session.step_has_unresolved_yaml_findings(2))
            self.assertIsNone(session.yaml_findings_resolution(2))
            report = session.load_yaml_validation_report(2)
            assert report is not None
            self.assertIsNone(report["handoff_target_step"])

    def test_result_serialization_contains_exact_issue_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            _, validator = LocalYamlValidatorTests()._fixture(temp_dir)
            result = validator.validate(
                step_id=2,
                text="root:\n  flag: false\n  status: maybe\n  child: {}\n  mode: dangerous\n  extra: value\n",
                expects_yaml=True,
                enabled=True,
                selected_addon=None,
            )
            report = result.to_report_dict()
            self.assertEqual(report["status"], "findings")
            paths = {issue["path"] for issue in report["issues"]}
            self.assertIn("root.child.required", paths)
            self.assertIn("root.extra", paths)
            self.assertIn("root.status", paths)


if __name__ == "__main__":
    unittest.main()
