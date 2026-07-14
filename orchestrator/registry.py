from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class StepDefinition:
    step_id: int
    title: str
    prompt_number: int
    upload_files: tuple[str, ...]
    context_steps: tuple[int, ...]
    output_filename: str
    output_label: str
    branch: str = "base"


STEPS: tuple[StepDefinition, ...] = (
    StepDefinition(1, "Read PMS.yaml", 1, ("pms/PMS.yaml",), (), "step_01_pms_read.txt", "PMS read confirmation"),
    StepDefinition(2, "Apply Pre-Analysis Template", 2, ("templates/pms_discipline_pre_analysis_template.yaml",), (1,), "step_02_pre_analysis_output.yaml", "Pre-Analysis output"),
    StepDefinition(3, "Check Pre-Analysis YAML", 3, (), (1, 2), "step_03_pre_analysis_check.txt", "Pre-Analysis check response"),
    StepDefinition(4, "Apply PMS Core Case Application Template", 4, ("templates/pms_core_case_application_template.yaml",), (1, 2, 3), "step_04_core_output.yaml", "PMS Core output"),
    StepDefinition(5, "Check PMS Core Case Application YAML", 5, (), (1, 2, 3, 4), "step_05_core_check.txt", "PMS Core check response"),
    StepDefinition(6, "Apply Add-on Recommendation Gate Template", 6, ("templates/pms_discipline_addon_recommendation_gate_template.yaml",), (1, 2, 3, 4, 5), "step_06_addon_gate_output.yaml", "Add-on Gate output"),
    StepDefinition(7, "Check Add-on Recommendation Gate YAML", 7, (), (1, 2, 3, 4, 5, 6), "step_07_addon_gate_check.txt", "Add-on Gate check response"),
    StepDefinition(8, "Read Selected PMS Add-on YAML", 8, ("pms/PMS-{SELECTED_ADDON}.yaml",), (1, 3, 5, 7), "step_08_selected_addon_read.txt", "Selected add-on read confirmation", branch="selected_addon"),
    StepDefinition(9, "Apply Selected PMS Add-on Case Application Template", 9, ("templates/pms_addon_{selected_addon_lower}_case_application_template.yaml",), (1, 3, 5, 7, 8), "step_09_selected_addon_output.yaml", "Selected add-on output", branch="selected_addon"),
    StepDefinition(10, "Check Selected PMS Add-on Case Application YAML", 10, (), (1, 3, 5, 7, 8, 9), "step_10_selected_addon_check.txt", "Selected add-on check response", branch="selected_addon"),
    StepDefinition(11, "Apply PMS-DISCIPLINE MIP Gate Template", 11, ("templates/pms_discipline_mip_gate_template.yaml",), (1, 3, 5, 7, 10), "step_11_mip_gate_output.yaml", "MIP Gate output"),
    StepDefinition(12, "Check PMS-DISCIPLINE MIP Gate YAML", 12, (), (1, 3, 5, 7, 10, 11), "step_12_mip_gate_check.txt", "MIP Gate check response"),
    StepDefinition(13, "Read MIP YAML", 13, ("mip/MIP - Maturity in Practice.yaml",), (1, 3, 5, 7, 10, 12), "step_13_mip_read.txt", "MIP read confirmation", branch="mip"),
    StepDefinition(14, "Apply MIP Case Application", 14, ("mip/MIP - Maturity in Practice.yaml",), (1, 3, 5, 7, 10, 12, 13), "step_14_mip_output.yaml", "MIP output", branch="mip"),
    StepDefinition(15, "Check MIP Case Application YAML", 15, (), (1, 3, 5, 7, 10, 12, 13, 14), "step_15_mip_check.txt", "MIP check response", branch="mip"),
    StepDefinition(16, "Apply PMS-DISCIPLINE AHP Gate Template", 16, ("templates/pms_discipline_ahp_gate_template.yaml",), (1, 3, 5, 7, 10, 12, 15), "step_16_ahp_gate_output.yaml", "AHP Gate output", branch="ahp"),
    StepDefinition(17, "Check PMS-DISCIPLINE AHP Gate YAML", 17, (), (1, 3, 5, 7, 10, 12, 15, 16), "step_17_ahp_gate_check.txt", "AHP Gate check response", branch="ahp"),
    StepDefinition(18, "Apply AHP Module", 18, ("mip/MIP - Maturity in Practice - AHP Module.yaml",), (1, 3, 5, 7, 10, 12, 15, 17), "step_18_ahp_output.yaml", "AHP Module output", branch="ahp_application"),
    StepDefinition(19, "Check AHP Module Output YAML", 19, (), (1, 3, 5, 7, 10, 12, 15, 17, 18), "step_19_ahp_check.txt", "AHP Module check response", branch="ahp_application"),
    StepDefinition(20, "Apply PMS-DISCIPLINE Case Record Stage 1 Artifact Index", 20, ("templates/pms_case_record_stage_1_artifact_index_template.yaml",), tuple(range(1, 20)), "step_20_stage_1_artifact_index.yaml", "Stage 1 Artifact Index output", branch="case_record"),
    StepDefinition(21, "Check PMS-DISCIPLINE Case Record Stage 1 Artifact Index", 21, (), tuple(range(1, 21)), "step_21_stage_1_check.txt", "Stage 1 check response", branch="case_record"),
    StepDefinition(22, "Apply PMS-DISCIPLINE Case Record Stage 2 Layer Digest Extraction", 22, ("templates/pms_case_record_stage_2_layer_digest_extraction_template.yaml",), tuple(range(1, 22)), "step_22_stage_2_layer_digests.yaml", "Stage 2 Layer Digest output", branch="case_record"),
    StepDefinition(23, "Check PMS-DISCIPLINE Case Record Stage 2 Layer Digest Extraction", 23, (), tuple(range(1, 23)), "step_23_stage_2_check.txt", "Stage 2 check response", branch="case_record"),
    StepDefinition(24, "Apply PMS-DISCIPLINE Case Record Stage 3 Full Record Integration", 24, ("templates/pms_case_record_stage_3_full_case_record_integration_template.yaml",), tuple(range(1, 24)), "step_24_stage_3_full_record.yaml", "Stage 3 Full Record output", branch="case_record"),
    StepDefinition(25, "Check PMS-DISCIPLINE Case Record Stage 3 Full Record Integration", 25, (), tuple(range(1, 25)), "step_25_stage_3_check.txt", "Stage 3 check response", branch="case_record"),
    StepDefinition(26, "Article Source Setup and Rendering Contract", 26, (), (1, 3, 5, 7, 10, 12, 15, 17, 19, 21, 23, 25), "step_26_article_rendering_contract.txt", "Article rendering contract confirmation", branch="article"),
    StepDefinition(27, "Base Markdown Case Article Draft", 27, (), (21, 23, 25, 26), "step_27_base_markdown_case_article.md", "Base Markdown article draft", branch="article"),
    StepDefinition(28, "Example Decision and Optional Example Generation", 28, (), (21, 23, 25, 27), "step_28_example_decision_and_examples.md", "Example decision and optional examples", branch="article"),
    StepDefinition(29, "Final Integrated Markdown Case Article", 29, (), (21, 23, 25, 27, 28), "step_29_final_markdown_case_article.md", "Final integrated Markdown article", branch="article"),
    StepDefinition(30, "Final Article Check and Conservative Patch", 30, (), (21, 23, 25, 27, 28, 29), "step_30_final_article_check.md", "Final article check response", branch="article"),
)


AI_REVIEW_STEP_IDS: tuple[int, ...] = (3, 5, 7, 10, 12, 15, 17, 19, 21, 23, 25, 30)


COMPLETED_STEP_STATUSES: tuple[str, ...] = (
    "completed",
    "completed_by_runner_no_examples",
)

NO_EXAMPLE_DECISION_STATES: tuple[str, ...] = (
    "examples_not_applicable",
    "examples_unsafe",
    "examples_not_needed",
    "no_examples",
)

ALL_EXAMPLE_DECISION_STATES: tuple[str, ...] = (
    "examples_not_applicable",
    "examples_unsafe",
    "examples_not_needed",
    "examples_optional",
    "examples_recommended",
    "examples_required_for_readability",
    "no_examples",
)


def is_completed_step_status(status: object) -> bool:
    return str(status) in COMPLETED_STEP_STATUSES

REVIEW_SOURCE_STEP: dict[int, int] = {
    3: 2,
    5: 4,
    7: 6,
    10: 9,
    12: 11,
    15: 14,
    17: 16,
    19: 18,
    21: 20,
    23: 22,
    25: 24,
    30: 29,
}


def is_ai_review_step(step_id: int) -> bool:
    return step_id in AI_REVIEW_STEP_IDS

SUPPORTED_ADDONS: tuple[str, ...] = (
    "ANTICIPATION",
    "CRITIQUE",
    "CONFLICT",
    "LOGIC",
    "EDEN",
    "SEX",
)

MIP_SOURCE_FILENAME = "MIP - Maturity in Practice.yaml"
AHP_SOURCE_FILENAME = "MIP - Maturity in Practice - AHP Module.yaml"


def get_step(step_id: int) -> StepDefinition:
    for step in STEPS:
        if step.step_id == step_id:
            return step
    raise KeyError(f"Unknown step id: {step_id}")


def iter_steps() -> Iterable[StepDefinition]:
    return iter(STEPS)


def resolve_upload_files(step: StepDefinition, project_root: Path, selected_addon: str | None) -> list[Path]:
    values = {
        "SELECTED_ADDON": selected_addon or "SELECTED_ADDON",
        "selected_addon_lower": (selected_addon or "selected_addon").lower(),
    }
    return [project_root / pattern.format(**values) for pattern in step.upload_files]
