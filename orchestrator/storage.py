from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .registry import (
    AI_REVIEW_STEP_IDS,
    ALL_EXAMPLE_DECISION_STATES,
    COMPLETED_STEP_STATUSES,
    NO_EXAMPLE_DECISION_STATES,
    REVIEW_SOURCE_STEP,
    STEPS,
    get_step,
    is_ai_review_step,
    is_completed_step_status,
)


class StorageError(RuntimeError):
    pass


DEFAULT_AI_REVIEW_STEPS_ENABLED = True
DEFAULT_LOCAL_YAML_VALIDATION_ENABLED = True
DEFAULT_YAML_VALIDATION_BEHAVIOR = "warn"
VALID_YAML_VALIDATION_BEHAVIORS = {"warn", "block"}
YAML_VALIDATION_REPORT_SCHEMA = "PMS_ORCHESTRATOR_YAML_VALIDATION_1.3"
ARTICLE_PROFILE_CASE = "case_article"
ARTICLE_PROFILE_FULL = "full_analysis_article"
VALID_ARTICLE_PROFILES = {ARTICLE_PROFILE_CASE, ARTICLE_PROFILE_FULL}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-").lower()
    return cleaned[:48] or "case"


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StorageError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StorageError(f"Invalid JSON in {path}: {exc}") from exc


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def _initial_status(step_id: int) -> str:
    if step_id == 1:
        return "current"
    if get_step(step_id).branch in {"selected_addon", "mip", "ahp", "ahp_application", "case_record", "iteration", "article"}:
        return "locked"
    return "open"


def _new_step_state(step_id: int, status: str | None = None) -> dict[str, Any]:
    step = get_step(step_id)
    return {
        "title": step.title,
        "status": status or _initial_status(step_id),
        "prompt_file": None,
        "output_file": None,
        "last_saved_at": None,
        "completed_at": None,
        "yaml_validation_file": None,
        "yaml_validation_status": None,
        "yaml_validation_issue_count": 0,
        "yaml_validation_handoff_target_step": None,
        "yaml_validation_resolved_by_step": None,
        "runner_completion_mode": None,
        "example_decision_state": None,
    }


def _route_signature(route: dict[str, Any] | None, fields: Iterable[str]) -> tuple[Any, ...] | None:
    if not route:
        return None
    return tuple(route.get(field) for field in fields)


def _article_route_signature(route: dict[str, Any] | None) -> tuple[Any, ...] | None:
    if not route:
        return None
    route_type = route.get("route_type")
    profile = route.get("article_profile")
    if route_type == "generate_article" and profile not in VALID_ARTICLE_PROFILES:
        profile = ARTICLE_PROFILE_FULL
    if route_type != "generate_article":
        profile = None
    return route_type, profile


@dataclass
class CaseSession:
    project_root: Path
    case_dir: Path
    case_data: dict[str, Any]
    session_data: dict[str, Any]

    @property
    def case_id(self) -> str:
        return str(self.case_data["case_id"])

    @property
    def selected_addon(self) -> str | None:
        route = self.session_data.get("route") or {}
        value = route.get("selected_addon")
        return str(value) if value else None

    @property
    def article_profile(self) -> str:
        route = self.session_data.get("article_route") or {}
        if route.get("route_type") != "generate_article":
            return ARTICLE_PROFILE_FULL
        value = str(route.get("article_profile") or ARTICLE_PROFILE_FULL)
        return value if value in VALID_ARTICLE_PROFILES else ARTICLE_PROFILE_FULL

    @property
    def ai_review_steps_enabled(self) -> bool:
        return bool(self.case_data.get("ai_review_steps_enabled", DEFAULT_AI_REVIEW_STEPS_ENABLED))

    @property
    def local_yaml_validation_enabled(self) -> bool:
        return bool(self.case_data.get("local_yaml_validation_enabled", DEFAULT_LOCAL_YAML_VALIDATION_ENABLED))

    @property
    def yaml_validation_behavior(self) -> str:
        value = str(self.case_data.get("yaml_validation_behavior", DEFAULT_YAML_VALIDATION_BEHAVIOR))
        return value if value in VALID_YAML_VALIDATION_BEHAVIORS else DEFAULT_YAML_VALIDATION_BEHAVIOR

    def required_route_step(self, route_name: str) -> int:
        mapping = {
            "addon": (7, 6, "route"),
            "mip": (12, 11, "mip_route"),
            "ahp": (17, 16, "ahp_route"),
            "article": (26, 26, "article_route"),
        }
        try:
            checked_step, unchecked_step, route_field = mapping[route_name]
        except KeyError as exc:
            raise StorageError(f"Unknown route name: {route_name}") from exc
        if not self.ai_review_steps_enabled:
            return unchecked_step
        if self.step_state(checked_step).get("status") == "completed":
            return checked_step
        # A case may enable reviews only after an earlier unchecked route was
        # already confirmed. Past skipped checks remain skipped by design; the
        # saved route must still be reviewable without pretending it was checked.
        if (
            self.session_data.get(route_field)
            and self.step_state(checked_step).get("status") == "skipped"
            and self.step_state(unchecked_step).get("status") == "completed"
        ):
            return unchecked_step
        return checked_step

    def route_ready(self, route_name: str) -> bool:
        return self.step_state(self.required_route_step(route_name)).get("status") == "completed"

    @property
    def case_json_path(self) -> Path:
        return self.case_dir / "case.json"

    @property
    def session_json_path(self) -> Path:
        return self.case_dir / "session.json"

    @property
    def prompts_dir(self) -> Path:
        return self.case_dir / "prompts"

    @property
    def outputs_dir(self) -> Path:
        return self.case_dir / "outputs"

    @property
    def exchanges_dir(self) -> Path:
        return self.case_dir / "exchanges"

    @property
    def history_dir(self) -> Path:
        return self.case_dir / "history" / "route_revisions"

    @property
    def validation_dir(self) -> Path:
        return self.case_dir / "validation"

    def validation_report_path(self, step_id: int) -> Path:
        return self.validation_dir / f"step_{step_id:02d}_yaml_validation.json"

    def save(self) -> None:
        self.case_data["updated_at"] = utc_now()
        self.session_data["updated_at"] = utc_now()
        _write_json(self.case_json_path, self.case_data)
        _write_json(self.session_json_path, self.session_data)

    def step_state(self, step_id: int) -> dict[str, Any]:
        try:
            return self.session_data["steps"][str(step_id)]
        except KeyError as exc:
            raise StorageError(f"Missing state for step #{step_id}.") from exc

    def current_step_id(self) -> int | None:
        current = self.session_data.get("current_step")
        return int(current) if current is not None else None

    def prompt_path(self, step_id: int) -> Path:
        return self.prompts_dir / f"step_{step_id:02d}_prompt.txt"

    def output_path(self, step_id: int) -> Path:
        return self.outputs_dir / get_step(step_id).output_filename

    def write_prompt(self, step_id: int, text: str, overwrite: bool = False) -> Path:
        path = self.prompt_path(step_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not path.exists():
            path.write_text(text, encoding="utf-8")
        self.step_state(step_id)["prompt_file"] = str(path.relative_to(self.case_dir))
        self.save()
        return path

    def invalidate_prompt(self, step_id: int) -> None:
        path = self.prompt_path(step_id)
        if path.exists():
            path.unlink()
        self.step_state(step_id)["prompt_file"] = None
        self.save()

    def write_output(self, step_id: int, text: str, complete: bool = False) -> Path:
        path = self.output_path(step_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        state = self.step_state(step_id)
        state["output_file"] = str(path.relative_to(self.case_dir))
        state["last_saved_at"] = utc_now()
        if complete:
            self.complete_step(step_id)
        else:
            if state["status"] in {"open", "current"}:
                state["status"] = "draft" if self.current_step_id() != step_id else "current"
            self.save()
        return path

    def load_yaml_validation_report(self, step_id: int) -> dict[str, Any] | None:
        path = self.validation_report_path(step_id)
        if not path.is_file():
            return None
        try:
            data = _read_json(path)
        except StorageError:
            return None
        return data if isinstance(data, dict) else None

    def save_yaml_validation_report(
        self,
        step_id: int,
        report: dict[str, Any],
        *,
        completion_state: str,
    ) -> Path:
        path = self.validation_report_path(step_id)
        existing = self.load_yaml_validation_report(step_id) or {}
        status = str(report.get("status") or "unknown")
        issue_count = int((report.get("counts") or {}).get("total_findings") or 0)
        if status == "syntax_error":
            issue_count = max(1, issue_count)
        unresolved_status = status in {"findings", "syntax_error"}
        handoff_target = existing.get("handoff_target_step") if unresolved_status and issue_count > 0 else None
        resolved_by_step = existing.get("resolved_by_step") if unresolved_status and issue_count > 0 else None
        resolved_at = existing.get("resolved_at") if resolved_by_step is not None else None
        now = utc_now()
        output_path = self.output_path(step_id)
        data = {
            "schema_version": YAML_VALIDATION_REPORT_SCHEMA,
            **report,
            "step_id": step_id,
            "source_output": str(output_path.relative_to(self.case_dir)),
            "completion_state": completion_state,
            "handoff_target_step": handoff_target,
            "resolved_by_step": resolved_by_step,
            "resolved_at": resolved_at,
            "created_at": existing.get("created_at") or now,
            "updated_at": now,
        }
        _write_json(path, data)
        state = self.step_state(step_id)
        state["yaml_validation_file"] = str(path.relative_to(self.case_dir))
        state["yaml_validation_status"] = status
        state["yaml_validation_issue_count"] = issue_count
        state["yaml_validation_handoff_target_step"] = handoff_target
        state["yaml_validation_resolved_by_step"] = resolved_by_step

        profile_step_id = report.get("validation_profile_step_id")
        if (
            completion_state == "completed"
            and status == "clean"
            and step_id in REVIEW_SOURCE_STEP
            and int(profile_step_id or 0) == REVIEW_SOURCE_STEP[step_id]
        ):
            self._resolve_yaml_findings_from_review(step_id)

        self.save()
        return path

    def step_has_yaml_findings(self, step_id: int) -> bool:
        state = self.step_state(step_id)
        return (
            state.get("yaml_validation_status") in {"findings", "syntax_error"}
            and int(state.get("yaml_validation_issue_count") or 0) > 0
        )

    def step_has_unresolved_yaml_findings(self, step_id: int) -> bool:
        if not self.step_has_yaml_findings(step_id):
            return False
        report = self.load_yaml_validation_report(step_id)
        return bool(report) and report.get("resolved_by_step") is None

    def yaml_findings_resolution(self, step_id: int) -> int | None:
        report = self.load_yaml_validation_report(step_id)
        if not report or report.get("resolved_by_step") is None:
            return None
        try:
            return int(report["resolved_by_step"])
        except (TypeError, ValueError):
            return None

    def _resolve_yaml_findings_from_review(self, review_step_id: int) -> bool:
        source_step_id = REVIEW_SOURCE_STEP.get(review_step_id)
        if source_step_id is None:
            return False
        report = self.load_yaml_validation_report(source_step_id)
        if not report or str(report.get("status")) not in {"findings", "syntax_error"}:
            return False
        if int((report.get("counts") or {}).get("total_findings") or 0) <= 0 and not report.get("syntax_error"):
            return False
        target = report.get("handoff_target_step")
        if target is not None and int(target) != review_step_id:
            return False
        report["handoff_target_step"] = review_step_id
        report["resolved_by_step"] = review_step_id
        report["resolved_at"] = utc_now()
        report["updated_at"] = utc_now()
        _write_json(self.validation_report_path(source_step_id), report)
        state = self.step_state(source_step_id)
        state["yaml_validation_handoff_target_step"] = review_step_id
        state["yaml_validation_resolved_by_step"] = review_step_id
        return True

    def claim_yaml_validation_handoffs(self, target_step_id: int) -> list[dict[str, Any]]:
        claimed: list[dict[str, Any]] = []
        changed = False
        for source_step_id in range(1, target_step_id):
            state = self.step_state(source_step_id)
            if not is_completed_step_status(state.get("status")) or not self.step_has_unresolved_yaml_findings(source_step_id):
                continue
            report = self.load_yaml_validation_report(source_step_id)
            if not report or report.get("resolved_by_step") is not None:
                continue
            target = report.get("handoff_target_step")
            if target is None:
                report["handoff_target_step"] = target_step_id
                report["updated_at"] = utc_now()
                _write_json(self.validation_report_path(source_step_id), report)
                state["yaml_validation_handoff_target_step"] = target_step_id
                changed = True
                claimed.append(report)
            elif int(target) == target_step_id:
                claimed.append(report)
        if changed:
            self.save()
        return claimed

    def _requeue_yaml_validation_handoffs(self, cleared_step_ids: set[int]) -> None:
        changed = False
        for source_step_id in range(1, len(STEPS) + 1):
            if source_step_id in cleared_step_ids:
                continue
            report = self.load_yaml_validation_report(source_step_id)
            if not report:
                continue
            target = report.get("handoff_target_step")
            resolver = report.get("resolved_by_step")
            target_cleared = target is not None and int(target) in cleared_step_ids
            resolver_cleared = resolver is not None and int(resolver) in cleared_step_ids
            if not target_cleared and not resolver_cleared:
                continue
            report["handoff_target_step"] = None
            report["resolved_by_step"] = None
            report["resolved_at"] = None
            report["updated_at"] = utc_now()
            _write_json(self.validation_report_path(source_step_id), report)
            state = self.step_state(source_step_id)
            state["yaml_validation_handoff_target_step"] = None
            state["yaml_validation_resolved_by_step"] = None
            changed = True
        if changed:
            self.save()

    def _activate_step(self, step_id: int) -> None:
        self.session_data["current_step"] = step_id
        self.step_state(step_id)["status"] = "current"
        self.session_data["run_status"] = "active"

    def _set_awaiting_route(self, route_name: str) -> None:
        self.session_data["current_step"] = None
        self.session_data["run_status"] = f"awaiting_{route_name}_route"

    def _finish_article_pipeline(self) -> None:
        self.session_data["current_step"] = None
        self.session_data["run_status"] = "pipeline_complete_with_article"

    def _example_decision_state(self) -> str | None:
        text = self.load_output(29)
        found = {
            value
            for value in ALL_EXAMPLE_DECISION_STATES
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(value)}(?![A-Za-z0-9_])", text)
        }
        return next(iter(found)) if len(found) == 1 else None

    def _complete_final_article_from_base_without_examples(self, decision: str) -> bool:
        source = self.output_path(28)
        target = self.output_path(30)
        if not source.is_file():
            return False
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        prompt_path = self.prompt_path(30)
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(
            "RUNNER ACTION — NO EXAMPLES\n\n"
            f"Step #29 returned the unambiguous decision: {decision}.\n"
            "The runner copied the Base Markdown Case Article from step #28 unchanged to the final article output for step #30.\n"
            "No AI rewrite was requested. Step #31 may apply a conservative final patch when semantic review steps are enabled.",
            encoding="utf-8",
        )
        state = self.step_state(30)
        state.update({
            "status": "completed_by_runner_no_examples",
            "prompt_file": str(prompt_path.relative_to(self.case_dir)),
            "output_file": str(target.relative_to(self.case_dir)),
            "last_saved_at": utc_now(),
            "completed_at": utc_now(),
            "runner_completion_mode": "completed_by_runner_no_examples",
            "example_decision_state": decision,
        })
        return True

    def _advance_after_completed(self, step_id: int) -> None:
        reviews = self.ai_review_steps_enabled
        if step_id == 1:
            self._activate_step(2)
        elif step_id == 2:
            self._activate_step(3 if reviews else 4)
        elif step_id == 3:
            self._activate_step(4)
        elif step_id == 4:
            self._activate_step(5 if reviews else 6)
        elif step_id == 5:
            self._activate_step(6)
        elif step_id == 6:
            if reviews:
                self._activate_step(7)
            else:
                self._set_awaiting_route("addon")
        elif step_id == 7:
            self._set_awaiting_route("addon")
        elif step_id == 8:
            self._activate_step(9)
        elif step_id == 9:
            self._activate_step(10 if reviews else 11)
        elif step_id == 10:
            self._activate_step(11)
        elif step_id == 11:
            if reviews:
                self._activate_step(12)
            else:
                self._set_awaiting_route("mip")
        elif step_id == 12:
            self._set_awaiting_route("mip")
        elif step_id == 13:
            self._activate_step(14)
        elif step_id == 14:
            self._activate_step(15 if reviews else 16)
        elif step_id == 15:
            self._activate_step(16)
        elif step_id == 16:
            if reviews:
                self._activate_step(17)
            else:
                self._set_awaiting_route("ahp")
        elif step_id == 17:
            self._set_awaiting_route("ahp")
        elif step_id == 18:
            self._activate_step(19 if reviews else 20)
        elif step_id == 19:
            self._activate_step(20)
        elif step_id == 20:
            self._activate_step(21 if reviews else 22)
        elif step_id == 21:
            self._activate_step(22)
        elif step_id == 22:
            self._activate_step(23 if reviews else 24)
        elif step_id == 23:
            self._activate_step(24)
        elif step_id == 24:
            if reviews:
                self._activate_step(25)
            else:
                self._activate_step(26)
        elif step_id == 25:
            self._activate_step(26)
        elif step_id == 26:
            self._set_awaiting_route("article")
        elif step_id in {27, 28}:
            self._activate_step(step_id + 1)
        elif step_id == 29:
            decision = self._example_decision_state()
            if decision in NO_EXAMPLE_DECISION_STATES and self._complete_final_article_from_base_without_examples(decision):
                if reviews:
                    self._activate_step(31)
                else:
                    self._finish_article_pipeline()
            else:
                self._activate_step(30)
        elif step_id == 30:
            if reviews:
                self._activate_step(31)
            else:
                self._finish_article_pipeline()
        elif step_id == 31:
            self._finish_article_pipeline()
        else:
            raise StorageError(f"Unsupported completion transition for step #{step_id}.")

    def complete_step(self, step_id: int) -> None:
        current = self.current_step_id()
        if current != step_id:
            raise StorageError(f"Only current step #{current} can be completed.")
        if is_ai_review_step(step_id) and not self.ai_review_steps_enabled:
            raise StorageError(f"AI review step #{step_id} is disabled for this case.")

        state = self.step_state(step_id)
        state["status"] = "completed"
        state["completed_at"] = utc_now()
        self._advance_after_completed(step_id)
        self.save()

    def has_step_activity(self, step_ids: Iterable[int]) -> bool:
        for step_id in step_ids:
            state = self.step_state(step_id)
            if is_completed_step_status(state.get("status")) or state.get("status") in {"current", "draft"}:
                return True
            if self.prompt_path(step_id).exists() or self.output_path(step_id).exists():
                return True
        return False

    def _archive_and_clear(self, label: str, step_ids: Iterable[int], extra_files: Iterable[Path] = ()) -> Path | None:
        step_ids = tuple(step_ids)
        cleared_step_ids = set(step_ids)
        files: list[tuple[Path, str]] = []
        for step_id in step_ids:
            prompt = self.prompt_path(step_id)
            output = self.output_path(step_id)
            validation = self.validation_report_path(step_id)
            if prompt.exists():
                files.append((prompt, f"prompts/{prompt.name}"))
            if output.exists():
                files.append((output, f"outputs/{output.name}"))
            if validation.exists():
                files.append((validation, f"validation/{validation.name}"))
        for path in extra_files:
            if path.exists():
                files.append((path, path.name))

        self._requeue_yaml_validation_handoffs(cleared_step_ids)

        archive_dir: Path | None = None
        if files:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            archive_dir = self.history_dir / f"{stamp}-{label}"
            archive_dir.mkdir(parents=True, exist_ok=True)
            _write_json(archive_dir / "session_snapshot.json", self.session_data)
            for source, relative_name in files:
                target = archive_dir / relative_name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

        for step_id in step_ids:
            prompt = self.prompt_path(step_id)
            output = self.output_path(step_id)
            validation = self.validation_report_path(step_id)
            if prompt.exists():
                prompt.unlink()
            if output.exists():
                output.unlink()
            if validation.exists():
                validation.unlink()
            state = self.step_state(step_id)
            state.update({
                "prompt_file": None,
                "output_file": None,
                "last_saved_at": None,
                "completed_at": None,
                "yaml_validation_file": None,
                "yaml_validation_status": None,
                "yaml_validation_issue_count": 0,
                "yaml_validation_handoff_target_step": None,
                "yaml_validation_resolved_by_step": None,
                "runner_completion_mode": None,
                "example_decision_state": None,
            })
        return archive_dir

    def _set_statuses(self, statuses: dict[int, str]) -> None:
        for step_id, status in statuses.items():
            self.step_state(step_id)["status"] = status

    def _set_case_record_statuses(self, current_step: int = 20) -> None:
        statuses = {
            20: "current" if current_step == 20 else "open",
            21: "open" if self.ai_review_steps_enabled else "skipped",
            22: "open",
            23: "open" if self.ai_review_steps_enabled else "skipped",
            24: "open",
            25: "open" if self.ai_review_steps_enabled else "skipped",
        }
        self._set_statuses(statuses)

    def _apply_review_mode_to_future_steps(self) -> None:
        if self.ai_review_steps_enabled:
            return
        for step_id in AI_REVIEW_STEP_IDS:
            state = self.step_state(step_id)
            if state.get("status") != "completed":
                state["status"] = "skipped"


    def reset_from_step(self, step_id: int) -> Path | None:
        if step_id < 1 or step_id > len(STEPS):
            raise StorageError(f"Unknown step #{step_id}.")

        state = self.step_state(step_id)
        status = state.get("status")
        if not is_completed_step_status(status) and status not in {"current", "draft"}:
            raise StorageError(f"Step #{step_id} cannot be reset from status {status!r}.")

        route_fields_to_clear: tuple[str, ...]
        route_filenames_to_clear: tuple[str, ...]
        if step_id <= 7:
            route_fields_to_clear = ("route", "mip_route", "ahp_route", "article_route")
            route_filenames_to_clear = ("route.json", "mip_route.json", "ahp_route.json", "article_route.json")
            open_through = 7
        elif step_id <= 12:
            route_fields_to_clear = ("mip_route", "ahp_route", "article_route")
            route_filenames_to_clear = ("mip_route.json", "ahp_route.json", "article_route.json")
            open_through = 12
        elif step_id <= 17:
            route_fields_to_clear = ("ahp_route", "article_route")
            route_filenames_to_clear = ("ahp_route.json", "article_route.json")
            open_through = 17
        elif step_id <= 25:
            route_fields_to_clear = ("article_route",)
            route_filenames_to_clear = ("article_route.json",)
            open_through = 25
        elif step_id == 26:
            route_fields_to_clear = ("article_route",)
            route_filenames_to_clear = ("article_route.json",)
            open_through = 26
        else:
            route_fields_to_clear = ()
            route_filenames_to_clear = ()
            open_through = 31

        route_files = tuple(self.case_dir / filename for filename in route_filenames_to_clear)
        archive_dir = self._archive_and_clear(
            f"manual-reset-step-{step_id:02d}",
            range(step_id, 32),
            route_files,
        )

        for field in route_fields_to_clear:
            self.session_data[field] = None
        for route_file in route_files:
            if route_file.exists():
                route_file.unlink()

        for downstream_step_id in range(step_id, 32):
            self.step_state(downstream_step_id)["status"] = "locked"
        for active_step_id in range(step_id, open_through + 1):
            self.step_state(active_step_id)["status"] = "open"

        self.step_state(step_id)["status"] = "current"
        self.session_data["current_step"] = step_id
        self.session_data["run_status"] = "active"
        self._apply_review_mode_to_future_steps()
        self.save()
        return archive_dir

    def set_route(self, route: dict[str, Any]) -> bool:
        if not self.route_ready("addon"):
            required = self.required_route_step("addon")
            raise StorageError(f"Step #{required} must be completed before setting the add-on route.")

        old_route = self.session_data.get("route")
        changed = _route_signature(old_route, ("route_type", "selected_addon")) != _route_signature(route, ("route_type", "selected_addon"))
        if old_route and changed:
            self._archive_and_clear(
                "addon-route",
                range(8, 32),
                (self.case_dir / "route.json", self.case_dir / "mip_route.json", self.case_dir / "ahp_route.json", self.case_dir / "article_route.json"),
            )
            self.session_data["mip_route"] = None
            self.session_data["ahp_route"] = None
            self.session_data["article_route"] = None
            for filename in ("mip_route.json", "ahp_route.json", "article_route.json"):
                path = self.case_dir / filename
                if path.exists():
                    path.unlink()

        route = dict(route)
        route["recorded_at"] = utc_now()
        _write_json(self.case_dir / "route.json", route)
        self.session_data["route"] = route

        if not changed and old_route:
            self.save()
            return False

        route_type = route.get("route_type")
        if route_type == "selected_addon":
            if not route.get("selected_addon"):
                raise StorageError("A selected add-on is required for the selected add-on route.")
            self._set_statuses({8: "current", 9: "open", 10: "open" if self.ai_review_steps_enabled else "skipped", 11: "open", 12: "open" if self.ai_review_steps_enabled else "skipped"})
            self._set_statuses({step_id: "locked" for step_id in range(13, 32)})
            self.session_data["current_step"] = 8
            self.session_data["run_status"] = "active"
        elif route_type == "core_only":
            self._set_statuses({8: "skipped", 9: "skipped", 10: "skipped", 11: "current", 12: "open" if self.ai_review_steps_enabled else "skipped"})
            self._set_statuses({step_id: "locked" for step_id in range(13, 32)})
            self.session_data["current_step"] = 11
            self.session_data["run_status"] = "active"
        else:
            raise StorageError(f"Unsupported route type: {route_type}")
        self.save()
        return changed

    def set_mip_route(self, route: dict[str, Any]) -> bool:
        if not self.route_ready("mip"):
            required = self.required_route_step("mip")
            raise StorageError(f"Step #{required} must be completed before setting the MIP route.")

        old_route = self.session_data.get("mip_route")
        changed = _route_signature(old_route, ("route_type",)) != _route_signature(route, ("route_type",))
        if old_route and changed:
            self._archive_and_clear(
                "mip-route",
                range(13, 32),
                (self.case_dir / "mip_route.json", self.case_dir / "ahp_route.json", self.case_dir / "article_route.json"),
            )
            self.session_data["ahp_route"] = None
            self.session_data["article_route"] = None
            for filename in ("ahp_route.json", "article_route.json"):
                path = self.case_dir / filename
                if path.exists():
                    path.unlink()

        route = dict(route)
        route["recorded_at"] = utc_now()
        _write_json(self.case_dir / "mip_route.json", route)
        self.session_data["mip_route"] = route

        if not changed and old_route:
            self.save()
            return False

        route_type = route.get("route_type")
        if route_type == "use_mip":
            self._set_statuses({13: "current", 14: "open", 15: "open" if self.ai_review_steps_enabled else "skipped"})
            self._set_statuses({step_id: "locked" for step_id in range(16, 32)})
            self.session_data["current_step"] = 13
            self.session_data["run_status"] = "active"
        elif route_type == "no_mip":
            self._set_statuses({step_id: "skipped" for step_id in range(13, 20)})
            self._set_case_record_statuses(current_step=20)
            self._set_statuses({step_id: "locked" for step_id in range(26, 32)})
            self.session_data["current_step"] = 20
            self.session_data["run_status"] = "active"
        else:
            raise StorageError(f"Unsupported MIP route type: {route_type}")
        self.save()
        return changed

    def set_ahp_route(self, route: dict[str, Any]) -> bool:
        if not self.route_ready("ahp"):
            required = self.required_route_step("ahp")
            raise StorageError(f"Step #{required} must be completed before setting the AHP route.")

        old_route = self.session_data.get("ahp_route")
        changed = _route_signature(old_route, ("route_type",)) != _route_signature(route, ("route_type",))
        if old_route and changed:
            self._archive_and_clear("ahp-route", range(18, 32), (self.case_dir / "ahp_route.json", self.case_dir / "article_route.json"))
            self.session_data["article_route"] = None
            article_path = self.case_dir / "article_route.json"
            if article_path.exists():
                article_path.unlink()

        route = dict(route)
        route["recorded_at"] = utc_now()
        _write_json(self.case_dir / "ahp_route.json", route)
        self.session_data["ahp_route"] = route

        if not changed and old_route:
            self.save()
            return False

        route_type = route.get("route_type")
        if route_type == "use_ahp":
            self._set_statuses({18: "current", 19: "open" if self.ai_review_steps_enabled else "skipped"})
            self._set_statuses({step_id: "locked" for step_id in range(20, 32)})
            self.session_data["current_step"] = 18
            self.session_data["run_status"] = "active"
        elif route_type == "no_ahp":
            self._set_statuses({18: "skipped", 19: "skipped"})
            self._set_case_record_statuses(current_step=20)
            self._set_statuses({step_id: "locked" for step_id in range(26, 32)})
            self.session_data["current_step"] = 20
            self.session_data["run_status"] = "active"
        else:
            raise StorageError(f"Unsupported AHP route type: {route_type}")
        self.save()
        return changed

    def set_article_route(self, route: dict[str, Any]) -> bool:
        if not self.route_ready("article"):
            required = self.required_route_step("article")
            raise StorageError(f"Step #{required} must be completed before setting the article route.")

        route = dict(route)
        route_type = route.get("route_type")
        if route_type == "generate_article":
            profile = str(route.get("article_profile") or ARTICLE_PROFILE_FULL)
            if profile not in VALID_ARTICLE_PROFILES:
                raise StorageError(f"Unsupported article profile: {profile}")
            route["article_profile"] = profile
        elif route_type == "no_article":
            route.pop("article_profile", None)
        else:
            raise StorageError(f"Unsupported article route type: {route_type}")

        old_route = self.session_data.get("article_route")
        changed = _article_route_signature(old_route) != _article_route_signature(route)
        if old_route and changed:
            self._archive_and_clear(
                "article-route",
                range(27, 32),
                (self.case_dir / "article_route.json",),
            )

        route["recorded_at"] = utc_now()
        _write_json(self.case_dir / "article_route.json", route)
        self.session_data["article_route"] = route

        if not changed and old_route:
            self.save()
            return False

        if route_type == "generate_article":
            self._set_statuses({27: "current", 28: "open", 29: "open", 30: "open", 31: "open" if self.ai_review_steps_enabled else "skipped"})
            self.session_data["current_step"] = 27
            self.session_data["run_status"] = "active"
        else:
            self._set_statuses({step_id: "skipped" for step_id in range(27, 32)})
            self.session_data["current_step"] = None
            self.session_data["run_status"] = "pipeline_complete_without_article"
        self.save()
        return changed

    def load_output(self, step_id: int) -> str:
        path = self.output_path(step_id)
        return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""

    def load_prompt(self, step_id: int) -> str:
        path = self.prompt_path(step_id)
        return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""

    def _disable_unfinished_review_steps(self) -> None:
        unfinished = [
            step_id for step_id in AI_REVIEW_STEP_IDS
            if self.step_state(step_id).get("status") != "completed"
        ]
        active_files = [
            step_id for step_id in unfinished
            if self.prompt_path(step_id).exists() or self.output_path(step_id).exists()
        ]
        if active_files:
            self._archive_and_clear("ai-review-disabled", active_files)

        current = self.current_step_id()
        current_review_source = REVIEW_SOURCE_STEP.get(current) if current is not None else None
        for step_id in unfinished:
            self.step_state(step_id)["status"] = "skipped"

        if current_review_source is not None:
            self.session_data["current_step"] = None
            self._advance_after_completed(current_review_source)

    def _enable_future_review_steps(self) -> None:
        awaiting_to_step = {
            "awaiting_addon_route": 7,
            "awaiting_mip_route": 12,
            "awaiting_ahp_route": 17,
            "awaiting_article_route": 26,
        }
        run_status = str(self.session_data.get("run_status", "active"))
        if run_status in awaiting_to_step:
            step_id = awaiting_to_step[run_status]
            if self.step_state(step_id).get("status") == "skipped":
                self._activate_step(step_id)

        current = self.current_step_id()
        for step_id in AI_REVIEW_STEP_IDS:
            state = self.step_state(step_id)
            if state.get("status") != "skipped":
                continue
            source_step = REVIEW_SOURCE_STEP[step_id]
            source_status = self.step_state(source_step).get("status")
            if source_status in {"skipped", "locked"}:
                continue
            if current is not None and step_id > current:
                state["status"] = "open"

    def update_case(self, values: dict[str, Any]) -> None:
        old_review_mode = self.ai_review_steps_enabled
        new_review_mode = bool(values.get("ai_review_steps_enabled", old_review_mode))
        validation_behavior = str(values.get("yaml_validation_behavior", self.yaml_validation_behavior))
        if validation_behavior not in VALID_YAML_VALIDATION_BEHAVIORS:
            validation_behavior = DEFAULT_YAML_VALIDATION_BEHAVIOR

        self.case_data.update({
            "title": str(values.get("title", self.case_data.get("title", ""))).strip(),
            "description": str(values.get("description", self.case_data.get("description", ""))).strip(),
            "source_status": str(values.get("source_status", self.case_data.get("source_status", ""))).strip(),
            "intended_use": str(values.get("intended_use", self.case_data.get("intended_use", ""))).strip(),
            "ai_review_steps_enabled": new_review_mode,
            "local_yaml_validation_enabled": bool(values.get("local_yaml_validation_enabled", self.local_yaml_validation_enabled)),
            "yaml_validation_behavior": validation_behavior,
        })

        if old_review_mode and not new_review_mode:
            self._disable_unfinished_review_steps()
        elif not old_review_mode and new_review_mode:
            self._enable_future_review_steps()

        current = self.current_step_id()
        if current is not None:
            for step in STEPS:
                if step.step_id >= current:
                    path = self.prompt_path(step.step_id)
                    if path.exists():
                        path.unlink()
                    self.step_state(step.step_id)["prompt_file"] = None
        self.save()



class CaseStore:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.cases_dir = self.project_root / "cases"
        self.cases_dir.mkdir(parents=True, exist_ok=True)

    def create_case(self, values: dict[str, Any]) -> CaseSession:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_id = f"{timestamp}-{_slugify(values['title'])}"
        case_id = base_id
        counter = 2
        while (self.cases_dir / case_id).exists():
            case_id = f"{base_id}-{counter}"
            counter += 1

        case_dir = self.cases_dir / case_id
        for subdir in ("prompts", "outputs", "exchanges", "validation", "history"):
            (case_dir / subdir).mkdir(parents=True, exist_ok=True)

        now = utc_now()
        validation_behavior = str(values.get("yaml_validation_behavior", DEFAULT_YAML_VALIDATION_BEHAVIOR))
        if validation_behavior not in VALID_YAML_VALIDATION_BEHAVIORS:
            validation_behavior = DEFAULT_YAML_VALIDATION_BEHAVIOR

        case_data: dict[str, Any] = {
            "schema_version": "PMS_ORCHESTRATOR_CASE_1.3",
            "case_id": case_id,
            "title": values["title"].strip(),
            "description": values["description"].strip(),
            "source_status": values["source_status"].strip(),
            "intended_use": values["intended_use"].strip(),
            "ai_review_steps_enabled": bool(values.get("ai_review_steps_enabled", DEFAULT_AI_REVIEW_STEPS_ENABLED)),
            "local_yaml_validation_enabled": bool(values.get("local_yaml_validation_enabled", DEFAULT_LOCAL_YAML_VALIDATION_ENABLED)),
            "yaml_validation_behavior": validation_behavior,
            "created_at": now,
            "updated_at": now,
        }
        if values.get("created_from_iteration_handoff"):
            case_data["created_from_iteration_handoff"] = True
            case_data["parent_case_id"] = str(values.get("parent_case_id") or "")
            case_data["parent_case_title"] = str(values.get("parent_case_title") or "")
            case_data["parent_case_dir"] = str(values.get("parent_case_dir") or "")
        steps = {str(step.step_id): _new_step_state(step.step_id) for step in STEPS}
        if not case_data["ai_review_steps_enabled"]:
            for review_step_id in AI_REVIEW_STEP_IDS:
                steps[str(review_step_id)]["status"] = "skipped"
        session_data: dict[str, Any] = {
            "schema_version": "PMS_ORCHESTRATOR_SESSION_1.3",
            "case_id": case_id,
            "run_status": "active",
            "current_step": 1,
            "steps": steps,
            "route": None,
            "mip_route": None,
            "ahp_route": None,
            "article_route": None,
            "created_at": now,
            "updated_at": now,
        }
        session = CaseSession(self.project_root, case_dir, case_data, session_data)
        session.save()
        lineage = values.get("followup_lineage")
        if isinstance(lineage, dict):
            _write_json(case_dir / "followup_lineage.json", lineage)
        return session

    def _migrate_case(self, case_data: dict[str, Any], session_data: dict[str, Any]) -> bool:
        changed = False
        steps = session_data.setdefault("steps", {})
        new_step_ids: set[int] = set()
        for step in STEPS:
            key = str(step.step_id)
            if key not in steps:
                steps[key] = _new_step_state(step.step_id)
                new_step_ids.add(step.step_id)
                changed = True
            else:
                if steps[key].get("title") != step.title:
                    steps[key]["title"] = step.title
                    changed = True
                defaults = {
                    "yaml_validation_file": None,
                    "yaml_validation_status": None,
                    "yaml_validation_issue_count": 0,
                    "yaml_validation_handoff_target_step": None,
                    "yaml_validation_resolved_by_step": None,
                    "runner_completion_mode": None,
                    "example_decision_state": None,
                }
                for field, default in defaults.items():
                    if field not in steps[key]:
                        steps[key][field] = default
                        changed = True

        old_status = str(session_data.get("run_status", "active"))
        route = session_data.get("route") or {}
        route_type = route.get("route_type")
        current = session_data.get("current_step")

        if old_status == "awaiting_route":
            session_data["run_status"] = "awaiting_addon_route"
            old_status = "awaiting_addon_route"
            changed = True

        if old_status in {"pass_1_complete", "vertical_slice_complete"}:
            if route_type == "selected_addon" and steps["10"].get("status") != "completed":
                steps["8"]["status"] = "current"
                steps["9"]["status"] = "open"
                steps["10"]["status"] = "open"
                session_data["current_step"] = 8
            else:
                steps["11"]["status"] = "current"
                steps["12"]["status"] = "open"
                session_data["current_step"] = 11
            session_data["run_status"] = "active"
            old_status = "active"
            changed = True
        elif current is None and steps["10"].get("status") == "completed" and steps["11"].get("status") not in {"completed", "current"}:
            steps["11"]["status"] = "current"
            session_data["current_step"] = 11
            session_data["run_status"] = "active"
            old_status = "active"
            changed = True

        session_data.setdefault("mip_route", None)
        session_data.setdefault("ahp_route", None)
        session_data.setdefault("article_route", None)
        existing_article_route = session_data.get("article_route")
        if (
            isinstance(existing_article_route, dict)
            and existing_article_route.get("route_type") == "generate_article"
            and existing_article_route.get("article_profile") not in VALID_ARTICLE_PROFILES
        ):
            existing_article_route["article_profile"] = ARTICLE_PROFILE_FULL
            changed = True
        mip_route = session_data.get("mip_route") or {}

        # Extend earlier runs without disturbing an active or awaiting route position.
        added_ahp_steps = bool(new_step_ids.intersection(set(range(16, 20))))
        added_case_record_steps = bool(new_step_ids.intersection(set(range(20, 26))))
        added_iteration_step = 26 in new_step_ids
        added_article_steps = bool(new_step_ids.intersection(set(range(27, 32))))
        mip_type = mip_route.get("route_type")
        ahp_route = session_data.get("ahp_route") or {}
        ahp_type = ahp_route.get("route_type")
        current = session_data.get("current_step")

        if old_status == "through_step_15_complete":
            if mip_type == "no_mip":
                for step_id in range(13, 20):
                    steps[str(step_id)]["status"] = "skipped"
                if added_case_record_steps:
                    steps["20"]["status"] = "current"
                    for step_id in range(21, 26):
                        steps[str(step_id)]["status"] = "open"
                    session_data["current_step"] = 20
                    session_data["run_status"] = "active"
                else:
                    session_data["current_step"] = None
            elif mip_type == "use_mip" and steps["15"].get("status") == "completed":
                steps["16"]["status"] = "current"
                steps["17"]["status"] = "open"
                for step_id in range(18, 26):
                    steps[str(step_id)]["status"] = "locked"
                session_data["current_step"] = 16
                session_data["run_status"] = "active"
            changed = True
        elif old_status == "through_step_19_complete":
            steps["20"]["status"] = "current"
            for step_id in range(21, 26):
                steps[str(step_id)]["status"] = "open"
            session_data["current_step"] = 20
            session_data["run_status"] = "active"
            changed = True
        elif added_ahp_steps and current is None and old_status not in {"awaiting_addon_route", "awaiting_mip_route", "awaiting_ahp_route"}:
            # Compatibility for older runs that ended after MIP but predate AHP steps.
            if mip_type == "no_mip":
                for step_id in range(13, 20):
                    steps[str(step_id)]["status"] = "skipped"
                if added_case_record_steps:
                    steps["20"]["status"] = "current"
                    for step_id in range(21, 26):
                        steps[str(step_id)]["status"] = "open"
                    session_data["current_step"] = 20
                    session_data["run_status"] = "active"
            elif mip_type == "use_mip" and steps["15"].get("status") == "completed":
                steps["16"]["status"] = "current"
                steps["17"]["status"] = "open"
                for step_id in range(18, 26):
                    steps[str(step_id)]["status"] = "locked"
                session_data["current_step"] = 16
                session_data["run_status"] = "active"
            changed = True
        elif added_case_record_steps:
            # v0.4 cases keep their current/awaiting analytical position; Stage 1–3 stay locked
            # until the analytical route converges after step #19 or a no-MIP/no-AHP decision.
            for step_id in range(20, 26):
                if not is_completed_step_status(steps[str(step_id)].get("status")) and steps[str(step_id)].get("status") not in {"current", "open", "skipped"}:
                    steps[str(step_id)]["status"] = "locked"
            changed = True


        # Runs that ended after checked Stage 3 now first produce the optional
        # Iteration Handoff before pausing for the optional article decision.
        article_route = session_data.get("article_route") or {}
        article_type = article_route.get("route_type")
        current = session_data.get("current_step")
        stage_3_checked = steps.get("25", {}).get("status") == "completed"
        iteration_done = is_completed_step_status(steps.get("26", {}).get("status"))
        if stage_3_checked and current is None and not iteration_done:
            steps["26"]["status"] = "current"
            for step_id in range(27, 32):
                if not is_completed_step_status(steps[str(step_id)].get("status")):
                    steps[str(step_id)]["status"] = "locked"
            session_data["current_step"] = 26
            session_data["run_status"] = "active"
            changed = True
        elif stage_3_checked and current is None and iteration_done:
            if article_type == "generate_article":
                incomplete_article_steps = [
                    step_id for step_id in range(27, 32)
                    if not is_completed_step_status(steps[str(step_id)].get("status"))
                ]
                if incomplete_article_steps:
                    next_article_step = incomplete_article_steps[0]
                    for step_id in range(27, 32):
                        if step_id < next_article_step and not is_completed_step_status(steps[str(step_id)].get("status")):
                            steps[str(step_id)]["status"] = "completed"
                        elif step_id == next_article_step:
                            steps[str(step_id)]["status"] = "current"
                        elif not is_completed_step_status(steps[str(step_id)].get("status")):
                            steps[str(step_id)]["status"] = "open"
                    session_data["current_step"] = next_article_step
                    session_data["run_status"] = "active"
                else:
                    session_data["run_status"] = "pipeline_complete_with_article"
            elif article_type == "no_article":
                for step_id in range(27, 32):
                    steps[str(step_id)]["status"] = "skipped"
                session_data["run_status"] = "pipeline_complete_without_article"
            else:
                for step_id in range(27, 32):
                    if not is_completed_step_status(steps[str(step_id)].get("status")):
                        steps[str(step_id)]["status"] = "locked"
                session_data["run_status"] = "awaiting_article_route"
            changed = True
        elif added_iteration_step and stage_3_checked and current is None:
            steps["26"]["status"] = "current"
            session_data["current_step"] = 26
            session_data["run_status"] = "active"
            changed = True
        elif added_article_steps:
            for step_id in range(27, 32):
                if not is_completed_step_status(steps[str(step_id)].get("status")) and steps[str(step_id)].get("status") not in {"current", "open", "skipped"}:
                    steps[str(step_id)]["status"] = "locked"
            changed = True

        if "ai_review_steps_enabled" not in case_data:
            case_data["ai_review_steps_enabled"] = DEFAULT_AI_REVIEW_STEPS_ENABLED
            changed = True
        if "local_yaml_validation_enabled" not in case_data:
            case_data["local_yaml_validation_enabled"] = DEFAULT_LOCAL_YAML_VALIDATION_ENABLED
            changed = True
        if case_data.get("yaml_validation_behavior") not in VALID_YAML_VALIDATION_BEHAVIORS:
            case_data["yaml_validation_behavior"] = DEFAULT_YAML_VALIDATION_BEHAVIOR
            changed = True

        if case_data.get("schema_version") != "PMS_ORCHESTRATOR_CASE_1.3":
            case_data["schema_version"] = "PMS_ORCHESTRATOR_CASE_1.3"
            changed = True
        if session_data.get("schema_version") != "PMS_ORCHESTRATOR_SESSION_1.3":
            session_data["schema_version"] = "PMS_ORCHESTRATOR_SESSION_1.3"
            changed = True
        return changed

    def load_case(self, case_dir: Path) -> CaseSession:
        case_dir = case_dir.resolve()
        case_data = _read_json(case_dir / "case.json")
        session_data = _read_json(case_dir / "session.json")
        if case_data.get("case_id") != session_data.get("case_id"):
            raise StorageError("case.json and session.json belong to different cases.")
        session = CaseSession(self.project_root, case_dir, case_data, session_data)
        session.validation_dir.mkdir(parents=True, exist_ok=True)
        if self._migrate_case(case_data, session_data):
            session.save()
            article_route = session_data.get("article_route")
            article_route_path = case_dir / "article_route.json"
            if isinstance(article_route, dict) and article_route_path.is_file():
                _write_json(article_route_path, article_route)
        return session

    def list_cases(self) -> list[Path]:
        result = []
        for child in self.cases_dir.iterdir():
            if child.is_dir() and (child / "case.json").is_file() and (child / "session.json").is_file():
                result.append(child)
        return sorted(result, key=lambda path: path.name, reverse=True)
