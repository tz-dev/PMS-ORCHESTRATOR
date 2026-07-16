from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

USER_ACTIONS: tuple[str, ...] = (
    "accept",
    "refine",
    "replace",
    "split",
    "merge",
    "reject",
)

OVERALL_ACTIONS: tuple[str, ...] = (
    "accept_model_preselection",
    "accept_with_notes_or_revisions",
    "prepare_despite_negative_recommendation",
    "skip_iteration_handoff",
    "regenerate_after_revised_focus",
)

ARTICLE_VISIBILITY_VALUES: tuple[str, ...] = ("exclude", "summarize", "include")
URGENCY_LEVELS: tuple[str, ...] = ("none", "low", "moderate", "high", "critical")


@dataclass(frozen=True)
class CoverageValidation:
    ok: bool
    issues: tuple[str, ...]
    target_count: int
    dimension_count: int
    required_target_count: int | None
    required_dimension_count: int


class IterationHandoffError(RuntimeError):
    pass


def _string(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _list_of_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_string(item) for item in value if _string(item)]
    text = _string(value)
    if not text:
        return []
    return [line.strip(" -\t") for line in text.splitlines() if line.strip(" -\t")]


def _safe_id(value: str, fallback: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_\-]+", "_", value.strip().lower()).strip("_")
    return token[:64] or fallback


def unwrap_yaml_text(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(r"```(?:yaml|yml)?\s*\n(.*)\n```", stripped, flags=re.IGNORECASE | re.DOTALL)
    return match.group(1) if match else text


def parse_handoff_text(text: str) -> dict[str, Any]:
    if yaml is None:  # pragma: no cover
        raise IterationHandoffError("PyYAML is required to annotate the Iteration Handoff YAML.")
    try:
        data = yaml.safe_load(unwrap_yaml_text(text))
    except Exception as exc:  # noqa: BLE001
        raise IterationHandoffError(f"Could not parse Iteration Handoff YAML: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("pms_discipline_iteration_handoff"), dict):
        raise IterationHandoffError("Iteration Handoff YAML must contain root key pms_discipline_iteration_handoff.")
    return data


def dump_handoff_yaml(data: dict[str, Any]) -> str:
    if yaml is None:  # pragma: no cover
        raise IterationHandoffError("PyYAML is required to save the annotated Iteration Handoff YAML.")
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)


def handoff_root(data: dict[str, Any]) -> dict[str, Any]:
    root = data.setdefault("pms_discipline_iteration_handoff", {})
    if not isinstance(root, dict):
        raise IterationHandoffError("pms_discipline_iteration_handoff must be a mapping.")
    return root


def proposed_targets(root: dict[str, Any]) -> list[dict[str, Any]]:
    targets = root.get("proposed_iteration_targets")
    return targets if isinstance(targets, list) else []


def target_summary(target: dict[str, Any]) -> dict[str, str]:
    proposal = target.get("model_proposal") if isinstance(target.get("model_proposal"), dict) else {}
    return {
        "target_id": _string(target.get("target_id")),
        "focus": _string(proposal.get("focus")),
        "question": _string(proposal.get("question")),
        "basis": _string(proposal.get("basis_in_checked_record")),
        "expected_value": _string(proposal.get("expected_discriminative_value")),
        "dimension": _string(proposal.get("dimension"), "other"),
        "blocking_status": _string(proposal.get("blocking_status"), "non_blocking"),
        "priority": _string(proposal.get("priority"), "medium"),
        "required_new_material": "\n".join(_list_of_strings(proposal.get("required_new_material"))),
    }


def _base_effective_target(*, target_id: str, question: str, origin: str) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "source_target_id": None,
        "origin": origin,
        "status": "approved",
        "question": question,
        "basis_in_checked_record": "",
        "required_new_material": [],
        "expected_discriminative_value": "",
        "dimension": "other",
        "blocking_status": "non_blocking",
        "priority": "medium",
        "user_note": "",
        "revision_rationale": "",
        "builds_on_prior_point": "",
        "trajectory_note": "",
        "article_visibility": "exclude",
    }


def _effective_from_model(target: dict[str, Any], response: dict[str, Any], *, origin: str, question: str | None = None, new_id: str | None = None) -> dict[str, Any]:
    summary = target_summary(target)
    effective = _base_effective_target(
        target_id=new_id or summary["target_id"],
        question=question or summary["question"],
        origin=origin,
    )
    effective.update({
        "source_target_id": summary["target_id"] or None,
        "basis_in_checked_record": _string(response.get("builds_on_prior_point")) or summary["basis"],
        "required_new_material": _list_of_strings(response.get("additional_material_needed")) or _list_of_strings(summary["required_new_material"]),
        "expected_discriminative_value": _string(response.get("expected_discriminative_value")) or summary["expected_value"],
        "dimension": _string(response.get("dimension")) or summary["dimension"] or "other",
        "blocking_status": summary["blocking_status"] or "non_blocking",
        "priority": summary["priority"] or "medium",
        "user_note": _string(response.get("note")),
        "revision_rationale": _string(response.get("revision_rationale")),
        "builds_on_prior_point": _string(response.get("builds_on_prior_point")),
        "trajectory_note": _string(response.get("trajectory_note")),
        "article_visibility": _string(response.get("article_visibility"), "exclude") if _string(response.get("article_visibility"), "exclude") in ARTICLE_VISIBILITY_VALUES else "exclude",
    })
    return effective


def _target_by_id(root: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for target in proposed_targets(root):
        if isinstance(target, dict):
            target_id = _string(target.get("target_id"))
            if target_id:
                result[target_id] = target
    return result


def apply_user_response(data: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    updated = copy.deepcopy(data)
    root = handoff_root(updated)
    by_id = _target_by_id(root)
    overall = _string(response.get("overall_decision"), "accept_model_preselection")
    if overall not in OVERALL_ACTIONS:
        overall = "accept_with_notes_or_revisions"

    target_responses = response.get("target_responses") if isinstance(response.get("target_responses"), list) else []
    response_by_id: dict[str, dict[str, Any]] = {}
    for item in target_responses:
        if isinstance(item, dict):
            target_id = _string(item.get("target_id"))
            if target_id:
                response_by_id[target_id] = dict(item)

    effective_targets: list[dict[str, Any]] = []
    accepted_ids: list[str] = []
    refined_ids: list[str] = []
    replaced_ids: list[str] = []
    split_ids: list[str] = []
    merged_ids: list[str] = []
    rejected_ids: list[str] = []
    user_added_targets: list[dict[str, Any]] = []

    if overall in {"accept_model_preselection", "prepare_despite_negative_recommendation"}:
        for target_id, target in by_id.items():
            response_item = response_by_id.get(target_id, {"target_id": target_id, "action": "accept"})
            effective_targets.append(_effective_from_model(target, response_item, origin="model_preselection_accepted"))
            accepted_ids.append(target_id)
    elif overall == "skip_iteration_handoff":
        pass
    elif overall == "regenerate_after_revised_focus":
        pass
    else:
        for target_id, target in by_id.items():
            item = response_by_id.get(target_id, {"target_id": target_id, "action": "reject"})
            action = _string(item.get("action"), "reject")
            if action not in USER_ACTIONS:
                action = "reject"
            if action == "reject":
                rejected_ids.append(target_id)
                continue
            if action == "accept":
                effective_targets.append(_effective_from_model(target, item, origin="model_proposal_accepted"))
                accepted_ids.append(target_id)
            elif action in {"refine", "replace"}:
                revised_question = _string(item.get("revised_question")) or target_summary(target)["question"]
                origin = "user_refinement_of_model_proposal" if action == "refine" else "user_replacement_of_model_proposal"
                effective_targets.append(_effective_from_model(target, item, origin=origin, question=revised_question))
                (refined_ids if action == "refine" else replaced_ids).append(target_id)
            elif action == "split":
                split_questions = _list_of_strings(item.get("split_questions"))
                if not split_questions and _string(item.get("revised_question")):
                    split_questions = _list_of_strings(item.get("revised_question"))
                for index, split_question in enumerate(split_questions, start=1):
                    new_id = _safe_id(f"{target_id}_split_{index}", f"{target_id}_split_{index}")
                    effective_targets.append(_effective_from_model(target, item, origin="user_split_of_model_proposal", question=split_question, new_id=new_id))
                split_ids.append(target_id)
            elif action == "merge":
                merged_question = _string(item.get("revised_question")) or target_summary(target)["question"]
                new_id = _safe_id(f"{target_id}_merged", f"{target_id}_merged")
                effective_targets.append(_effective_from_model(target, item, origin="user_merge_of_model_proposals", question=merged_question, new_id=new_id))
                merged_ids.append(target_id)

    additional_questions = response.get("additional_questions")
    if isinstance(additional_questions, list):
        additional_items = [item for item in additional_questions if isinstance(item, dict)]
    else:
        additional_items = [{"question": question} for question in _list_of_strings(additional_questions)]
    for index, item in enumerate(additional_items, start=1):
        question = _string(item.get("question"))
        if not question:
            continue
        target_id = _safe_id(_string(item.get("target_id")) or f"user_added_{index}", f"user_added_{index}")
        effective = _base_effective_target(target_id=target_id, question=question, origin="user_added_followup_question")
        effective.update({
            "basis_in_checked_record": _string(item.get("basis_in_checked_record")),
            "required_new_material": _list_of_strings(item.get("required_new_material")),
            "expected_discriminative_value": _string(item.get("expected_discriminative_value")),
            "dimension": _string(item.get("dimension"), "other"),
            "priority": _string(item.get("priority"), "medium"),
            "user_note": _string(item.get("note")),
            "revision_rationale": _string(item.get("revision_rationale")),
            "builds_on_prior_point": _string(item.get("builds_on_prior_point")),
            "trajectory_note": _string(item.get("trajectory_note")),
            "article_visibility": _string(item.get("article_visibility"), "exclude") if _string(item.get("article_visibility"), "exclude") in ARTICLE_VISIBILITY_VALUES else "exclude",
        })
        effective_targets.append(effective)
        user_added_targets.append(effective)

    normalized_target_responses: list[dict[str, Any]] = []
    for raw_item in target_responses:
        if not isinstance(raw_item, dict):
            continue
        normalized_target_responses.append({
            "target_id": _string(raw_item.get("target_id")),
            "action": _string(raw_item.get("action"), "accept") if _string(raw_item.get("action"), "accept") in USER_ACTIONS else "accept",
            "note": _string(raw_item.get("note")),
            "revised_question": _string(raw_item.get("revised_question")),
            "revision_rationale": _string(raw_item.get("revision_rationale")),
            "builds_on_prior_point": _string(raw_item.get("builds_on_prior_point")),
            "additional_material_needed": _list_of_strings(raw_item.get("additional_material_needed")),
            "trajectory_note": _string(raw_item.get("trajectory_note")),
            "split_questions": _list_of_strings(raw_item.get("split_questions")),
            "merge_with_target_ids": _list_of_strings(raw_item.get("merge_with_target_ids")),
            "article_visibility": _string(raw_item.get("article_visibility"), "exclude") if _string(raw_item.get("article_visibility"), "exclude") in ARTICLE_VISIBILITY_VALUES else "exclude",
        })

    normalized_additional_questions: list[dict[str, Any]] = []
    for index, raw_item in enumerate(additional_items, start=1):
        question = _string(raw_item.get("question"))
        if not question:
            continue
        normalized_additional_questions.append({
            "target_id": _safe_id(_string(raw_item.get("target_id")) or f"user_added_{index}", f"user_added_{index}"),
            "question": question,
            "basis_in_checked_record": _string(raw_item.get("basis_in_checked_record")),
            "required_new_material": _list_of_strings(raw_item.get("required_new_material")),
            "expected_discriminative_value": _string(raw_item.get("expected_discriminative_value")),
            "dimension": _string(raw_item.get("dimension"), "other"),
            "priority": _string(raw_item.get("priority"), "medium"),
            "note": _string(raw_item.get("note")),
            "revision_rationale": _string(raw_item.get("revision_rationale")),
            "builds_on_prior_point": _string(raw_item.get("builds_on_prior_point")),
            "trajectory_note": _string(raw_item.get("trajectory_note")),
            "article_visibility": _string(raw_item.get("article_visibility"), "exclude") if _string(raw_item.get("article_visibility"), "exclude") in ARTICLE_VISIBILITY_VALUES else "exclude",
        })

    root["user_response"] = {
        "status": "confirmed" if overall not in {"regenerate_after_revised_focus"} else "revision_requested",
        "overall_decision": overall,
        "target_responses": normalized_target_responses,
        "additional_questions": normalized_additional_questions,
        "general_case_notes": _string(response.get("general_case_notes")),
        "chronology_or_trajectory_notes": _string(response.get("chronology_or_trajectory_notes")),
        "material_location_notes": _string(response.get("material_location_notes")),
        "general_handoff_note": _string(response.get("general_handoff_note")),
    }

    status = "approved"
    handoff_status = "user_confirmed"
    if overall == "skip_iteration_handoff":
        status = "declined"
        handoff_status = "declined_by_user"
    elif overall == "regenerate_after_revised_focus":
        status = "requires_regeneration"
        handoff_status = "requires_regeneration"
    elif not effective_targets and _string((root.get("model_preselection") or {}).get("recommendation")) == "no_material_iteration_value":
        status = "no_material_iteration_target"
        handoff_status = "no_material_iteration_target"

    current = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
    followup_seed = current.get("followup_case_seed") if isinstance(current.get("followup_case_seed"), dict) else {}
    root["effective_followup_preparation"] = {
        "status": status,
        "accepted_targets": accepted_ids,
        "refined_targets": refined_ids,
        "replaced_targets": replaced_ids,
        "split_targets": split_ids,
        "merged_targets": merged_ids,
        "user_added_targets": [target["target_id"] for target in user_added_targets],
        "rejected_targets": rejected_ids,
        "effective_targets": effective_targets,
        "required_new_material": sorted({material for target in effective_targets for material in _list_of_strings(target.get("required_new_material"))}),
        "followup_case_seed": {
            "working_title": _string(followup_seed.get("working_title"), "optional or pending"),
            "proposed_case_boundary": _string(followup_seed.get("proposed_case_boundary"), "optional or pending"),
            "primary_question": effective_targets[0]["question"] if effective_targets else _string(followup_seed.get("primary_question"), "optional or pending"),
            "source_status": "requires_human_confirmation",
            "intended_use": "requires_human_confirmation",
            "claim_ceiling": "requires_new_pre_analysis",
        },
    }
    root["handoff_status"] = handoff_status
    return updated


def _root_from_text_or_data(value: str | dict[str, Any]) -> dict[str, Any]:
    data = parse_handoff_text(value) if isinstance(value, str) else value
    if isinstance(data, dict) and isinstance(data.get("pms_discipline_iteration_handoff"), dict):
        return handoff_root(data)
    if isinstance(data, dict):
        return data
    raise IterationHandoffError("Iteration Handoff data must be a mapping.")


def effective_targets_for_article(value: str | dict[str, Any]) -> list[dict[str, Any]]:
    """Return effective follow-up targets permitted for article rendering.

    Only confirmed/approved handoffs can contribute. Raw user notes are omitted
    unless their per-target article_visibility permits summarization or inclusion.
    """
    root = _root_from_text_or_data(value)
    effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
    status = _string(effective.get("status"))
    if status not in {"approved", "no_material_iteration_target"}:
        return []
    targets = effective.get("effective_targets") if isinstance(effective.get("effective_targets"), list) else []
    permitted: list[dict[str, Any]] = []
    for target in targets:
        if not isinstance(target, dict):
            continue
        visibility = _string(target.get("article_visibility"), "exclude")
        if visibility not in {"summarize", "include"}:
            continue
        permitted.append(target)
    return permitted


def should_render_article_outlook(value: str | dict[str, Any]) -> bool:
    root = _root_from_text_or_data(value)
    article = root.get("article_outlook") if isinstance(root.get("article_outlook"), dict) else {}
    recommendation = _string(article.get("recommendation"), "omit")
    effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
    status = _string(effective.get("status"))
    if recommendation == "omit" or status in {"declined", "requires_regeneration", "pending_user_confirmation"}:
        return False
    if status == "no_material_iteration_target":
        return recommendation in {"brief_if_article_generated", "include_if_article_generated"}
    return status == "approved"


def render_article_outlook_handoff(value: str | dict[str, Any], *, profile: str = "full_analysis_article") -> str:
    """Render a compact, prompt-safe handoff block for article prompts.

    This is not article prose. It gives the model a bounded summary of the
    confirmed Iteration Handoff and the exact limits for using it.
    """
    root = _root_from_text_or_data(value)
    depth = root.get("current_depth_assessment") if isinstance(root.get("current_depth_assessment"), dict) else {}
    model = root.get("model_preselection") if isinstance(root.get("model_preselection"), dict) else {}
    urgency = root.get("iteration_urgency") if isinstance(root.get("iteration_urgency"), dict) else {}
    article = root.get("article_outlook") if isinstance(root.get("article_outlook"), dict) else {}
    effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
    status = _string(effective.get("status"), "unknown")
    render = should_render_article_outlook(root)
    permitted_targets = effective_targets_for_article(root)

    lines = [
        "ITERATION OUTLOOK HANDOFF — RUNNER-GENERATED",
        "This block is prospective article-rendering guidance only.",
        "It does not change the current case result, claim ceiling, source status, route, operator status, layer result, sufficiency assessment, or final posture.",
        "Prior checked analysis artifacts provide bounded analytical context for a possible future case; they are not evidence for that future case.",
        "User notes are not verified facts and may appear in article prose only when article_visibility is summarize or include.",
        f"selected_article_profile: {profile}",
        f"handoff_status: {_string(root.get('handoff_status'), 'unknown')}",
        f"effective_followup_status: {status}",
        f"article_outlook_recommendation: {_string(article.get('recommendation'), 'omit')}",
        f"render_iteration_outlook: {'yes' if render else 'no'}",
        f"current_depth_status: {_string(depth.get('status'), 'unknown')}",
        f"sufficient_for_original_intended_use: {_string(depth.get('sufficient_for_original_intended_use'), 'unknown')}",
        f"iteration_value_recommendation: {_string(model.get('recommendation'), 'unknown')}",
        f"iteration_urgency_level: {_string(urgency.get('level'), 'unknown')}",
    ]
    reasons = _list_of_strings(urgency.get("reasons"))
    if reasons:
        lines.append("iteration_urgency_reasons:")
        lines.extend(f"- {item}" for item in reasons[:5])
    raises = _list_of_strings(urgency.get("what_raises_urgency"))
    lowers = _list_of_strings(urgency.get("what_lowers_urgency"))
    if raises:
        lines.append("what_raises_urgency:")
        lines.extend(f"- {item}" for item in raises[:4])
    if lowers:
        lines.append("what_lowers_urgency:")
        lines.extend(f"- {item}" for item in lowers[:4])
    consequence = _string(urgency.get("consequence_if_not_addressed"))
    if consequence:
        lines.append(f"consequence_if_not_addressed: {consequence}")
    summary_points = _list_of_strings(article.get("permitted_summary_points"))
    if summary_points:
        lines.append("permitted_summary_points:")
        lines.extend(f"- {item}" for item in summary_points[:6])
    if render and permitted_targets:
        lines.append("article_visible_effective_targets:")
        max_targets = 3 if profile == "case_article" else 8
        for target in permitted_targets[:max_targets]:
            lines.append(f"- target_id: {_string(target.get('target_id'), 'unknown')}")
            lines.append(f"  question: {_string(target.get('question'), 'unknown')}")
            lines.append(f"  basis_in_checked_record: {_string(target.get('basis_in_checked_record'), 'unknown')}")
            lines.append(f"  expected_discriminative_value: {_string(target.get('expected_discriminative_value'), 'unknown')}")
            material = _list_of_strings(target.get("required_new_material"))
            if material:
                lines.append("  required_new_material:")
                lines.extend(f"  - {item}" for item in material[:4])
            visibility = _string(target.get("article_visibility"), "exclude")
            note = _string(target.get("user_note")) if visibility == "include" else ""
            rationale = _string(target.get("revision_rationale")) if visibility in {"summarize", "include"} else ""
            trajectory = _string(target.get("trajectory_note")) if visibility == "include" else ""
            if rationale:
                lines.append(f"  user_revision_rationale_allowed_for_summary: {rationale}")
            if note:
                lines.append(f"  user_note_allowed_for_article: {note}")
            if trajectory:
                lines.append(f"  trajectory_note_allowed_for_article: {trajectory}")
    else:
        lines.append("article_visible_effective_targets: none")
    lines.extend([
        "ARTICLE RENDERING RULES FOR THIS BLOCK:",
        "- Do not describe the current case as incomplete if it is sufficient for its original intended use.",
        "- Do not convert follow-up questions into current-case findings.",
        "- Do not mention excluded raw user notes.",
        "- For case_article, use at most one brief Iteration outlook section only when render_iteration_outlook is yes.",
        "- For full_analysis_article, a fuller Iteration outlook section is allowed only when render_iteration_outlook is yes.",
        "END ITERATION OUTLOOK HANDOFF",
    ])
    return "\n".join(lines)


def required_coverage(root: dict[str, Any]) -> tuple[int | None, int, bool]:
    level = _string((root.get("iteration_urgency") or {}).get("level"), "none")
    coverage = root.get("minimum_followup_coverage") if isinstance(root.get("minimum_followup_coverage"), dict) else {}
    raw_targets = _string(coverage.get("minimum_material_targets"))
    raw_dimensions = _string(coverage.get("minimum_distinct_dimensions"))
    blocking_required = _string(coverage.get("blocking_targets_must_be_addressed"), "no").lower() == "yes"

    if raw_targets == "all_blocking_targets" or level == "critical":
        required_targets: int | None = None
    elif raw_targets.isdigit():
        required_targets = int(raw_targets)
    else:
        required_targets = {"none": 0, "low": 1, "moderate": 2, "high": 3}.get(level, 0)

    if raw_dimensions.isdigit():
        required_dimensions = int(raw_dimensions)
    else:
        required_dimensions = 2 if level == "high" else 0
    return required_targets, required_dimensions, blocking_required or level == "critical"


def validate_effective_coverage(data: dict[str, Any]) -> CoverageValidation:
    root = handoff_root(data)
    effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
    status = _string(effective.get("status"))
    if status in {"declined", "requires_regeneration", "pending_user_confirmation", "no_material_iteration_target"}:
        return CoverageValidation(True, (), 0, 0, 0, 0)

    targets = effective.get("effective_targets") if isinstance(effective.get("effective_targets"), list) else []
    material_targets: list[dict[str, Any]] = []
    issues: list[str] = []
    for target in targets:
        if not isinstance(target, dict):
            continue
        target_id = _string(target.get("target_id"), "unnamed_target")
        question = _string(target.get("question"))
        basis = _string(target.get("basis_in_checked_record")) or _string(target.get("builds_on_prior_point"))
        material = _list_of_strings(target.get("required_new_material"))
        expected = _string(target.get("expected_discriminative_value"))
        if question and basis and material and expected:
            material_targets.append(target)
        else:
            missing = []
            if not question:
                missing.append("question")
            if not basis:
                missing.append("basis in checked record")
            if not material:
                missing.append("required new material")
            if not expected:
                missing.append("expected discriminative value")
            issues.append(f"Target {target_id} is missing: {', '.join(missing)}.")

    required_targets, required_dimensions, blocking_required = required_coverage(root)
    dims = {_string(target.get("dimension"), "other") for target in material_targets if _string(target.get("dimension"), "other")}
    blocking_target_ids = {
        _string(target.get("target_id"))
        for target in proposed_targets(root)
        if _string((target.get("model_proposal") or {}).get("blocking_status")) == "blocking"
    }
    effective_sources = {
        _string(target.get("source_target_id"))
        for target in material_targets
        if _string(target.get("source_target_id"))
    }

    if required_targets is not None and len(material_targets) < required_targets:
        issues.append(f"Urgency requires at least {required_targets} material target(s); currently {len(material_targets)} qualify.")
    if len(dims) < required_dimensions:
        issues.append(f"Urgency requires at least {required_dimensions} distinct dimension(s); currently {len(dims)} qualify.")
    if blocking_required:
        missing_blockers = sorted(target_id for target_id in blocking_target_ids if target_id not in effective_sources)
        if missing_blockers:
            issues.append("Blocking target(s) not addressed: " + ", ".join(missing_blockers) + ".")

    return CoverageValidation(
        ok=not issues,
        issues=tuple(issues),
        target_count=len(material_targets),
        dimension_count=len(dims),
        required_target_count=required_targets,
        required_dimension_count=required_dimensions,
    )
