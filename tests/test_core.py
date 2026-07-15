from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.app import OrchestratorApp
from orchestrator.case_materials import (
    CaseMaterialError,
    CaseMaterialStore,
    render_case_material_manifest_block,
    render_case_material_prompt_block,
)
from orchestrator.gate_reader import (
    read_addon_gate_status,
    read_addon_recommendation,
    read_ahp_recommendation,
    read_mip_recommendation,
)
from orchestrator.prompt_source import PromptSource
from orchestrator.registry import AHP_SOURCE_FILENAME, MIP_SOURCE_FILENAME, STEPS, get_step, resolve_upload_files
from orchestrator.source_manager import SourceDownloadError, SourceManifest
from orchestrator.storage import ARTICLE_PROFILE_CASE, ARTICLE_PROFILE_FULL, CaseStore, StorageError


CASE_VALUES = {
    "title": "A Case",
    "description": "Description",
    "source_status": "unknown",
    "intended_use": "test",
}


class PromptSourceTests(unittest.TestCase):
    def test_load_and_render_all_thirty_prompts(self) -> None:
        source_path = Path(__file__).resolve().parents[1] / "resources" / "Prompts and Instructions.md"
        source = PromptSource(source_path)
        for number in range(1, 31):
            self.assertIn(number, source.available_prompt_numbers())
            raw = source.get(number)
            self.assertFalse(raw.startswith("\n"))
            self.assertFalse(raw.endswith("---"))
            self.assertEqual(raw, raw.rstrip())

        material_block = (
            "CASE MATERIAL PACKAGE — RUNNER-GENERATED\n"
            "material_count: 1\n"
            "material_1: sample.zip"
        )
        step_one = source.render(
            1,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_MATERIALS": material_block},
        )
        self.assertIn(material_block, step_one)
        self.assertIn("Read PMS.yaml before reading any case material", step_one)
        self.assertNotIn("{RUNNER_CASE_MATERIALS}", step_one)

        rendered = source.render(2, CASE_VALUES)
        self.assertIn("A Case", rendered)
        self.assertIn("Description", rendered)
        self.assertIn("case materials were read in step #1", rendered)
        self.assertNotIn("{CASE_TITLE}", rendered)

        addon_rendered = source.render(9, CASE_VALUES, selected_addon="EDEN")
        self.assertIn("SELECTED ADD-ON FAMILY:\nEDEN", addon_rendered)
        self.assertIn("pms_addon_eden_case_application_template.yaml", addon_rendered)

        mip_rendered = source.render(13, CASE_VALUES)
        self.assertIn(MIP_SOURCE_FILENAME, mip_rendered)
        self.assertNotIn("MIP.yaml", mip_rendered)

        ahp_rendered = source.render(18, CASE_VALUES)
        self.assertIn(AHP_SOURCE_FILENAME, ahp_rendered)

        article_rendered = source.render(27, CASE_VALUES)
        self.assertIn("Create the base Markdown article draft for the selected article profile", article_rendered)
        self.assertIn("selected_profile: full_analysis_article", article_rendered)
        self.assertIn("For `case_article`", article_rendered)
        self.assertIn("A Case", article_rendered)

        stage1_manifest = "RUNNER-GENERATED STAGE 1 MANIFEST\nstep_01: status=completed"
        stage1_rendered = source.render(20, CASE_VALUES, runtime_values={"RUNNER_STAGE_1_MANIFEST": stage1_manifest})
        self.assertIn(stage1_manifest, stage1_rendered)
        self.assertIn("CURRENT-STEP SELF-REFERENCE RULE", stage1_rendered)
        self.assertIn("must not be set to no solely", stage1_rendered)
        self.assertNotIn("{RUNNER_STAGE_1_MANIFEST}", stage1_rendered)

        stage1_check = source.render(21, CASE_VALUES, runtime_values={"RUNNER_STAGE_1_MANIFEST": stage1_manifest})
        self.assertIn("Reject or correct AI-service-local paths", stage1_check)
        self.assertIn("mark the future templates deferred", stage1_check)
        self.assertIn("MANDATORY CRITERIA LEDGER", stage1_check)
        self.assertIn("Do not declare ready while any criterion remains FAIL", stage1_check)

        case_record_manifest = "RUNNER-GENERATED CASE-RECORD MANIFEST\nstep_22: expected_output=outputs/step_22_stage_2_layer_digests.yaml"
        for number in (22, 23, 24, 25):
            rendered_case_record = source.render(
                number,
                CASE_VALUES,
                runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
            )
            self.assertIn(case_record_manifest, rendered_case_record)
            self.assertNotIn("{RUNNER_CASE_RECORD_MANIFEST}", rendered_case_record)

        self.assertIn("session.json is not used as a substitute", source.render(
            23,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        ))
        self.assertIn("workflow QA notes are metadata issues, not substantive case findings", source.render(
            24,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        ))

        stage2_prompt = source.render(
            22,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        )
        self.assertIn("preserve each operator's canonical identity", stage2_prompt)
        self.assertIn("`Λ` remains `Non-Event`", stage2_prompt)
        self.assertIn("must not be redefined as continuity", stage2_prompt)

        stage2_check_prompt = source.render(
            23,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        )
        self.assertIn("PMS operator identity or function changed during digest compression", stage2_check_prompt)
        self.assertIn("without renaming, repurposing, merging, or substitution", stage2_check_prompt)

        stage3_prompt = source.render(
            24,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        )
        self.assertIn("Preserve canonical PMS operator identities and functions exactly", stage3_prompt)

        stage3_check_prompt = source.render(
            25,
            CASE_VALUES,
            runtime_values={"RUNNER_CASE_RECORD_MANIFEST": case_record_manifest},
        )
        self.assertIn("canonical PMS operator identities, functions, and checked case-specific roles remain unchanged", stage3_check_prompt)

        for number in (26, 27, 28, 29, 30):
            article_prompt = source.render(number, CASE_VALUES)
            self.assertIn("selected_profile: full_analysis_article", article_prompt)
            case_contract = (
                "ARTICLE PROFILE — RUNNER-GENERATED\n"
                "selected_profile: case_article\n"
                "CASE ARTICLE CONTRACT"
            )
            case_prompt = source.render(
                number,
                CASE_VALUES,
                runtime_values={"RUNNER_ARTICLE_PROFILE_CONTRACT": case_contract},
            )
            self.assertIn("selected_profile: case_article", case_prompt)
            self.assertNotIn("{RUNNER_ARTICLE_PROFILE_CONTRACT}", case_prompt)


        default_article_prompt = source.render(27, CASE_VALUES)
        self.assertIn("CANONICAL PMS OPERATOR NAMING RULE", default_article_prompt)
        self.assertIn("Δ (Difference)", default_article_prompt)
        self.assertIn("first occurrence of each operator in every paragraph", default_article_prompt)
        self.assertIn("`**Δ** (Difference)`", default_article_prompt)

        self.assertIn(
            "Normally place them in no more than one compact calibration paragraph",
            default_article_prompt,
        )
        self.assertIn(
            "Normally select the two to four risks nearest to the case material",
            default_article_prompt,
        )
        self.assertIn(
            "remote legal, clinical, forensic, HR, automated-decision",
            default_article_prompt,
        )

        final_article_prompt = source.render(29, CASE_VALUES)
        self.assertIn("In every rewritten or newly inserted paragraph", final_article_prompt)
        self.assertIn("Do not replace canonical operator names with case-specific descriptions", final_article_prompt)

        self.assertIn(
            "Do not unpack grouped operators into separate paragraphs",
            final_article_prompt,
        )
        self.assertIn(
            "Keep the case-specific boundary focused on the risks nearest",
            final_article_prompt,
        )

        article_check_prompt = source.render(30, CASE_VALUES)
        self.assertIn("Every paragraph containing PMS operator prose", article_check_prompt)
        self.assertIn("Canonical operator names are not replaced by case-specific glosses or functions", article_check_prompt)

        self.assertIn(
            "should normally be grouped by shared calibration function",
            article_check_prompt,
        )
        self.assertIn(
            "prioritize the two to four misuse or escalation risks",
            article_check_prompt,
        )
        self.assertIn(
            "repeated calibration points",
            article_check_prompt,
        )


class ArticleProfileContractTests(unittest.TestCase):
    def test_runtime_contract_contains_canonical_operator_naming_rule(self) -> None:
        class SessionStub:
            article_profile = ARTICLE_PROFILE_CASE

        app = OrchestratorApp.__new__(OrchestratorApp)
        app.session = SessionStub()

        contract = app._article_profile_contract(27)

        self.assertIn("CANONICAL PMS OPERATOR NAMING RULE", contract)
        self.assertIn("Δ (Difference)", contract)
        self.assertIn("Λ (Non-Event)", contract)
        self.assertIn("Ψ (Self-Binding)", contract)
        self.assertIn("first occurrence of each operator in every paragraph", contract)
        self.assertIn("`**Δ** (Difference)`", contract)
        self.assertIn("Do not replace a canonical operator name with a case-specific gloss", contract)
        self.assertIn(
            "Group weak, conditional, dependency-limited, inactive, or analytic-only operators",
            contract,
        )
        self.assertIn(
            "two to four misuse or escalation risks nearest",
            contract,
        )
        self.assertIn(
            "concrete proximity to that misuse",
            contract,
        )

class RunnerManifestTests(unittest.TestCase):
    def _app_for_session(self, session, project_root: Path) -> OrchestratorApp:
        app = OrchestratorApp.__new__(OrchestratorApp)
        app.project_root = project_root
        app.session = session
        app._material_manifest_entries = lambda: []
        return app

    def _core_only_stage_1_session(self, project_root: Path):
        session = CaseStore(project_root).create_case(CASE_VALUES)
        for step_id in range(1, 8):
            session.write_output(step_id, f"output {step_id}", complete=True)
        session.set_route({
            "route_type": "core_only",
            "selected_addon": None,
            "selection_basis": "manual_user_route",
        })
        session.write_output(11, "output 11", complete=True)
        session.write_output(12, "output 12", complete=True)
        session.set_mip_route({
            "route_type": "no_mip",
            "selection_basis": "manual_user_route",
        })
        return session

    def test_stage_1_manifest_uses_selected_run_resources_without_self_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            for relative in (
                "pms/PMS.yaml",
                "templates/pms_discipline_pre_analysis_template.yaml",
                "templates/pms_core_case_application_template.yaml",
                "templates/pms_discipline_addon_recommendation_gate_template.yaml",
                "templates/pms_discipline_mip_gate_template.yaml",
                "templates/pms_case_record_stage_1_artifact_index_template.yaml",
            ):
                path = project_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("x", encoding="utf-8")
            session = self._core_only_stage_1_session(project_root)
            app = self._app_for_session(session, project_root)

            manifest = app._stage_1_runner_manifest()

            self.assertIn("SELECTED RUN RESOURCES", manifest)
            self.assertNotIn("LOCAL SOURCE AND TEMPLATE INVENTORY", manifest)
            self.assertNotIn("pms/PMS-ANTICIPATION.yaml", manifest)
            self.assertIn("CURRENT STEP EXECUTION METADATA", manifest)
            self.assertIn("The Stage 1 output must not index its own current production path", manifest)
            upstream = manifest.split("CURRENT STEP EXECUTION METADATA", 1)[0]
            self.assertNotIn("step_20", upstream)

    def test_stage_1_check_does_not_require_step_20_self_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            session = self._core_only_stage_1_session(project_root)
            session.write_output(20, "stage 1", complete=True)
            app = self._app_for_session(session, project_root)

            manifest = app._stage_1_check_runner_manifest()

            upstream = manifest.split("current_stage_1_output_under_review:", 1)[0]
            self.assertNotIn("step_20", upstream)
            self.assertIn("self_index_required: false", manifest)
            self.assertIn("outputs/step_20_stage_1_artifact_index.yaml", manifest)

    def test_case_record_manifest_separates_current_output_from_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            session = self._core_only_stage_1_session(project_root)
            session.write_output(20, "stage 1", complete=True)
            session.write_output(21, "stage 1 check", complete=True)
            app = self._app_for_session(session, project_root)

            manifest = app._case_record_runner_manifest(22)

            upstream = manifest.split("CURRENT STEP EXECUTION METADATA", 1)[0]
            self.assertNotIn("step_22", upstream)
            self.assertIn("expected_output: outputs/step_22_stage_2_layer_digests.yaml", manifest)
            self.assertIn("current_output_is_upstream_input: false", manifest)
            self.assertIn("Do not import current-step execution state", manifest)




class SourceManifestTests(unittest.TestCase):
    def test_packaged_manifest_contains_all_resources(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        manifest = SourceManifest.load(
            project_root / "source_manifest.json",
            project_root,
        )

        self.assertEqual(len(manifest.entries), 23)

        destinations = {
            entry.destination
            for entry in manifest.entries
        }

        self.assertIn(
            "templates/pms_discipline_pre_analysis_template.yaml",
            destinations,
        )
        self.assertIn(
            "templates/pms_core_case_application_template.yaml",
            destinations,
        )
        self.assertIn(
            "templates/pms_case_record_stage_3_full_case_record_integration_template.yaml",
            destinations,
        )
        self.assertIn("pms/PMS.yaml", destinations)
        self.assertIn("pms/PMS-EDEN.yaml", destinations)
        self.assertIn(
            "mip/MIP - Maturity in Practice.yaml",
            destinations,
        )
        self.assertIn(
            "mip/MIP - Maturity in Practice - AHP Module.yaml",
            destinations,
        )
        self.assertIn("pms/PMS.yaml", destinations)
        self.assertIn("pms/PMS-EDEN.yaml", destinations)
        self.assertIn("mip/MIP - Maturity in Practice.yaml", destinations)
        self.assertIn("mip/MIP - Maturity in Practice - AHP Module.yaml", destinations)

    def test_download_all_uses_manifest_destinations(self) -> None:
        source_manifest = Path(__file__).resolve().parents[1] / "source_manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "source_manifest.json"
            manifest_path.write_text(source_manifest.read_text(encoding="utf-8"), encoding="utf-8")
            manifest = SourceManifest.load(manifest_path, root)

            results = manifest.download_all(fetch_bytes=lambda url, timeout: f"downloaded from {url}\n".encode("utf-8"))

            self.assertEqual(len(results), 23)
            self.assertTrue(all(item.present for item in manifest.check()))
            self.assertIn(b"downloaded from", (root / "pms" / "PMS.yaml").read_bytes())

    def test_failed_download_does_not_replace_existing_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "source_manifest.json"
            manifest_path.write_text(
                json.dumps({
                    "sources": [
                        {"id": "one", "label": "One", "destination": "pms/one.yaml", "url": "https://example.test/one"},
                        {"id": "two", "label": "Two", "destination": "pms/two.yaml", "url": "https://example.test/two"},
                    ]
                }),
                encoding="utf-8",
            )
            (root / "pms").mkdir()
            first = root / "pms" / "one.yaml"
            second = root / "pms" / "two.yaml"
            first.write_text("old one", encoding="utf-8")
            second.write_text("old two", encoding="utf-8")
            manifest = SourceManifest.load(manifest_path, root)

            def failing_fetch(url: str, timeout: int) -> bytes:
                if url.endswith("/two"):
                    raise OSError("offline")
                return b"new one"

            with self.assertRaises(SourceDownloadError):
                manifest.download_all(fetch_bytes=failing_fetch)

            self.assertEqual(first.read_text(encoding="utf-8"), "old one")
            self.assertEqual(second.read_text(encoding="utf-8"), "old two")


class CaseMaterialStoreTests(unittest.TestCase):
    def test_adds_materials_and_renders_runner_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            case_dir.mkdir()
            source_zip = root / "packet.zip"
            source_zip.write_bytes(b"PK synthetic archive")
            source_csv = root / "statistics.csv"
            source_csv.write_text("name,value\nA,1\n", encoding="utf-8")

            store = CaseMaterialStore(case_dir, "case-001")
            entries = store.replace([
                {
                    "source_path": str(source_zip),
                    "description": "Archive containing the article and supporting notes.",
                    "purpose": "Primary material package for the case.",
                },
                {
                    "source_path": str(source_csv),
                    "description": "Small synthetic statistics table.",
                    "purpose": "Support bounded numerical references.",
                },
            ])

            self.assertEqual(len(entries), 2)
            self.assertTrue((case_dir / "materials.json").is_file())
            self.assertTrue(all(store.path_for(entry).is_file() for entry in entries))
            self.assertTrue(all(len(str(entry.get("sha256"))) == 64 for entry in entries))

            prompt_block = render_case_material_prompt_block(entries)
            self.assertIn("Read PMS.yaml first", prompt_block)
            self.assertIn("packet.zip", prompt_block)
            self.assertIn("Primary material package for the case", prompt_block)
            self.assertIn("ZIP HANDLING", prompt_block)

            manifest_entries = []
            for entry in entries:
                item = dict(entry)
                item["_present"] = store.path_for(entry).is_file()
                manifest_entries.append(item)
            manifest_block = render_case_material_manifest_block(
                manifest_entries,
                step_1_status="completed",
            )
            self.assertIn("CASE MATERIAL INVENTORY", manifest_block)
            self.assertIn("read_instruction_step: 1", manifest_block)
            self.assertIn("role: bounded_case_material", manifest_block)

    def test_removal_archives_previous_manifest_and_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            case_dir.mkdir()
            first = root / "first.txt"
            second = root / "second.txt"
            first.write_text("first", encoding="utf-8")
            second.write_text("second", encoding="utf-8")
            store = CaseMaterialStore(case_dir, "case-002")
            entries = store.replace([
                {"source_path": str(first), "description": "First", "purpose": "One"},
                {"source_path": str(second), "description": "Second", "purpose": "Two"},
            ])
            removed_path = store.path_for(entries[1])

            retained = dict(entries[0])
            retained["description"] = "Updated first description"
            updated = store.replace([retained])

            self.assertEqual(len(updated), 1)
            self.assertFalse(removed_path.exists())
            archives = list((case_dir / "history" / "material_revisions").glob("*-materials"))
            self.assertEqual(len(archives), 1)
            self.assertTrue((archives[0] / "materials.json").is_file())
            self.assertTrue((archives[0] / "materials" / removed_path.name).is_file())
            self.assertEqual(store.entries()[0]["description"], "Updated first description")

    def test_pipeline_reset_preserves_case_material_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            session = CaseStore(root).create_case(CASE_VALUES)
            source = root / "packet.zip"
            source.write_bytes(b"PK reset test")
            store = CaseMaterialStore(session.case_dir, session.case_id)
            entries = store.replace([{
                "source_path": str(source),
                "description": "Reset-safe packet",
                "purpose": "Remain attached to the case after a workflow reset.",
            }])
            session.write_output(1, "PMS and materials read", complete=True)
            session.write_output(2, "pre-analysis", complete=True)

            archive = session.reset_from_step(1)

            self.assertIsNotNone(archive)
            self.assertEqual(session.current_step_id(), 1)
            self.assertTrue(store.path_for(entries[0]).is_file())
            self.assertEqual(len(store.entries()), 1)

    def test_manifest_rejects_paths_outside_case_materials_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            case_dir.mkdir()
            (case_dir / "materials.json").write_text(
                json.dumps({
                    "schema_version": "PMS_ORCHESTRATOR_MATERIALS_1.0",
                    "case_id": "case-unsafe",
                    "materials": [{
                        "id": "material_001",
                        "stored_path": "../outside.txt",
                    }],
                }),
                encoding="utf-8",
            )
            store = CaseMaterialStore(case_dir, "case-unsafe")
            with self.assertRaises(CaseMaterialError):
                store.entries()

    def test_duplicate_filenames_are_stored_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            case_dir.mkdir()
            left = root / "left"
            right = root / "right"
            left.mkdir()
            right.mkdir()
            (left / "article.pdf").write_bytes(b"left")
            (right / "article.pdf").write_bytes(b"right")
            store = CaseMaterialStore(case_dir, "case-003")
            entries = store.replace([
                {"source_path": str(left / "article.pdf")},
                {"source_path": str(right / "article.pdf")},
            ])
            names = [store.path_for(entry).name for entry in entries]
            self.assertEqual(names, ["article.pdf", "article-2.pdf"])
            self.assertEqual(store.path_for(entries[0]).read_bytes(), b"left")
            self.assertEqual(store.path_for(entries[1]).read_bytes(), b"right")


class GateReaderTests(unittest.TestCase):
    def test_reads_supported_addon_and_status(self) -> None:
        text = """
gate_result:
  gate_status: selected_addon_recommended
  selected_addon: ANTICIPATION
"""
        recommendation = read_addon_recommendation(text, source_step=6)
        self.assertEqual(recommendation.value, "ANTICIPATION")
        self.assertEqual(recommendation.source_step, 6)
        self.assertEqual(read_addon_gate_status(text).value, "selected_addon_recommended")

    def test_missing_addon_key_is_non_blocking_null(self) -> None:
        result = read_addon_recommendation("CHECK STATUS: ready")
        self.assertIsNone(result.value)
        self.assertEqual(result.status, "key_not_found")
        self.assertEqual(result.display_value, "NULL")

    def test_none_and_unsupported_values_become_null(self) -> None:
        none_result = read_addon_recommendation("gate_result:\n  selected_addon: none\n")
        self.assertIsNone(none_result.value)
        self.assertEqual(none_result.status, "no_addon")
        unsupported = read_addon_recommendation("gate_result:\n  selected_addon: AXIOM\n")
        self.assertIsNone(unsupported.value)
        self.assertEqual(unsupported.status, "unsupported_value")

    def test_reads_mip_recommendation(self) -> None:
        recommended = read_mip_recommendation("mip_recommendation_output:\n  recommendation_status: recommended_with_limits\n")
        self.assertEqual(recommended.value, "MIP")
        not_recommended = read_mip_recommendation("mip_recommendation_output:\n  recommendation_status: not_recommended\n")
        self.assertIsNone(not_recommended.value)
        self.assertEqual(not_recommended.status, "not_recommended")

    def test_reads_ahp_recommendation(self) -> None:
        recommended = read_ahp_recommendation("gate_result:\n  gate_status: ahp_source_reading_recommended\n")
        self.assertEqual(recommended.value, "AHP")
        not_recommended = read_ahp_recommendation("gate_result:\n  gate_status: ahp_not_recommended\n")
        self.assertIsNone(not_recommended.value)
        self.assertEqual(not_recommended.status, "ahp_not_recommended")
        missing = read_ahp_recommendation("CHECK STATUS: ready")
        self.assertEqual(missing.display_value, "NULL")


class RegistryTests(unittest.TestCase):
    def test_registry_has_all_thirty_pipeline_steps(self) -> None:
        self.assertEqual([step.step_id for step in STEPS], list(range(1, 31)))

    def test_upload_files_match_step_contract(self) -> None:
        root = Path("C:/project")
        self.assertEqual(resolve_upload_files(get_step(3), root, None), [])
        self.assertEqual(resolve_upload_files(get_step(8), root, "LOGIC")[0].name, "PMS-LOGIC.yaml")
        self.assertEqual(resolve_upload_files(get_step(9), root, "LOGIC")[0].name, "pms_addon_logic_case_application_template.yaml")
        self.assertEqual(resolve_upload_files(get_step(13), root, None)[0].name, MIP_SOURCE_FILENAME)
        self.assertEqual(resolve_upload_files(get_step(16), root, None)[0].name, "pms_discipline_ahp_gate_template.yaml")
        self.assertEqual(resolve_upload_files(get_step(18), root, None)[0].name, AHP_SOURCE_FILENAME)
        self.assertEqual(resolve_upload_files(get_step(20), root, None)[0].name, "pms_case_record_stage_1_artifact_index_template.yaml")
        self.assertEqual(resolve_upload_files(get_step(22), root, None)[0].name, "pms_case_record_stage_2_layer_digest_extraction_template.yaml")
        self.assertEqual(resolve_upload_files(get_step(24), root, None)[0].name, "pms_case_record_stage_3_full_case_record_integration_template.yaml")
        for step_id in range(26, 31):
            self.assertEqual(resolve_upload_files(get_step(step_id), root, None), [])


class CaseStoreTests(unittest.TestCase):
    def _complete_through_step_7(self, session) -> None:
        for step_id in range(1, 8):
            session.write_output(step_id, f"output {step_id}", complete=True)

    def _complete_through_step_12_core_only(self, session) -> None:
        self._complete_through_step_7(session)
        session.set_route({"route_type": "core_only", "selected_addon": None, "selection_basis": "manual_user_route"})
        session.write_output(11, "output 11", complete=True)
        session.write_output(12, "output 12", complete=True)

    def _complete_case_record(self, session) -> None:
        for step_id in range(20, 26):
            session.write_output(step_id, f"output {step_id}", complete=True)

    def test_full_route_reaches_optional_article_decision_and_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_7(session)
            session.set_route({"route_type": "selected_addon", "selected_addon": "EDEN", "selection_basis": "gate_recommended"})
            for step_id in range(8, 13):
                session.write_output(step_id, f"output {step_id}", complete=True)
            session.set_mip_route({"route_type": "use_mip", "selection_basis": "gate_recommended"})
            for step_id in range(13, 18):
                session.write_output(step_id, f"output {step_id}", complete=True)
            session.set_ahp_route({"route_type": "use_ahp", "selection_basis": "gate_recommended"})
            session.write_output(18, "output 18", complete=True)
            session.write_output(19, "output 19", complete=True)
            self._complete_case_record(session)
            self.assertEqual(session.session_data["run_status"], "awaiting_article_route")
            self.assertIsNone(session.current_step_id())

            session.set_article_route({"route_type": "generate_article", "selection_basis": "user_confirmed"})
            self.assertEqual(session.current_step_id(), 26)
            for step_id in range(26, 31):
                session.write_output(step_id, f"output {step_id}", complete=True)
            self.assertEqual(session.session_data["run_status"], "pipeline_complete_with_article")
            self.assertIsNone(session.current_step_id())

    def test_no_article_finishes_after_stage_3(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self._complete_case_record(session)
            session.set_article_route({"route_type": "no_article", "selection_basis": "user_confirmed"})
            self.assertEqual(session.session_data["run_status"], "pipeline_complete_without_article")
            self.assertIsNone(session.current_step_id())
            for step_id in range(26, 31):
                self.assertEqual(session.step_state(step_id)["status"], "skipped")

    def test_article_decision_can_be_changed_later(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self._complete_case_record(session)
            session.set_article_route({"route_type": "no_article", "selection_basis": "user_confirmed"})
            changed = session.set_article_route({"route_type": "generate_article", "selection_basis": "user_confirmed"})
            self.assertTrue(changed)
            self.assertEqual(session.current_step_id(), 26)
            self.assertEqual(session.step_state(26)["status"], "current")

    def test_no_mip_can_be_changed_to_use_mip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self.assertEqual(session.step_state(13)["status"], "skipped")
            self.assertEqual(session.current_step_id(), 20)
            changed = session.set_mip_route({"route_type": "use_mip", "selection_basis": "user_requested"})
            self.assertTrue(changed)
            self.assertEqual(session.current_step_id(), 13)
            self.assertEqual(session.step_state(13)["status"], "current")
            self.assertEqual(session.step_state(20)["status"], "locked")

    def test_mip_route_revision_archives_dependent_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            session.write_output(20, "stage one draft", complete=False)
            self.assertTrue(session.output_path(20).exists())
            session.set_mip_route({"route_type": "use_mip", "selection_basis": "user_requested"})
            self.assertFalse(session.output_path(20).exists())
            archives = list(session.history_dir.glob("*-mip-route"))
            self.assertTrue(archives)
            self.assertTrue(any((archive / "outputs" / "step_20_stage_1_artifact_index.yaml").exists() for archive in archives))

    def test_reset_completed_step_reopens_it_and_archives_following_work(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            session.write_output(1, "output 1", complete=True)
            session.write_prompt(2, "prompt 2")
            session.write_output(2, "output 2", complete=True)
            self.assertEqual(session.current_step_id(), 3)

            archive = session.reset_from_step(2)

            self.assertIsNotNone(archive)
            assert archive is not None
            self.assertTrue((archive / "outputs" / "step_02_pre_analysis_output.yaml").exists())
            self.assertTrue((archive / "prompts" / "step_02_prompt.txt").exists())
            self.assertEqual(session.current_step_id(), 2)
            self.assertEqual(session.step_state(2)["status"], "current")
            for step_id in range(3, 8):
                self.assertEqual(session.step_state(step_id)["status"], "open")
            self.assertEqual(session.step_state(8)["status"], "locked")
            self.assertTrue(session.output_path(1).exists())
            self.assertFalse(session.output_path(2).exists())

    def test_reset_mip_gate_clears_only_dependent_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self.assertEqual(session.current_step_id(), 20)

            archive = session.reset_from_step(12)

            self.assertIsNotNone(archive)
            self.assertIsNotNone(session.session_data["route"])
            self.assertIsNone(session.session_data["mip_route"])
            self.assertIsNone(session.session_data["ahp_route"])
            self.assertIsNone(session.session_data["article_route"])
            self.assertEqual(session.current_step_id(), 12)
            self.assertEqual(session.step_state(12)["status"], "current")
            for step_id in range(13, 31):
                self.assertEqual(session.step_state(step_id)["status"], "locked")
            self.assertFalse((session.case_dir / "mip_route.json").exists())

    def test_reset_case_record_preserves_analytical_routes_and_clears_article(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self._complete_case_record(session)
            session.set_article_route({"route_type": "generate_article", "selection_basis": "user_confirmed"})
            session.write_output(26, "article contract", complete=True)

            archive = session.reset_from_step(20)

            self.assertIsNotNone(archive)
            self.assertEqual(session.session_data["route"]["route_type"], "core_only")
            self.assertEqual(session.session_data["mip_route"]["route_type"], "no_mip")
            self.assertIsNone(session.session_data["article_route"])
            self.assertEqual(session.current_step_id(), 20)
            self.assertEqual(session.step_state(20)["status"], "current")
            for step_id in range(21, 26):
                self.assertEqual(session.step_state(step_id)["status"], "open")
            for step_id in range(26, 31):
                self.assertEqual(session.step_state(step_id)["status"], "locked")
            for step_id in range(13, 20):
                self.assertEqual(session.step_state(step_id)["status"], "skipped")
            self.assertFalse((session.case_dir / "article_route.json").exists())

    def test_article_profile_is_persisted_and_profile_change_resets_only_article_steps(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "manual_user_route"})
            self._complete_case_record(session)

            session.set_article_route({
                "route_type": "generate_article",
                "article_profile": ARTICLE_PROFILE_CASE,
                "selection_basis": "user_confirmed",
            })
            self.assertEqual(session.article_profile, ARTICLE_PROFILE_CASE)
            for step_id in (26, 27, 28):
                session.write_output(step_id, f"article {step_id}", complete=True)
            self.assertTrue(session.output_path(25).is_file())

            changed = session.set_article_route({
                "route_type": "generate_article",
                "article_profile": ARTICLE_PROFILE_FULL,
                "selection_basis": "user_confirmed",
            })

            self.assertTrue(changed)
            self.assertEqual(session.article_profile, ARTICLE_PROFILE_FULL)
            self.assertEqual(session.current_step_id(), 26)
            self.assertTrue(session.output_path(25).is_file())
            for step_id in range(26, 31):
                self.assertFalse(session.output_path(step_id).is_file())
            saved = json.loads((session.case_dir / "article_route.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["article_profile"], ARTICLE_PROFILE_FULL)

    def test_legacy_generated_article_route_defaults_to_full_analysis_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = CaseStore(Path(temp_dir))
            session = store.create_case(CASE_VALUES)
            session.session_data["article_route"] = {
                "route_type": "generate_article",
                "selection_basis": "user_confirmed",
            }
            session.save()
            (session.case_dir / "article_route.json").write_text(
                json.dumps(session.session_data["article_route"]),
                encoding="utf-8",
            )

            loaded = store.load_case(session.case_dir)

            self.assertEqual(loaded.article_profile, ARTICLE_PROFILE_FULL)
            self.assertEqual(
                loaded.session_data["article_route"]["article_profile"],
                ARTICLE_PROFILE_FULL,
            )
            route_file = json.loads((loaded.case_dir / "article_route.json").read_text(encoding="utf-8"))
            self.assertEqual(route_file["article_profile"], ARTICLE_PROFILE_FULL)

    def test_skipped_step_cannot_be_reset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_7(session)
            session.set_route({"route_type": "core_only", "selected_addon": None, "selection_basis": "manual_user_route"})
            with self.assertRaises(StorageError):
                session.reset_from_step(8)

    def test_completed_output_can_be_saved_again(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            session.write_output(1, "first", complete=True)
            self.assertEqual(session.step_state(1)["status"], "completed")
            session.write_output(1, "revised", complete=False)
            self.assertEqual(session.load_output(1), "revised")
            self.assertEqual(session.step_state(1)["status"], "completed")

    def test_core_only_moves_directly_to_step_11(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_7(session)
            session.set_route({"route_type": "core_only", "selected_addon": None, "selection_basis": "gate_recommended_core_only"})
            self.assertEqual(session.current_step_id(), 11)
            for step_id in (8, 9, 10):
                self.assertEqual(session.step_state(step_id)["status"], "skipped")

    def test_no_mip_skips_analytical_branches_and_opens_stage_1(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "no_mip", "selection_basis": "gate_recommended_no_mip"})
            self.assertEqual(session.current_step_id(), 20)
            for step_id in range(13, 20):
                self.assertEqual(session.step_state(step_id)["status"], "skipped")
            self.assertEqual(session.step_state(20)["status"], "current")
            self.assertEqual(session.step_state(26)["status"], "locked")

    def test_no_ahp_opens_stage_1(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = CaseStore(Path(temp_dir)).create_case(CASE_VALUES)
            self._complete_through_step_12_core_only(session)
            session.set_mip_route({"route_type": "use_mip", "selection_basis": "gate_recommended"})
            for step_id in range(13, 18):
                session.write_output(step_id, f"output {step_id}", complete=True)
            session.set_ahp_route({"route_type": "no_ahp", "selection_basis": "gate_recommended_no_ahp"})
            self.assertEqual(session.current_step_id(), 20)
            self.assertEqual(session.step_state(18)["status"], "skipped")
            self.assertEqual(session.step_state(19)["status"], "skipped")

    def test_v04_complete_case_migrates_to_step_20(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = CaseStore(Path(temp_dir))
            session = store.create_case(CASE_VALUES)
            case_dir = session.case_dir
            data = json.loads((case_dir / "session.json").read_text(encoding="utf-8"))
            for step_id in range(20, 31):
                data["steps"].pop(str(step_id), None)
            for step_id in range(1, 20):
                data["steps"][str(step_id)]["status"] = "completed"
            data["schema_version"] = "PMS_ORCHESTRATOR_SESSION_0.4"
            data["run_status"] = "through_step_19_complete"
            data["current_step"] = None
            data["mip_route"] = {"route_type": "use_mip", "selection_basis": "gate_recommended"}
            data["ahp_route"] = {"route_type": "use_ahp", "selection_basis": "gate_recommended"}
            data.pop("article_route", None)
            (case_dir / "session.json").write_text(json.dumps(data), encoding="utf-8")
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            case["schema_version"] = "PMS_ORCHESTRATOR_CASE_0.4"
            (case_dir / "case.json").write_text(json.dumps(case), encoding="utf-8")

            migrated = store.load_case(case_dir)
            self.assertEqual(migrated.session_data["schema_version"], "PMS_ORCHESTRATOR_SESSION_1.3")
            self.assertEqual(migrated.current_step_id(), 20)
            self.assertEqual(migrated.step_state(20)["status"], "current")
            self.assertEqual(migrated.step_state(25)["status"], "open")
            self.assertEqual(migrated.step_state(26)["status"], "locked")

    def test_v05_stage_3_complete_case_migrates_to_article_question(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = CaseStore(Path(temp_dir))
            session = store.create_case(CASE_VALUES)
            case_dir = session.case_dir
            data = json.loads((case_dir / "session.json").read_text(encoding="utf-8"))
            for step_id in range(26, 31):
                data["steps"].pop(str(step_id), None)
            for step_id in range(1, 26):
                data["steps"][str(step_id)]["status"] = "completed"
            data["schema_version"] = "PMS_ORCHESTRATOR_SESSION_0.5"
            data["run_status"] = "through_step_25_complete"
            data["current_step"] = None
            data.pop("article_route", None)
            (case_dir / "session.json").write_text(json.dumps(data), encoding="utf-8")
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            case["schema_version"] = "PMS_ORCHESTRATOR_CASE_0.5"
            (case_dir / "case.json").write_text(json.dumps(case), encoding="utf-8")

            migrated = store.load_case(case_dir)
            self.assertEqual(migrated.session_data["run_status"], "awaiting_article_route")
            self.assertIsNone(migrated.current_step_id())
            self.assertIsNone(migrated.session_data["article_route"])
            for step_id in range(26, 31):
                self.assertEqual(migrated.step_state(step_id)["status"], "locked")

    def test_v04_active_ahp_case_keeps_current_step_during_migration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = CaseStore(Path(temp_dir))
            session = store.create_case(CASE_VALUES)
            case_dir = session.case_dir
            data = json.loads((case_dir / "session.json").read_text(encoding="utf-8"))
            for step_id in range(20, 31):
                data["steps"].pop(str(step_id), None)
            for step_id in range(1, 18):
                data["steps"][str(step_id)]["status"] = "completed"
            data["steps"]["18"]["status"] = "current"
            data["steps"]["19"]["status"] = "open"
            data["schema_version"] = "PMS_ORCHESTRATOR_SESSION_0.4"
            data["run_status"] = "active"
            data["current_step"] = 18
            data["mip_route"] = {"route_type": "use_mip", "selection_basis": "gate_recommended"}
            data["ahp_route"] = {"route_type": "use_ahp", "selection_basis": "gate_recommended"}
            data.pop("article_route", None)
            (case_dir / "session.json").write_text(json.dumps(data), encoding="utf-8")
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            case["schema_version"] = "PMS_ORCHESTRATOR_CASE_0.4"
            (case_dir / "case.json").write_text(json.dumps(case), encoding="utf-8")

            migrated = store.load_case(case_dir)
            self.assertEqual(migrated.current_step_id(), 18)
            self.assertEqual(migrated.step_state(18)["status"], "current")
            self.assertEqual(migrated.step_state(20)["status"], "locked")
            self.assertEqual(migrated.step_state(26)["status"], "locked")


class ArticleNoExamplesRunnerTests(unittest.TestCase):
    def _article_session_at_step_28(self, root: Path, *, reviews: bool = True):
        session = CaseStore(root).create_case({**CASE_VALUES, "ai_review_steps_enabled": reviews})
        session.session_data["article_route"] = {"route_type": "generate_article"}
        session.session_data["current_step"] = 28
        session.session_data["run_status"] = "active"
        for step_id in range(1, 31):
            session.step_state(step_id)["status"] = "locked"
        session.step_state(27)["status"] = "completed"
        session.step_state(28)["status"] = "current"
        session.step_state(29)["status"] = "open"
        session.step_state(30)["status"] = "open" if reviews else "skipped"
        session.output_path(27).parent.mkdir(parents=True, exist_ok=True)
        session.output_path(27).write_text("# Base article\n\nBody.", encoding="utf-8")
        session.step_state(27)["output_file"] = str(session.output_path(27).relative_to(session.case_dir))
        session.save()
        return session

    def test_no_examples_copies_base_article_and_skips_ai_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self._article_session_at_step_28(Path(temp_dir), reviews=True)
            session.write_output(28, "### Example decision\n\n**examples_not_needed**\n", complete=True)

            self.assertEqual(session.step_state(29)["status"], "completed_by_runner_no_examples")
            self.assertEqual(session.step_state(29)["runner_completion_mode"], "completed_by_runner_no_examples")
            self.assertEqual(session.output_path(29).read_text(encoding="utf-8"), "# Base article\n\nBody.")
            self.assertEqual(session.current_step_id(), 30)
            self.assertIn("No AI rewrite", session.load_prompt(29))

    def test_runner_completed_step_29_can_be_reset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self._article_session_at_step_28(Path(temp_dir), reviews=True)
            session.write_output(28, "examples_not_applicable", complete=True)
            archive = session.reset_from_step(29)

            self.assertIsNotNone(archive)
            self.assertEqual(session.current_step_id(), 29)
            self.assertEqual(session.step_state(29)["status"], "current")
            self.assertFalse(session.output_path(29).exists())
            self.assertIsNone(session.step_state(29)["runner_completion_mode"])

    def test_examples_optional_keeps_step_29_as_ai_step(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self._article_session_at_step_28(Path(temp_dir), reviews=True)
            session.write_output(28, "### Example decision\n\n**examples_optional**\n", complete=True)

            self.assertEqual(session.current_step_id(), 29)
            self.assertEqual(session.step_state(29)["status"], "current")
            self.assertFalse(session.output_path(29).exists())

    def test_no_examples_finishes_fast_mode_after_runner_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self._article_session_at_step_28(Path(temp_dir), reviews=False)
            session.write_output(28, "no_examples", complete=True)

            self.assertEqual(session.step_state(29)["status"], "completed_by_runner_no_examples")
            self.assertEqual(session.session_data["run_status"], "pipeline_complete_with_article")
            self.assertIsNone(session.current_step_id())



if __name__ == "__main__":
    unittest.main()
