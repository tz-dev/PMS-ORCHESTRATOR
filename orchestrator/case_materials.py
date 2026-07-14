from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


MATERIALS_SCHEMA = "PMS_ORCHESTRATOR_MATERIALS_1.0"
_MATERIAL_ID = re.compile(r"^material_(\d+)$")


class CaseMaterialError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise CaseMaterialError(f"Could not read case material {path}: {exc}") from exc
    return digest.hexdigest()


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    try:
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(path)
    except OSError as exc:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass
        raise CaseMaterialError(f"Could not write case-material manifest {path}: {exc}") from exc


def _safe_inline(value: object) -> str:
    return " ".join(str(value or "").split())


def _quoted(value: object) -> str:
    return json.dumps(_safe_inline(value), ensure_ascii=False)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _unique_filename(original_name: str, occupied: set[str]) -> str:
    candidate = Path(original_name).name.strip() or "material"
    if candidate not in occupied:
        occupied.add(candidate)
        return candidate
    path = Path(candidate)
    suffixes = "".join(path.suffixes)
    stem = candidate[: -len(suffixes)] if suffixes else candidate
    counter = 2
    while True:
        proposal = f"{stem}-{counter}{suffixes}"
        if proposal not in occupied:
            occupied.add(proposal)
            return proposal
        counter += 1


def _next_material_number(entries: Iterable[dict[str, Any]]) -> int:
    highest = 0
    for entry in entries:
        match = _MATERIAL_ID.fullmatch(str(entry.get("id") or ""))
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


class CaseMaterialStore:
    def __init__(self, case_dir: Path, case_id: str) -> None:
        self.case_dir = case_dir.resolve()
        self.case_id = case_id
        self.materials_dir = self.case_dir / "materials"
        self.manifest_path = self.case_dir / "materials.json"
        self.history_dir = self.case_dir / "history" / "material_revisions"

    def _default_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": MATERIALS_SCHEMA,
            "case_id": self.case_id,
            "materials": [],
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }

    def load_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.is_file():
            return self._default_manifest()
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise CaseMaterialError(f"Could not read {self.manifest_path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise CaseMaterialError(f"Invalid JSON in {self.manifest_path}: {exc}") from exc
        if not isinstance(data, dict):
            raise CaseMaterialError(f"Case-material manifest must be a JSON object: {self.manifest_path}")
        materials = data.get("materials")
        if not isinstance(materials, list):
            raise CaseMaterialError(f"Case-material manifest has no materials list: {self.manifest_path}")
        if data.get("case_id") not in {None, self.case_id}:
            raise CaseMaterialError("Case-material manifest belongs to another case.")
        data["schema_version"] = MATERIALS_SCHEMA
        data["case_id"] = self.case_id
        return data

    def entries(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for raw in self.load_manifest().get("materials", []):
            if not isinstance(raw, dict):
                raise CaseMaterialError("Every case-material entry must be a JSON object.")
            stored_path = str(raw.get("stored_path") or "")
            if not stored_path:
                raise CaseMaterialError("A case-material entry is missing stored_path.")
            absolute = (self.case_dir / stored_path).resolve()
            if not _is_within(absolute, self.materials_dir):
                raise CaseMaterialError(f"Unsafe case-material path: {stored_path}")
            entry = dict(raw)
            entry["stored_path"] = absolute.relative_to(self.case_dir).as_posix()
            result.append(entry)
        return result

    def path_for(self, entry: dict[str, Any]) -> Path:
        stored_path = str(entry.get("stored_path") or "")
        absolute = (self.case_dir / stored_path).resolve()
        if not _is_within(absolute, self.materials_dir):
            raise CaseMaterialError(f"Unsafe case-material path: {stored_path}")
        return absolute

    def paths(self) -> list[Path]:
        return [self.path_for(entry) for entry in self.entries()]

    def _archive_previous(self, previous: dict[str, Any], removed_paths: list[Path]) -> Path | None:
        if not self.manifest_path.exists() and not removed_paths:
            return None
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        archive = self.history_dir / f"{stamp}-materials"
        archive.mkdir(parents=True, exist_ok=True)
        if self.manifest_path.exists():
            shutil.copy2(self.manifest_path, archive / "materials.json")
        else:
            _write_json(archive / "materials.json", previous)
        for source in removed_paths:
            if source.is_file():
                target = archive / "materials" / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        return archive

    def replace(self, drafts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        previous = self.load_manifest()
        old_entries = self.entries()
        old_by_id = {str(entry.get("id")): entry for entry in old_entries}
        occupied = {
            self.path_for(entry).name
            for entry in old_entries
            if self.path_for(entry).is_file()
        }
        # Keep every old filename occupied during this transaction. A newly added
        # file must never reuse the path of an entry that is removed in the same
        # save, because removed paths are deleted only after the new manifest is
        # committed.

        next_number = _next_material_number(old_entries)
        now = utc_now()
        prepared: list[dict[str, Any]] = []
        staged: list[tuple[Path, Path]] = []
        stage_dir = Path(tempfile.mkdtemp(prefix=".materials-stage-", dir=self.case_dir))
        try:
            seen_ids: set[str] = set()
            for draft in drafts:
                material_id = str(draft.get("id") or "").strip()
                description = str(draft.get("description") or "").strip()
                purpose = str(draft.get("purpose") or "").strip()
                if material_id:
                    if material_id not in old_by_id:
                        raise CaseMaterialError(f"Unknown existing case-material id: {material_id}")
                    if material_id in seen_ids:
                        raise CaseMaterialError(f"Duplicate case-material id: {material_id}")
                    seen_ids.add(material_id)
                    old = old_by_id[material_id]
                    path = self.path_for(old)
                    if not path.is_file():
                        raise CaseMaterialError(
                            f"Existing case material is missing: {old.get('stored_path')}. Remove it or restore the file."
                        )
                    prepared.append({
                        **old,
                        "description": description,
                        "purpose": purpose,
                        "size_bytes": path.stat().st_size,
                        "sha256": sha256_file(path),
                        "updated_at": now,
                    })
                    continue

                source_text = str(draft.get("source_path") or "").strip()
                if not source_text:
                    raise CaseMaterialError("A new case material has no source_path.")
                source = Path(source_text).expanduser().resolve()
                if not source.is_file():
                    raise CaseMaterialError(f"Case material is not a readable file: {source}")
                filename = _unique_filename(source.name, occupied)
                destination = self.materials_dir / filename
                staged_path = stage_dir / filename
                try:
                    shutil.copy2(source, staged_path)
                except OSError as exc:
                    raise CaseMaterialError(f"Could not stage case material {source}: {exc}") from exc
                material_id = f"material_{next_number:03d}"
                next_number += 1
                seen_ids.add(material_id)
                prepared.append({
                    "id": material_id,
                    "original_filename": source.name,
                    "stored_path": destination.relative_to(self.case_dir).as_posix(),
                    "description": description,
                    "purpose": purpose,
                    "size_bytes": staged_path.stat().st_size,
                    "sha256": sha256_file(staged_path),
                    "added_at": now,
                    "updated_at": now,
                })
                staged.append((staged_path, destination))

            retained_ids = {str(entry.get("id")) for entry in prepared}
            removed_paths = [
                self.path_for(entry)
                for entry in old_entries
                if str(entry.get("id")) not in retained_ids
            ]
            self._archive_previous(previous, removed_paths)

            self.materials_dir.mkdir(parents=True, exist_ok=True)
            moved: list[Path] = []
            try:
                for staged_path, destination in staged:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    staged_path.replace(destination)
                    moved.append(destination)
                manifest = {
                    "schema_version": MATERIALS_SCHEMA,
                    "case_id": self.case_id,
                    "materials": prepared,
                    "created_at": previous.get("created_at") or now,
                    "updated_at": now,
                }
                _write_json(self.manifest_path, manifest)
            except Exception:
                for destination in moved:
                    try:
                        destination.unlink(missing_ok=True)
                    except OSError:
                        pass
                raise

            for path in removed_paths:
                try:
                    path.unlink(missing_ok=True)
                except OSError as exc:
                    raise CaseMaterialError(f"Could not remove old case material {path}: {exc}") from exc
            return prepared
        finally:
            shutil.rmtree(stage_dir, ignore_errors=True)


def render_case_material_prompt_block(entries: list[dict[str, Any]]) -> str:
    lines = [
        "CASE MATERIAL PACKAGE — RUNNER-GENERATED",
        "This block is authoritative for which user-provided case files are configured for step #1 and for their user-supplied descriptions and purposes.",
        "Read PMS.yaml first. Then read every listed case-material file completely before responding.",
        "The case materials are bounded inputs, not PMS Base, not a PMS add-on, not MIP/AHP, not a template, not validation, and not authority.",
        "Do not infer inaccessible archive contents, missing documents, unsupported statistics, citations, provenance, or context.",
        "A material marked present: no was not available for upload and must not be reported as read.",
        "Distinguish claims contained in a material from claims established by the pipeline.",
        "",
    ]
    if not entries:
        lines.extend([
            "material_count: 0",
            "No additional case-material files are configured. Read PMS.yaml only.",
            "END CASE MATERIAL PACKAGE",
        ])
        return "\n".join(lines)

    lines.append(f"material_count: {len(entries)}")
    for index, entry in enumerate(entries, start=1):
        lines.extend([
            f"material_{index}:",
            f"  file: {_quoted(Path(str(entry.get('stored_path') or entry.get('original_filename') or 'unknown')).name)}",
            f"  case_relative_path: {_quoted(entry.get('stored_path') or 'unknown')}",
            f"  description: {_quoted(entry.get('description') or 'not supplied by user')}",
            f"  purpose: {_quoted(entry.get('purpose') or 'not supplied by user')}",
            f"  present: {'yes' if entry.get('_present', True) else 'no'}",
            f"  sha256: {_quoted(entry.get('sha256') or 'unknown')}",
            f"  size_bytes: {int(entry.get('size_bytes') or 0)}",
        ])
    lines.extend([
        "",
        "ZIP HANDLING:",
        "- ZIP is the recommended package format when several related files belong together.",
        "- For each ZIP, inspect the archive inventory and read all accessible, relevant contained files before responding.",
        "- Preserve internal filenames and file-type distinctions.",
        "- If any archive entry or contained format cannot be read, state that limitation instead of claiming complete access.",
        "",
        "REQUIRED STEP CONFIRMATION:",
        "After PMS.yaml and every accessible listed material have been read, use the material-aware confirmation specified by Prompt #1.",
        "END CASE MATERIAL PACKAGE",
    ])
    return "\n".join(lines)


def render_case_material_manifest_block(entries: list[dict[str, Any]], *, step_1_status: str) -> str:
    lines = [
        "CASE MATERIAL INVENTORY",
        "Case materials are bounded user-provided inputs. File presence does not prove that content is true, complete, relevant, or correctly interpreted.",
        "They are not PMS/MIP/AHP source files, not templates, and not evidence merely because the runner stored them.",
        f"materials_manifest: {'materials.json' if entries else 'none'}",
        f"material_count: {len(entries)}",
        "read_instruction_step: 1",
        f"step_01_status: {step_1_status}",
    ]
    if not entries:
        lines.append("materials: none")
        return "\n".join(lines)
    for entry in entries:
        material_id = str(entry.get("id") or "material_unknown")
        lines.extend([
            f"{material_id}:",
            f"  path: {_quoted(entry.get('stored_path') or 'unknown')}",
            f"  original_filename: {_quoted(entry.get('original_filename') or 'unknown')}",
            f"  present: {'yes' if entry.get('_present', True) else 'no'}",
            f"  description: {_quoted(entry.get('description') or 'not supplied by user')}",
            f"  purpose: {_quoted(entry.get('purpose') or 'not supplied by user')}",
            f"  sha256: {_quoted(entry.get('sha256') or 'unknown')}",
            f"  size_bytes: {int(entry.get('size_bytes') or 0)}",
            "  role: bounded_case_material",
        ])
    return "\n".join(lines)
