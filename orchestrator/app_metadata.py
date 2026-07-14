from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AppMetadata:
    name: str = "PMS-ORCHESTRATOR"
    version: str = "1.4"
    project_status: str = "Pre-release guided desktop application"
    repository_url: str = ""
    license_file: str = "LICENSE"

    @classmethod
    def load(cls, path: Path) -> "AppMetadata":
        if not path.exists():
            return cls()
        try:
            data: Any = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()
        if not isinstance(data, dict):
            return cls()
        return cls(
            name=str(data.get("name") or cls.name),
            version=str(data.get("version") or cls.version),
            project_status=str(data.get("project_status") or cls.project_status),
            repository_url=str(data.get("repository_url") or "").strip(),
            license_file=str(data.get("license_file") or cls.license_file),
        )

    def license_path(self, project_root: Path) -> Path:
        return project_root / self.license_file

    def read_license(self, project_root: Path) -> str:
        path = self.license_path(project_root)
        if not path.exists():
            return f"License file not found: {self.license_file}"
        try:
            return path.read_text(encoding="utf-8-sig").strip()
        except OSError as exc:
            return f"Could not read {self.license_file}: {exc}"
