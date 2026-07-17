from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .registry import SUPPORTED_ADDONS


@dataclass(frozen=True)
class GateValue:
    value: str | None
    status: str
    key_path: str
    raw_value: str | None = None
    source_step: int | None = None

    @property
    def display_value(self) -> str:
        return self.value if self.value is not None else "NULL"


@dataclass(frozen=True)
class MipGateDetails:
    overall: GateValue
    source_read: GateValue
    case_application: GateValue


@dataclass(frozen=True)
class PreAnalysisDisposition:
    pipeline_case_disposition: GateValue
    final_pipeline_case_disposition: GateValue
    final_status: GateValue
    final_next_allowed_step: GateValue
    requested_output_disposition: GateValue
    hard_gate_status: GateValue
    hard_gate_effect: GateValue
    input_strength: GateValue
    whole_person_claim: GateValue
    motive_claim: GateValue
    person_nearness_level: GateValue
    irreversibility_level: GateValue
    requested_output_entry_condition_status: GateValue

    @property
    def explicit_stop_signal(self) -> GateValue | None:
        candidates = (
            (self.pipeline_case_disposition, "stop"),
            (self.final_pipeline_case_disposition, "stop"),
            (self.final_status, "stop_before_core"),
            (self.final_next_allowed_step, "stop"),
        )
        for field, stop_value in candidates:
            if field.status == "found" and field.value == stop_value:
                return field
        return None

    @property
    def explicit_pipeline_stop(self) -> bool:
        return self.explicit_stop_signal is not None

    @property
    def mandatory_person_near_stop(self) -> bool:
        prohibited_person_output = (
            self.whole_person_claim.value == "not_allowed"
            or self.motive_claim.value == "not_allowed"
        )
        return (
            self.requested_output_disposition.value == "refuse"
            and self.hard_gate_status.value == "triggered"
            and prohibited_person_output
            and self.input_strength.value in {"minimal", "low", "insufficient"}
            and self.person_nearness_level.value in {"high", "severe"}
            and self.irreversibility_level.value in {"high", "severe"}
            and self.requested_output_entry_condition_status.value == "not_satisfied"
        )

    @property
    def is_pipeline_stop(self) -> bool:
        return self.explicit_pipeline_stop or self.mandatory_person_near_stop

    @property
    def stop_reason(self) -> str | None:
        if self.explicit_pipeline_stop:
            return "pipeline_case_disposition_stop"
        if self.mandatory_person_near_stop:
            return "mandatory_person_near_hard_stop"
        return None


def _clean_scalar(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def _find_nested_scalar(text: str, parent_key: str, child_key: str) -> str | None:
    parent_pattern = re.compile(rf"^(?P<indent>\s*){re.escape(parent_key)}\s*:\s*(?:#.*)?$")
    child_pattern = re.compile(rf"^\s+{re.escape(child_key)}\s*:\s*(?P<value>.*)$")
    inside = False
    parent_indent: int | None = None
    for line in text.splitlines():
        match = parent_pattern.match(line)
        if match:
            parent_indent = len(match.group("indent").replace("\t", "    "))
            inside = True
            continue
        if not inside:
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        current_indent = len(line) - len(line.lstrip(" \t"))
        if parent_indent is not None and current_indent <= parent_indent:
            inside = False
            match = parent_pattern.match(line)
            if match:
                parent_indent = len(match.group("indent").replace("\t", "    "))
                inside = True
            continue
        child = child_pattern.match(line)
        if child:
            return _clean_scalar(child.group("value"))
    return None


def _read_pre_analysis_scalar(
    text: str,
    parent_key: str,
    child_key: str,
    source_step: int | None = None,
) -> GateValue:
    key_path = f"{parent_key}.{child_key}"
    raw = _find_nested_scalar(text, parent_key, child_key)
    if raw is None:
        return GateValue(None, "key_not_found", key_path, source_step=source_step)
    normalized = raw.lower()
    if normalized in {"unclear", "unknown", "missing", "unresolved", ""} or "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", key_path, raw, source_step)
    return GateValue(normalized, "found", key_path, raw, source_step)


def _read_pre_analysis_disposition_field(
    text: str,
    child_key: str,
    source_step: int | None = None,
) -> GateValue:
    return _read_pre_analysis_scalar(
        text, "scope_and_pipeline_disposition", child_key, source_step
    )


def read_pre_analysis_disposition(
    text: str,
    source_step: int | None = None,
) -> PreAnalysisDisposition:
    """Read the authoritative Pre-Analysis scope and pipeline disposition fields."""
    return PreAnalysisDisposition(
        pipeline_case_disposition=_read_pre_analysis_disposition_field(
            text, "pipeline_case_disposition", source_step
        ),
        final_pipeline_case_disposition=_read_pre_analysis_scalar(
            text, "final_pre_analysis_status", "pipeline_case_disposition", source_step
        ),
        final_status=_read_pre_analysis_scalar(
            text, "final_pre_analysis_status", "status", source_step
        ),
        final_next_allowed_step=_read_pre_analysis_scalar(
            text, "final_pre_analysis_status", "next_allowed_step", source_step
        ),
        requested_output_disposition=_read_pre_analysis_disposition_field(
            text, "requested_output_disposition", source_step
        ),
        hard_gate_status=_read_pre_analysis_disposition_field(
            text, "hard_gate_status", source_step
        ),
        hard_gate_effect=_read_pre_analysis_disposition_field(
            text, "hard_gate_effect", source_step
        ),
        input_strength=_read_pre_analysis_scalar(
            text, "input_status_discipline", "input_strength", source_step
        ),
        whole_person_claim=_read_pre_analysis_scalar(
            text, "scope_boundary_matrix", "whole_person_claim", source_step
        ),
        motive_claim=_read_pre_analysis_scalar(
            text, "scope_boundary_matrix", "motive_claim", source_step
        ),
        person_nearness_level=_read_pre_analysis_scalar(
            text, "person_nearness_publicness_irreversibility", "person_nearness_level", source_step
        ),
        irreversibility_level=_read_pre_analysis_scalar(
            text, "person_nearness_publicness_irreversibility", "irreversibility_level", source_step
        ),
        requested_output_entry_condition_status=_read_pre_analysis_scalar(
            text, "pms_entry_condition_precheck", "requested_output_entry_condition_status", source_step
        ),
    )


def read_addon_recommendation(text: str, source_step: int | None = None) -> GateValue:
    raw = _find_nested_scalar(text, "gate_result", "selected_addon")
    if raw is None:
        return GateValue(None, "key_not_found", "gate_result.selected_addon", source_step=source_step)
    normalized = raw.upper()
    if normalized in SUPPORTED_ADDONS:
        return GateValue(normalized, "supported_addon", "gate_result.selected_addon", raw, source_step)
    if normalized in {"NONE", "NULL", "~", "NO_ADDON", "CORE_ONLY"}:
        return GateValue(None, "no_addon", "gate_result.selected_addon", raw, source_step)
    if normalized in {"UNCLEAR", "UNKNOWN", "MISSING", "UNRESOLVED", ""} or "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", "gate_result.selected_addon", raw, source_step)
    return GateValue(None, "unsupported_value", "gate_result.selected_addon", raw, source_step)


def read_addon_gate_status(text: str, source_step: int | None = None) -> GateValue:
    raw = _find_nested_scalar(text, "gate_result", "gate_status")
    if raw is None:
        return GateValue(None, "key_not_found", "gate_result.gate_status", source_step=source_step)
    if "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", "gate_result.gate_status", raw, source_step)
    return GateValue(raw, "found", "gate_result.gate_status", raw, source_step)


def read_mip_recommendation(text: str, source_step: int | None = None) -> GateValue:
    raw = _find_nested_scalar(text, "mip_recommendation_output", "recommendation_status")
    if raw is None:
        return GateValue(None, "key_not_found", "mip_recommendation_output.recommendation_status", source_step=source_step)
    normalized = raw.lower()
    if normalized in {"recommended", "recommended_with_limits"}:
        return GateValue("MIP", "recommended", "mip_recommendation_output.recommendation_status", raw, source_step)
    if normalized in {"not_recommended", "scan_only"}:
        return GateValue(None, normalized, "mip_recommendation_output.recommendation_status", raw, source_step)
    if normalized in {"unclear", "unknown", "missing", "unresolved", ""} or "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", "mip_recommendation_output.recommendation_status", raw, source_step)
    return GateValue(None, normalized, "mip_recommendation_output.recommendation_status", raw, source_step)


def _read_mip_nested_recommendation(
    text: str,
    parent_key: str,
    key_path: str,
    source_step: int | None = None,
) -> GateValue:
    raw = _find_nested_scalar(text, parent_key, "status")
    if raw is None:
        return GateValue(None, "key_not_found", key_path, source_step=source_step)
    normalized = raw.lower()
    if normalized in {"unclear", "unknown", "missing", "unresolved", ""} or "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", key_path, raw, source_step)
    return GateValue(raw, "found", key_path, raw, source_step)


def read_mip_gate_details(text: str, source_step: int | None = None) -> MipGateDetails:
    """Read all three MIP Gate decision fields without changing binary runner routing."""
    return MipGateDetails(
        overall=read_mip_recommendation(text, source_step=source_step),
        source_read=_read_mip_nested_recommendation(
            text,
            "MIP_source_read_recommendation",
            "mip_recommendation_output.MIP_source_read_recommendation.status",
            source_step,
        ),
        case_application=_read_mip_nested_recommendation(
            text,
            "MIP_case_application_recommendation",
            "mip_recommendation_output.MIP_case_application_recommendation.status",
            source_step,
        ),
    )


def read_first_mip_gate_details(candidates: Iterable[tuple[int, str]]) -> MipGateDetails:
    """Prefer the first candidate containing the overall MIP decision, with fallback metadata."""
    fallback: MipGateDetails | None = None
    for source_step, text in candidates:
        if not text.strip():
            continue
        details = read_mip_gate_details(text, source_step=source_step)
        fallback = details
        if details.overall.status != "key_not_found":
            return details
    return fallback or read_mip_gate_details("")


def read_ahp_recommendation(text: str, source_step: int | None = None) -> GateValue:
    raw = _find_nested_scalar(text, "gate_result", "gate_status")
    if raw is None:
        return GateValue(None, "key_not_found", "gate_result.gate_status", source_step=source_step)
    normalized = raw.lower()
    if normalized == "ahp_source_reading_recommended":
        return GateValue("AHP", "recommended", "gate_result.gate_status", raw, source_step)
    if normalized in {"ahp_not_recommended", "scan_only"}:
        return GateValue(None, normalized, "gate_result.gate_status", raw, source_step)
    if normalized in {"unclear", "unknown", "missing", "unresolved", ""} or "<" in raw or ">" in raw:
        return GateValue(None, "unresolved", "gate_result.gate_status", raw, source_step)
    return GateValue(None, normalized, "gate_result.gate_status", raw, source_step)
