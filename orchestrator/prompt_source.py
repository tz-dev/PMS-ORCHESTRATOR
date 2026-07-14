from __future__ import annotations

import re
from pathlib import Path

from .registry import MIP_SOURCE_FILENAME


_PROMPT_HEADING = re.compile(r"^## Prompt #(\d+)\s+—\s+.+$", re.MULTILINE)


class PromptSourceError(RuntimeError):
    pass


def normalize_prompt_text(text: str) -> str:
    """Remove trailing whitespace, blank lines, and one terminal Markdown rule."""
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and lines[-1].strip() == "---":
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    return "\n".join(lines)


class PromptSource:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._prompts = self._load_prompts()

    def _load_prompts(self) -> dict[int, str]:
        if not self.path.is_file():
            raise PromptSourceError(f"Prompt source not found: {self.path}")
        text = self.path.read_text(encoding="utf-8-sig")
        matches = list(_PROMPT_HEADING.finditer(text))
        if not matches:
            raise PromptSourceError("No numbered prompt sections found.")

        prompts: dict[int, str] = {}
        for index, match in enumerate(matches):
            prompt_number = int(match.group(1))
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = normalize_prompt_text(text[start:end])
            prompts[prompt_number] = body
        return prompts

    def available_prompt_numbers(self) -> tuple[int, ...]:
        return tuple(sorted(self._prompts))

    def get(self, prompt_number: int) -> str:
        try:
            return self._prompts[prompt_number]
        except KeyError as exc:
            raise PromptSourceError(f"Prompt #{prompt_number} is missing.") from exc

    def render(
        self,
        prompt_number: int,
        case_data: dict[str, str],
        selected_addon: str | None = None,
        runtime_values: dict[str, str] | None = None,
    ) -> str:
        text = self.get(prompt_number)
        replacements = {
            "{CASE_TITLE}": case_data.get("title", ""),
            "{CASE_MATERIAL}": case_data.get("description", ""),
            "{CASE_DESCRIPTION}": case_data.get("description", ""),
            "{SOURCE_STATUS}": case_data.get("source_status", ""),
            "{INTENDED_USE}": case_data.get("intended_use", ""),
            "{SELECTED_ADDON}": selected_addon or "SELECTED_ADDON",
        }
        for marker, value in replacements.items():
            text = text.replace(marker, value)
        for marker, value in (runtime_values or {}).items():
            token = marker if marker.startswith("{") else "{" + marker + "}"
            text = text.replace(token, value)
        if selected_addon:
            text = text.replace(
                "pms_addon_SELECTED_ADDON_case_application_template.yaml",
                f"pms_addon_{selected_addon.lower()}_case_application_template.yaml",
            )
        if prompt_number in {13, 14, 15}:
            text = text.replace("MIP.yaml", MIP_SOURCE_FILENAME)
        return normalize_prompt_text(text)
