from __future__ import annotations

import os
import subprocess
import sys
import webbrowser
from pathlib import Path


class OpenPathError(RuntimeError):
    pass


def open_path(path: Path) -> None:
    path = path.resolve()
    if not path.exists():
        raise OpenPathError(f"Path does not exist: {path}")
    try:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError as exc:
        raise OpenPathError(str(exc)) from exc


def open_parent(path: Path) -> None:
    target = path if path.is_dir() else path.parent
    open_path(target)


def open_url(url: str) -> None:
    target = str(url or "").strip()
    if not target:
        raise OpenPathError("No URL is configured.")
    try:
        opened = webbrowser.open(target, new=2)
    except Exception as exc:
        raise OpenPathError(str(exc)) from exc
    if not opened:
        raise OpenPathError(f"Could not open URL: {target}")
