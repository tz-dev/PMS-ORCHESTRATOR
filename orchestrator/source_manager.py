from __future__ import annotations

import json
import os
import shutil
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable


class SourceManifestError(RuntimeError):
    pass


class SourceDownloadError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceEntry:
    source_id: str
    label: str
    destination: str
    url: str

    def destination_path(self, project_root: Path) -> Path:
        relative = PurePosixPath(self.destination)
        if relative.is_absolute() or ".." in relative.parts:
            raise SourceManifestError(f"Unsafe source destination: {self.destination}")
        return project_root.joinpath(*relative.parts)


@dataclass(frozen=True)
class SourceStatus:
    entry: SourceEntry
    path: Path
    present: bool


@dataclass(frozen=True)
class SourceDownloadResult:
    entry: SourceEntry
    path: Path
    downloaded: bool
    message: str


FetchBytes = Callable[[str, int], bytes]


def _default_fetch_bytes(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PMS-ORCHESTRATOR/0.10",
            "Accept": "application/yaml,text/yaml,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = getattr(response, "status", 200)
        if status != 200:
            raise SourceDownloadError(f"HTTP {status} for {url}")
        data = response.read()
    if not data:
        raise SourceDownloadError(f"Empty response from {url}")
    return data


class SourceManifest:
    def __init__(self, manifest_path: Path, project_root: Path, entries: Iterable[SourceEntry]) -> None:
        self.manifest_path = manifest_path.resolve()
        self.project_root = project_root.resolve()
        self.entries = tuple(entries)

    @classmethod
    def load(cls, manifest_path: Path, project_root: Path) -> "SourceManifest":
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise SourceManifestError(f"Missing source manifest: {manifest_path}") from exc
        except json.JSONDecodeError as exc:
            raise SourceManifestError(f"Invalid JSON in source manifest: {exc}") from exc

        raw_sources = data.get("sources")
        if not isinstance(raw_sources, list) or not raw_sources:
            raise SourceManifestError("The source manifest must contain a non-empty 'sources' list.")

        entries: list[SourceEntry] = []
        seen_ids: set[str] = set()
        seen_destinations: set[str] = set()
        for index, item in enumerate(raw_sources, start=1):
            if not isinstance(item, dict):
                raise SourceManifestError(f"Source entry #{index} is not an object.")
            try:
                source_id = str(item["id"]).strip()
                label = str(item["label"]).strip()
                destination = str(item["destination"]).strip().replace("\\", "/")
                url = str(item["url"]).strip()
            except KeyError as exc:
                raise SourceManifestError(f"Source entry #{index} is missing {exc.args[0]!r}.") from exc
            if not source_id or not label or not destination or not url:
                raise SourceManifestError(f"Source entry #{index} contains an empty required value.")
            if source_id in seen_ids:
                raise SourceManifestError(f"Duplicate source id: {source_id}")
            if destination in seen_destinations:
                raise SourceManifestError(f"Duplicate source destination: {destination}")
            if not url.lower().startswith(("https://", "http://")):
                raise SourceManifestError(f"Unsupported source URL for {source_id}: {url}")
            entry = SourceEntry(source_id, label, destination, url)
            entry.destination_path(project_root)
            entries.append(entry)
            seen_ids.add(source_id)
            seen_destinations.add(destination)
        return cls(manifest_path, project_root, entries)

    def check(self) -> list[SourceStatus]:
        return [
            SourceStatus(entry=entry, path=entry.destination_path(self.project_root), present=entry.destination_path(self.project_root).is_file())
            for entry in self.entries
        ]

    def download_all(
        self,
        *,
        timeout: int = 20,
        fetch_bytes: FetchBytes | None = None,
        progress: Callable[[int, int, SourceEntry], None] | None = None,
    ) -> list[SourceDownloadResult]:
        fetch = fetch_bytes or _default_fetch_bytes
        staged: list[tuple[SourceEntry, Path, Path]] = []
        total = len(self.entries)

        try:
            with tempfile.TemporaryDirectory(prefix="pms-orchestrator-sources-", dir=self.project_root) as temp_dir_name:
                temp_root = Path(temp_dir_name)
                for index, entry in enumerate(self.entries, start=1):
                    if progress is not None:
                        progress(index, total, entry)
                    data = fetch(entry.url, timeout)
                    if not isinstance(data, (bytes, bytearray)) or not data:
                        raise SourceDownloadError(f"No downloadable bytes returned for {entry.label}.")
                    staged_path = temp_root / entry.source_id
                    staged_path.write_bytes(bytes(data))
                    destination = entry.destination_path(self.project_root)
                    staged.append((entry, staged_path, destination))

                backup_root = temp_root / "backups"
                backups: dict[Path, Path | None] = {}
                committed: list[Path] = []
                results: list[SourceDownloadResult] = []
                try:
                    for entry, staged_path, destination in staged:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        if destination.exists():
                            backup = backup_root / entry.source_id
                            backup.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(destination, backup)
                            backups[destination] = backup
                        else:
                            backups[destination] = None

                        replacement = destination.with_name(destination.name + ".download")
                        replacement.write_bytes(staged_path.read_bytes())
                        os.replace(replacement, destination)
                        committed.append(destination)
                        results.append(SourceDownloadResult(entry, destination, True, "Downloaded"))
                except Exception:
                    for destination in reversed(committed):
                        backup = backups.get(destination)
                        try:
                            if backup is None:
                                destination.unlink(missing_ok=True)
                            else:
                                shutil.copy2(backup, destination)
                        except OSError:
                            pass
                    raise
                return results
        except (OSError, SourceDownloadError) as exc:
            raise SourceDownloadError(str(exc)) from exc
        except Exception as exc:
            raise SourceDownloadError(f"Source download failed: {exc}") from exc
