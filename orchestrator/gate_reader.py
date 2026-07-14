from __future__ import annotations

import re
from dataclasses import dataclass

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
