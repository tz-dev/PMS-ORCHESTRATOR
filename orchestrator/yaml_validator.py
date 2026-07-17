from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - exercised on systems without PyYAML
    yaml = None


if yaml is not None:
    class _UniqueKeyLoader(yaml.SafeLoader):  # type: ignore[misc,union-attr]
        pass


    def _construct_unique_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
        loader.flatten_mapping(node)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(  # type: ignore[union-attr]
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping


    _UniqueKeyLoader.add_constructor(  # type: ignore[name-defined]
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,  # type: ignore[union-attr]
        _construct_unique_mapping,
    )
else:  # pragma: no cover
    _UniqueKeyLoader = None


_PLACEHOLDER_ENUM = re.compile(r"^\s*<\s*([^<>]*\|[^<>]*)\s*>\s*$")
_PLACEHOLDER_VALUE = re.compile(r"^\s*<.*>\s*$", re.DOTALL)


class YamlValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ValidationIssue:
    category: str
    path: str
    message: str

    def display(self) -> str:
        location = self.path or "<root>"
        return f"[{self.category}] {location}: {self.message}"


@dataclass
class YamlValidationResult:
    step_id: int
    applicable: bool = True
    enabled: bool = True
    dependency_available: bool = True
    syntax_valid: bool = True
    reference_available: bool = False
    reference_path: str | None = None
    validation_profile_step_id: int | None = None
    syntax_error: str | None = None
    note: str | None = None
    empty: bool = False
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def missing_count(self) -> int:
        return sum(issue.category == "missing_key" for issue in self.issues)

    @property
    def unexpected_count(self) -> int:
        return sum(issue.category == "unexpected_key" for issue in self.issues)

    @property
    def type_count(self) -> int:
        return sum(issue.category == "type_mismatch" for issue in self.issues)

    @property
    def invalid_value_count(self) -> int:
        return sum(issue.category == "invalid_value" for issue in self.issues)

    @property
    def structural_issue_count(self) -> int:
        return len(self.issues)

    @property
    def has_blocking_syntax_error(self) -> bool:
        return self.applicable and self.enabled and self.dependency_available and not self.syntax_valid

    @property
    def clean(self) -> bool:
        return self.syntax_valid and not self.issues

    def short_summary(self) -> str:
        if not self.applicable:
            return "YAML validation: Not applicable for this step."
        if not self.enabled:
            return "YAML validation: Off for this case."
        if not self.dependency_available:
            return "YAML validation: Unavailable — PyYAML is not installed."
        if self.empty:
            return "YAML validation: Waiting for YAML output."
        if not self.syntax_valid:
            return f"YAML validation: Invalid syntax · {self.syntax_error or 'parse error'}"
        if not self.reference_available:
            suffix = f" · {self.note}" if self.note else ""
            return f"YAML validation: Syntax valid · structure check unavailable{suffix}"
        if self.clean:
            return "YAML validation: Valid · keys and explicit values match the reference."
        return (
            "YAML validation: Syntax valid"
            f" · {self.missing_count} missing"
            f" · {self.unexpected_count} unexpected"
            f" · {self.type_count} type"
            f" · {self.invalid_value_count} value"
        )

    def detailed_text(self) -> str:
        lines = [self.short_summary()]
        if self.validation_profile_step_id is not None and self.validation_profile_step_id != self.step_id:
            lines.append(f"Validation profile inherited from step #{self.validation_profile_step_id}.")
        if self.reference_path:
            lines.append(f"Reference: {self.reference_path}")
        if self.note:
            lines.append(f"Note: {self.note}")
        if self.syntax_error:
            lines.extend(["", "Syntax error", self.syntax_error])
        if self.issues:
            lines.append("")
            lines.append("Findings")
            for issue in self.issues:
                lines.append(f"- {issue.display()}")
        elif self.syntax_valid and self.reference_available and not self.empty:
            lines.extend(["", "No structural findings."])
        return "\n".join(lines)

    def report_status(self) -> str:
        if not self.applicable:
            return "not_applicable"
        if not self.enabled:
            return "disabled"
        if not self.dependency_available:
            return "unavailable"
        if self.empty:
            return "empty"
        if not self.syntax_valid:
            return "syntax_error"
        if self.issues:
            return "findings"
        if self.reference_available:
            return "clean"
        return "syntax_only"

    def to_report_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "status": self.report_status(),
            "applicable": self.applicable,
            "enabled": self.enabled,
            "dependency_available": self.dependency_available,
            "syntax_valid": self.syntax_valid,
            "reference_available": self.reference_available,
            "reference_path": self.reference_path,
            "validation_profile_step_id": self.validation_profile_step_id,
            "syntax_error": self.syntax_error,
            "note": self.note,
            "empty": self.empty,
            "summary": self.short_summary(),
            "counts": {
                "missing_keys": self.missing_count,
                "unexpected_keys": self.unexpected_count,
                "type_mismatches": self.type_count,
                "invalid_values": self.invalid_value_count,
                "total_findings": self.structural_issue_count,
            },
            "issues": [
                {
                    "category": issue.category,
                    "path": issue.path,
                    "message": issue.message,
                }
                for issue in self.issues
            ],
        }


class YamlValidationManifest:
    def __init__(self, path: Path, project_root: Path) -> None:
        self.path = path
        self.project_root = project_root
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except FileNotFoundError as exc:
            raise YamlValidationError(f"YAML validation manifest not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise YamlValidationError(f"Invalid JSON in YAML validation manifest: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("steps"), dict):
            raise YamlValidationError("YAML validation manifest must contain a 'steps' object.")
        self.data = data

    def step_config(self, step_id: int, selected_addon: str | None) -> dict[str, Any] | None:
        raw = self.data["steps"].get(str(step_id))
        if not isinstance(raw, dict):
            return None
        config = dict(raw)
        reference = config.get("reference")
        if isinstance(reference, str):
            values = {
                "SELECTED_ADDON": selected_addon or "SELECTED_ADDON",
                "selected_addon_lower": (selected_addon or "selected_addon").lower(),
            }
            config["reference"] = reference.format(**values)
        return config


class LocalYamlValidator:
    def __init__(self, project_root: Path, manifest_path: Path) -> None:
        self.project_root = project_root
        self.manifest_path = manifest_path
        self._manifest: YamlValidationManifest | None = None
        self._manifest_error: str | None = None
        try:
            self._manifest = YamlValidationManifest(manifest_path, project_root)
        except YamlValidationError as exc:
            self._manifest_error = str(exc)

    @property
    def dependency_available(self) -> bool:
        return yaml is not None

    def has_profile(self, step_id: int, selected_addon: str | None) -> bool:
        if self._manifest is None:
            return False
        return self._manifest.step_config(step_id, selected_addon) is not None

    def is_complete_yaml_mapping_or_sequence(self, text: str) -> bool:
        """Return True only for one complete YAML mapping or sequence document."""
        value = self._load_yaml_document_or_none(text)
        return isinstance(value, (dict, list))

    def extract_profile_yaml(
        self,
        text: str,
        profile_step_id: int,
        selected_addon: str | None,
    ) -> str | None:
        """Extract one unambiguous corrected YAML document for a review step.

        A review response may be either the complete corrected YAML document or a
        semantic review report containing exactly one fenced ``yaml``/``yml``
        block whose top-level root matches the reviewed source profile. Arbitrary
        prose that merely resembles YAML is never accepted. Multiple matching
        blocks are rejected as ambiguous.
        """
        expected = self.expected_root_keys(profile_step_id, selected_addon)
        if not expected:
            return None

        normalized = self._unwrap_single_code_fence(text)
        output_data = self._load_yaml_document_or_none(normalized)
        if isinstance(output_data, dict) and tuple(output_data.keys()) == expected:
            return normalized.strip()

        fenced_blocks = [
            match.group(1).strip()
            for match in re.finditer(
                r"```(?:yaml|yml)\s*\n(.*?)\n```",
                text,
                flags=re.IGNORECASE | re.DOTALL,
            )
        ]
        if len(fenced_blocks) != 1:
            return None
        candidate = fenced_blocks[0]
        candidate_data = self._load_yaml_document_or_none(candidate)
        if isinstance(candidate_data, dict) and tuple(candidate_data.keys()) == expected:
            return candidate
        return None

    def output_matches_profile_root(self, text: str, profile_step_id: int, selected_addon: str | None) -> bool:
        """Return True when one unambiguous corrected YAML document is present."""
        return self.extract_profile_yaml(text, profile_step_id, selected_addon) is not None

    def expected_root_keys(self, profile_step_id: int, selected_addon: str | None) -> tuple[str, ...]:
        if self._manifest is None:
            return ()
        config = self._manifest.step_config(profile_step_id, selected_addon)
        if not config:
            return ()
        reference_root_key = str(config.get("reference_root_key") or "").strip()
        if reference_root_key:
            return (reference_root_key,)
        reference_value = config.get("reference")
        if not reference_value:
            return ()
        reference_path = self.project_root / str(reference_value)
        if not reference_path.is_file() or yaml is None:
            return ()
        try:
            reference_data = yaml.load(reference_path.read_text(encoding="utf-8-sig"), Loader=_UniqueKeyLoader)
        except (OSError, yaml.YAMLError):  # type: ignore[union-attr]
            return ()
        reference_subpath = str(config.get("reference_subpath") or "").strip()
        if reference_subpath:
            found, reference_data = self._value_at_exact_path(reference_data, reference_subpath)
            if not found:
                return ()
        if isinstance(reference_data, dict):
            return tuple(str(key) for key in reference_data.keys())
        return ()

    @staticmethod
    def _load_yaml_document_or_none(text: str) -> Any | None:
        if yaml is None or not text.strip():
            return None
        normalized_text = LocalYamlValidator._unwrap_single_code_fence(text)
        try:
            return yaml.load(normalized_text, Loader=_UniqueKeyLoader)
        except yaml.YAMLError:  # type: ignore[union-attr]
            return None

    def validate(
        self,
        *,
        step_id: int,
        text: str,
        expects_yaml: bool,
        enabled: bool,
        selected_addon: str | None,
        profile_step_id: int | None = None,
    ) -> YamlValidationResult:
        effective_profile_step_id = step_id if profile_step_id is None else profile_step_id
        result = YamlValidationResult(
            step_id=step_id,
            applicable=expects_yaml,
            enabled=enabled,
            validation_profile_step_id=effective_profile_step_id if expects_yaml else None,
        )
        if not expects_yaml or not enabled:
            return result
        if yaml is None:
            result.dependency_available = False
            return result
        if self._manifest_error:
            result.note = self._manifest_error
        if not text.strip():
            result.empty = True
            return result

        normalized_text = self._unwrap_single_code_fence(text)
        try:
            output_data = yaml.load(normalized_text, Loader=_UniqueKeyLoader)
        except yaml.YAMLError as exc:  # type: ignore[union-attr]
            result.syntax_valid = False
            result.syntax_error = self._format_yaml_error(exc)
            return result

        config = self._manifest.step_config(effective_profile_step_id, selected_addon) if self._manifest else None
        if not config:
            result.note = result.note or "No validation profile is configured for this step."
            return result

        result.note = str(config.get("note") or result.note or "") or None
        reference_value = config.get("reference")
        if not reference_value or not bool(config.get("compare_keys", True)):
            result.note = result.note or "This profile performs syntax validation only."
            return result

        reference_path = self.project_root / str(reference_value)
        reference_subpath = str(config.get("reference_subpath") or "").strip()
        reference_root_key = str(config.get("reference_root_key") or "").strip()
        result.reference_path = str(reference_value) + (f"#{reference_subpath}" if reference_subpath else "")
        if not reference_path.is_file():
            result.note = f"Reference file is missing: {reference_value}"
            return result

        try:
            reference_data = yaml.load(reference_path.read_text(encoding="utf-8-sig"), Loader=_UniqueKeyLoader)
        except (OSError, yaml.YAMLError) as exc:  # type: ignore[union-attr]
            result.note = f"Reference YAML could not be loaded: {exc}"
            return result

        if reference_subpath:
            found, reference_data = self._value_at_exact_path(reference_data, reference_subpath)
            if not found:
                result.note = f"Reference subpath is missing: {reference_subpath}"
                return result
        if reference_root_key:
            reference_data = {reference_root_key: reference_data}

        result.reference_available = True
        optional_paths = tuple(str(item) for item in config.get("optional_paths", []))
        allow_extra_paths = tuple(str(item) for item in config.get("allow_extra_paths", []))
        allow_extra_keys = bool(config.get("allow_extra_keys", False))
        compare_scalar_types = bool(config.get("compare_scalar_types", False))
        extract_enums = bool(config.get("extract_placeholder_enums", True))

        self._compare_nodes(
            reference_data,
            output_data,
            path="",
            issues=result.issues,
            optional_paths=optional_paths,
            allow_extra_paths=allow_extra_paths,
            allow_extra_keys=allow_extra_keys,
            compare_scalar_types=compare_scalar_types,
            extract_enums=extract_enums,
        )
        self._apply_explicit_rules(config.get("rules", []), output_data, result.issues)
        return result

    @staticmethod
    def _unwrap_single_code_fence(text: str) -> str:
        stripped = text.strip()
        match = re.fullmatch(r"```(?:yaml|yml)?\s*\n(.*)\n```", stripped, flags=re.IGNORECASE | re.DOTALL)
        return match.group(1) if match else text

    @staticmethod
    def _format_yaml_error(exc: Exception) -> str:
        mark = getattr(exc, "problem_mark", None)
        problem = getattr(exc, "problem", None)
        if mark is not None:
            return f"line {mark.line + 1}, column {mark.column + 1}: {problem or str(exc)}"
        return str(exc)

    @staticmethod
    def _path_matches(path: str, patterns: Iterable[str]) -> bool:
        return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)

    @staticmethod
    def _child_path(path: str, key: object) -> str:
        return f"{path}.{key}" if path else str(key)

    def _compare_nodes(
        self,
        reference: Any,
        output: Any,
        *,
        path: str,
        issues: list[ValidationIssue],
        optional_paths: tuple[str, ...],
        allow_extra_paths: tuple[str, ...],
        allow_extra_keys: bool,
        compare_scalar_types: bool,
        extract_enums: bool,
    ) -> None:
        if isinstance(reference, dict):
            if not isinstance(output, dict):
                issues.append(ValidationIssue("type_mismatch", path, f"expected mapping, got {type(output).__name__}"))
                return
            for key, reference_value in reference.items():
                child = self._child_path(path, key)
                if key not in output:
                    if not self._path_matches(child, optional_paths):
                        issues.append(ValidationIssue("missing_key", child, "key is present in the supplied reference YAML"))
                    continue
                self._compare_nodes(
                    reference_value,
                    output[key],
                    path=child,
                    issues=issues,
                    optional_paths=optional_paths,
                    allow_extra_paths=allow_extra_paths,
                    allow_extra_keys=allow_extra_keys,
                    compare_scalar_types=compare_scalar_types,
                    extract_enums=extract_enums,
                )
            if not allow_extra_keys:
                for key in output:
                    if key in reference:
                        continue
                    child = self._child_path(path, key)
                    if not self._path_matches(child, allow_extra_paths):
                        issues.append(ValidationIssue("unexpected_key", child, "key is not present in the supplied reference YAML"))
            return

        if isinstance(reference, list):
            if not isinstance(output, list):
                issues.append(ValidationIssue("type_mismatch", path, f"expected list, got {type(output).__name__}"))
                return
            if reference and isinstance(reference[0], (dict, list)):
                for index, item in enumerate(output):
                    item_path = f"{path}.*" if path else "*"
                    self._compare_nodes(
                        reference[0],
                        item,
                        path=item_path,
                        issues=issues,
                        optional_paths=optional_paths,
                        allow_extra_paths=allow_extra_paths,
                        allow_extra_keys=allow_extra_keys,
                        compare_scalar_types=compare_scalar_types,
                        extract_enums=extract_enums,
                    )
            return

        if extract_enums:
            allowed = self._enum_values(reference)
            if allowed is not None and not self._value_matches_allowed(output, allowed):
                issues.append(
                    ValidationIssue(
                        "invalid_value",
                        path,
                        f"value {output!r} is not one of: {', '.join(repr(item) for item in allowed)}",
                    )
                )
                return

        if compare_scalar_types and reference is not None and not self._is_placeholder(reference):
            if type(reference) is not type(output):
                issues.append(
                    ValidationIssue(
                        "type_mismatch",
                        path,
                        f"expected {type(reference).__name__}, got {type(output).__name__}",
                    )
                )

    @staticmethod
    def _is_placeholder(value: Any) -> bool:
        return isinstance(value, str) and bool(_PLACEHOLDER_VALUE.match(value))

    @staticmethod
    def _enum_values(reference: Any) -> tuple[Any, ...] | None:
        if not isinstance(reference, str):
            return None
        match = _PLACEHOLDER_ENUM.match(reference)
        if not match:
            return None
        values = tuple(part.strip() for part in match.group(1).split("|") if part.strip())
        # Meta-placeholders describe a selection rule rather than a literal
        # enum. Their exact allowed values belong in an explicit manifest rule.
        if any(value.lower().startswith("exactly_one_of:") for value in values):
            return None
        return values or None


    @staticmethod
    def _canonical_scalar(value: Any) -> tuple[str, str]:
        """Normalize YAML 1.1 booleans/nulls for enum comparison.

        PyYAML resolves unquoted ``yes``/``no`` and ``true``/``false`` to
        booleans. A template enum is textual, so compare those spellings by
        semantic scalar value rather than reporting a false invalid-value
        finding.
        """
        if value is True:
            return ("bool", "true")
        if value is False:
            return ("bool", "false")
        if value is None:
            return ("null", "null")
        if isinstance(value, str):
            token = value.strip().lower()
            if token in {"true", "yes", "on"}:
                return ("bool", "true")
            if token in {"false", "no", "off"}:
                return ("bool", "false")
            if token in {"null", "~"}:
                return ("null", "null")
            if re.fullmatch(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", token):
                try:
                    number = float(token)
                except ValueError:
                    pass
                else:
                    return ("number", str(int(number)) if number.is_integer() else str(number))
            return ("str", value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            number = float(value)
            return ("number", str(int(number)) if number.is_integer() else str(number))
        return (type(value).__name__, repr(value))

    @classmethod
    def _value_matches_allowed(cls, value: Any, allowed: tuple[Any, ...]) -> bool:
        canonical = cls._canonical_scalar(value)
        return any(canonical == cls._canonical_scalar(candidate) for candidate in allowed)

    def _apply_explicit_rules(self, rules: Any, output_data: Any, issues: list[ValidationIssue]) -> None:
        if not isinstance(rules, list):
            return
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            path = str(rule.get("path", ""))
            allowed = rule.get("allowed_values")
            if not path or not isinstance(allowed, list):
                continue
            for actual_path, value in self._values_at_path(output_data, path):
                if not self._value_matches_allowed(value, tuple(allowed)):
                    issues.append(
                        ValidationIssue(
                            "invalid_value",
                            actual_path,
                            f"value {value!r} is not one of: {', '.join(repr(item) for item in allowed)}",
                        )
                    )

    @staticmethod
    def _value_at_exact_path(data: Any, path: str) -> tuple[bool, Any]:
        current = data
        for part in path.split(".") if path else ():
            if not isinstance(current, dict) or part not in current:
                return False, None
            current = current[part]
        return True, current

    def _values_at_path(self, data: Any, path: str) -> list[tuple[str, Any]]:
        parts = path.split(".") if path else []
        current: list[tuple[str, Any]] = [("", data)]
        for part in parts:
            next_values: list[tuple[str, Any]] = []
            for current_path, value in current:
                if part == "*" and isinstance(value, list):
                    for item in value:
                        next_path = f"{current_path}.*" if current_path else "*"
                        next_values.append((next_path, item))
                elif isinstance(value, dict) and part in value:
                    next_path = self._child_path(current_path, part)
                    next_values.append((next_path, value[part]))
            current = next_values
        return current
