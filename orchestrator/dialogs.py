from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable

from .gate_reader import GateValue, MipGateDetails
from .registry import SUPPORTED_ADDONS
from .iteration_handoff import (
    ARTICLE_VISIBILITY_VALUES,
    OVERALL_ACTIONS,
    USER_ACTIONS,
    apply_user_response,
    dump_handoff_yaml,
    handoff_root,
    parse_handoff_text,
    proposed_targets,
    target_summary,
    validate_effective_coverage,
)


def center_on_screen(window: tk.Toplevel) -> None:
    """Center a dialog on the current screen after its requested size is known."""
    window.update_idletasks()
    width = max(window.winfo_width(), window.winfo_reqwidth())
    height = max(window.winfo_height(), window.winfo_reqheight())
    x = max(0, (window.winfo_screenwidth() - width) // 2)
    y = max(0, (window.winfo_screenheight() - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.lift()


def finalize_dialog(window: tk.Toplevel, parent: tk.Misc) -> None:
    theme_owner: tk.Misc | None = parent
    while theme_owner is not None:
        apply_theme = getattr(theme_owner, "apply_theme_to_window", None)
        if callable(apply_theme):
            apply_theme(window)
            break
        theme_owner = getattr(theme_owner, "master", None)
    center_on_screen(window)
    window.bind("<Escape>", lambda _event: (window.destroy(), "break")[-1])
    try:
        window.focus_force()
    except tk.TclError:
        pass


class ConfirmationDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, title: str, message: str) -> None:
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result = False

        ttk.Label(self, text=message, wraplength=520, justify="left").pack(fill="x", padx=18, pady=(18, 12))
        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=18, pady=(0, 18))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Continue", command=self._confirm).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _confirm(self) -> None:
        self.result = True
        self.destroy()


class DisciplineStopDialog(tk.Toplevel):
    """Show a non-overridable PMS-DISCIPLINE pipeline stop."""

    def __init__(self, parent: tk.Misc, stop_record: dict[str, Any]) -> None:
        super().__init__(parent)
        self.title("PMS-DISCIPLINE stop")
        self.transient(parent)
        self.grab_set()
        self.result = "close"

        source_step = stop_record.get("source_step", "unknown")
        requested = stop_record.get("requested_output_disposition") or "not recorded"
        hard_gate = stop_record.get("hard_gate_status") or "not recorded"
        hard_effect = stop_record.get("hard_gate_effect") or "not recorded"
        stop_reason = stop_record.get("reason") or "pipeline_case_disposition_stop"
        declared_pipeline = stop_record.get("declared_pipeline_case_disposition") or "stop"
        if stop_reason == "mandatory_person_near_hard_stop":
            stop_explanation = (
                "The checked Pre-Analysis contains the mandatory person-near hard-stop "
                "configuration. A declared proceed_reframed value cannot override that "
                "cross-field rule. Core and all later analysis steps are locked. The "
                "Pre-Analysis must be revised before the pipeline can continue."
            )
        else:
            stop_explanation = (
                "The checked Pre-Analysis sets "
                "scope_and_pipeline_disposition.pipeline_case_disposition to stop. "
                "Core and all later analysis steps are locked. This stop cannot be overridden; "
                "the Pre-Analysis must be revised before the pipeline can continue."
            )

        ttk.Label(
            self,
            text="Analysis stopped by PMS-DISCIPLINE",
            font=("TkDefaultFont", 13, "bold"),
        ).pack(fill="x", padx=20, pady=(18, 8))
        ttk.Label(
            self,
            text=stop_explanation,
            wraplength=620,
            justify="left",
        ).pack(fill="x", padx=20, pady=(0, 12))

        details = ttk.LabelFrame(self, text="Recorded status")
        details.pack(fill="x", padx=20, pady=(0, 14))
        ttk.Label(details, text=f"Source step: #{source_step}").pack(anchor="w", padx=10, pady=(8, 2))
        ttk.Label(details, text=f"Declared pipeline disposition: {declared_pipeline}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(details, text="Enforced pipeline outcome: stop").pack(anchor="w", padx=10, pady=2)
        ttk.Label(details, text=f"Requested output disposition: {requested}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(details, text=f"Hard gate: {hard_gate} · effect: {hard_effect}").pack(
            anchor="w", padx=10, pady=(2, 8)
        )

        ttk.Label(
            self,
            text=(
                "You may inspect the source output or reopen the Pre-Analysis for revision. "
                "There is intentionally no continue-anyway action."
            ),
            wraplength=620,
            justify="left",
        ).pack(fill="x", padx=20, pady=(0, 12))

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ttk.Button(buttons, text="Close", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Open source output", command=lambda: self._choose("review")).pack(
            side="right", padx=(6, 0)
        )
        ttk.Button(buttons, text="Revise Pre-Analysis", command=lambda: self._choose("revise")).pack(
            side="right"
        )

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _choose(self, value: str) -> None:
        self.result = value
        self.destroy()


class ArticlePatchPreviewDialog(tk.Toplevel):
    """Review an exact article patch diff before applying, declining, or cancelling."""

    def __init__(
        self,
        parent: tk.Misc,
        *,
        patch_titles: tuple[str, ...],
        diff_text: str,
    ) -> None:
        super().__init__(parent)
        self.title("Apply proposed patch(es)?")
        self.transient(parent)
        self.grab_set()
        self.result: bool | None = None

        ttk.Label(
            self,
            text=(
                f"The final article check proposes {len(patch_titles)} exact patch"
                f"{'es' if len(patch_titles) != 1 else ''}. Review the unified diff before deciding."
            ),
            wraplength=860,
            justify="left",
        ).pack(fill="x", padx=14, pady=(14, 8))

        if patch_titles:
            ttk.Label(
                self,
                text=" · ".join(patch_titles),
                wraplength=860,
                justify="left",
            ).pack(fill="x", padx=14, pady=(0, 8))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        preview = tk.Text(frame, wrap="none", width=112, height=32)
        y_scroll = ttk.Scrollbar(frame, orient="vertical", command=preview.yview)
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=preview.xview)
        preview.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        preview.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        preview.insert("1.0", diff_text or "No textual difference could be rendered.")
        preview.configure(state="disabled")

        ttk.Label(
            self,
            text=(
                "Yes archives the current article and applies every patch atomically. "
                "No keeps the article unchanged and records the declined proposal. "
                "Cancel returns to step #31 without completing it."
            ),
            wraplength=860,
            justify="left",
        ).pack(fill="x", padx=14, pady=(0, 8))

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="No", command=lambda: self._choose(False)).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Yes", command=lambda: self._choose(True)).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.minsize(900, 650)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _choose(self, value: bool) -> None:
        self.result = value
        self.destroy()


def ask_centered_yes_no(parent: tk.Misc, title: str, message: str) -> bool:
    dialog = ConfirmationDialog(parent, title, message)
    parent.wait_window(dialog)
    return dialog.result


def _gate_value_payload(value: GateValue) -> dict[str, Any]:
    return {
        "value": value.value,
        "read_status": value.status,
        "key_path": value.key_path,
        "raw_value": value.raw_value,
        "source_step": value.source_step,
    }


def build_binary_layer_route_result(
    *,
    layer_name: str,
    recommendation: GateValue,
    route_type: str,
    use_route: str,
    no_route: str,
    extra_recommendations: dict[str, GateValue] | None = None,
) -> dict[str, Any]:
    """Build route provenance independently of the Tk dialog."""
    recommended_use = recommendation.value == layer_name
    if route_type == use_route and recommended_use:
        basis = "gate_recommended"
    elif route_type == no_route and not recommended_use and recommendation.status in {
        "not_recommended",
        "ahp_not_recommended",
        "scan_only",
    }:
        basis = f"gate_recommended_no_{layer_name.lower()}"
    elif route_type == use_route:
        basis = "user_requested"
    else:
        basis = "manual_user_route"

    gate_recommendation: dict[str, Any] = {
        f"recommended_{layer_name.lower()}": recommended_use,
        "read_status": recommendation.status,
        "key_path": recommendation.key_path,
        "raw_value": recommendation.raw_value,
        "source_step": recommendation.source_step,
    }
    for key, value in (extra_recommendations or {}).items():
        gate_recommendation[key] = _gate_value_payload(value)

    return {
        "route_type": route_type,
        "selection_basis": basis,
        "gate_recommendation": gate_recommendation,
    }


class CaseDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Misc,
        title: str,
        initial: dict[str, Any] | None = None,
        *,
        materials_count: int = 0,
        materials_command: Callable[[tk.Misc], int | None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result: dict[str, Any] | None = None
        self.materials_command = materials_command
        initial = initial or {}

        self.columnconfigure(1, weight=1)

        # Give the three multiline case fields responsive vertical space.
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Case title").grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 4))
        self.title_var = tk.StringVar(value=initial.get("title", ""))
        ttk.Entry(self, textvariable=self.title_var, width=70).grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 4))

        ttk.Label(self, text="Case description / material").grid(row=1, column=0, sticky="nw", padx=10, pady=4)
        self.description = tk.Text(self, width=70, height=9, wrap="word")
        self.description.grid(row=1, column=1, sticky="nsew", padx=10, pady=4)
        self.description.insert("1.0", initial.get("description", ""))

        ttk.Label(
            self,
            text="Source status",
        ).grid(
            row=2,
            column=0,
            sticky="nw",
            padx=10,
            pady=4,
        )

        self.source_status = tk.Text(
            self,
            width=70,
            height=5,
            wrap="word",
        )
        self.source_status.grid(
            row=2,
            column=1,
            sticky="nsew",
            padx=10,
            pady=4,
        )
        self.source_status.insert(
            "1.0",
            initial.get("source_status", ""),
        )

        ttk.Label(self, text="Intended use").grid(row=3, column=0, sticky="nw", padx=10, pady=4)
        self.intended_use = tk.Text(self, width=70, height=5, wrap="word")
        self.intended_use.grid(row=3, column=1, sticky="nsew", padx=10, pady=4)
        self.intended_use.insert("1.0", initial.get("intended_use", ""))

        next_row = 4
        if materials_command is not None:
            materials = ttk.LabelFrame(self, text="Case materials", padding=10)
            materials.grid(row=next_row, column=0, columnspan=2, sticky="ew", padx=10, pady=(8, 4))
            materials.columnconfigure(0, weight=1)
            self.materials_count_var = tk.StringVar()
            self._set_materials_count(materials_count)
            ttk.Label(
                materials,
                textvariable=self.materials_count_var,
                wraplength=560,
            ).grid(row=0, column=0, sticky="w")
            self.materials_button = ttk.Button(
                materials,
                text="Add materials…",
                command=self._open_materials,
            )
            self.materials_button.grid(
                row=0,
                column=1,
                sticky="e",
                padx=(12, 0),
            )
            ttk.Label(
                materials,
                text=(
                    "ZIP is recommended for a related document package. Materials are read with PMS.yaml in step #1."
                ),
                wraplength=690,
            ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))
            next_row += 1

        settings = ttk.LabelFrame(self, text="Review and validation", padding=10)
        settings.grid(row=next_row, column=0, columnspan=2, sticky="ew", padx=10, pady=(8, 4))
        settings.columnconfigure(0, weight=1)

        self.ai_review_var = tk.BooleanVar(value=bool(initial.get("ai_review_steps_enabled", True)))
        ttk.Checkbutton(
            settings,
            text="Run semantic AI review steps (#3, #5, #7, …)",
            variable=self.ai_review_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            settings,
            text="Disabling these review calls saves time but accepts a higher risk of semantic drift. Route decisions remain user-confirmed.",
            wraplength=690,
        ).grid(row=1, column=0, sticky="w", padx=(22, 0), pady=(2, 8))

        self.yaml_validation_var = tk.BooleanVar(value=bool(initial.get("local_yaml_validation_enabled", True)))
        ttk.Checkbutton(
            settings,
            text="Validate generated YAML locally",
            variable=self.yaml_validation_var,
            command=self._sync_validation_controls,
        ).grid(row=2, column=0, sticky="w")
        ttk.Label(
            settings,
            text="Checks YAML syntax, template-key structure, basic types, and explicit allowed values without evaluating case meaning.",
            wraplength=690,
        ).grid(row=3, column=0, sticky="w", padx=(22, 0), pady=(2, 6))

        behavior_frame = ttk.Frame(settings)
        behavior_frame.grid(row=4, column=0, sticky="w", padx=(22, 0))
        ttk.Label(behavior_frame, text="On structural findings:").pack(side="left")
        self.yaml_behavior_var = tk.StringVar(value=str(initial.get("yaml_validation_behavior", "warn")))
        self.yaml_behavior_box = ttk.Combobox(
            behavior_frame,
            textvariable=self.yaml_behavior_var,
            values=("warn", "block"),
            state="readonly",
            width=12,
        )
        self.yaml_behavior_box.pack(side="left", padx=(8, 0))
        ttk.Label(behavior_frame, text="warn = allow confirmation · block = require correction").pack(side="left", padx=(10, 0))
        self._sync_validation_controls()

        buttons = ttk.Frame(self)
        buttons.grid(row=next_row + 1, column=0, columnspan=2, sticky="e", padx=10, pady=10)
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save", command=self._save).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda _event: self.destroy())
        self.minsize(780, 720 if materials_command is not None else 680)
        self.wait_visibility()
        finalize_dialog(self, parent)

    def _set_materials_count(self, count: int) -> None:
        if not hasattr(self, "materials_count_var"):
            return
        suffix = "file" if count == 1 else "files"
        self.materials_count_var.set(f"Configured case materials: {count} {suffix}.")

    def _open_materials(self) -> None:
        if self.materials_command is None:
            return

        count = self.materials_command(self)
        if count is not None:
            self._set_materials_count(count)

    def _sync_validation_controls(self) -> None:
        if hasattr(self, "yaml_behavior_box"):
            self.yaml_behavior_box.configure(state="readonly" if self.yaml_validation_var.get() else "disabled")

    def _save(self) -> None:
        values: dict[str, Any] = {
            "title": self.title_var.get().strip(),
            "description": self.description.get("1.0", "end-1c").strip(),
            "source_status": self.source_status.get(
                "1.0",
                "end-1c",
            ).strip(),
            "intended_use": self.intended_use.get("1.0", "end-1c").strip(),
            "ai_review_steps_enabled": self.ai_review_var.get(),
            "local_yaml_validation_enabled": self.yaml_validation_var.get(),
            "yaml_validation_behavior": self.yaml_behavior_var.get(),
        }
        required = ("title", "description", "source_status", "intended_use")
        if any(not values[field] for field in required):
            messagebox.showerror("Missing information", "All four case fields are required.", parent=self)
            return
        self.result = values
        self.destroy()


class MaterialManagerDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, entries: list[dict[str, Any]], case_dir: Path) -> None:
        super().__init__(parent)
        self.title("Case materials")
        self.transient(parent)
        self.grab_set()
        self.case_dir = case_dir
        self.result: dict[str, Any] | None = None
        self.items = [dict(entry) for entry in entries]
        self._initial_snapshot = self._snapshot(self.items)
        self._selected_index: int | None = None
        self._selection_guard = False

        ttk.Label(
            self,
            text=(
                "Add case materials such as document packages, articles, statistics, tables, or notes. "
                "ZIP is recommended when several related files belong together."
            ),
            wraplength=850,
        ).pack(fill="x", padx=14, pady=(14, 6))
        ttk.Label(
            self,
            text=(
                "The files will be copied into the case folder and uploaded manually with PMS.yaml in step #1. "
                "Description and purpose are inserted into the step #1 reading instruction."
            ),
            wraplength=850,
        ).pack(fill="x", padx=14, pady=(0, 10))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=14)
        self.tree = ttk.Treeview(
            table_frame,
            columns=("file", "type", "size", "description"),
            show="headings",
            selectmode="browse",
            height=10,
        )
        self.tree.heading("file", text="File")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.heading("description", text="Description")
        self.tree.column("file", width=280)
        self.tree.column("type", width=80, stretch=False)
        self.tree.column("size", width=90, stretch=False, anchor="e")
        self.tree.column("description", width=380)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        table_buttons = ttk.Frame(self)
        table_buttons.pack(fill="x", padx=14, pady=(8, 10))
        ttk.Button(table_buttons, text="Add file(s)…", command=self._add_files).pack(side="left")
        ttk.Button(table_buttons, text="Remove selected", command=self._remove_selected).pack(side="left", padx=(6, 0))

        details = ttk.LabelFrame(self, text="Selected material metadata", padding=10)
        details.pack(fill="x", padx=14, pady=(0, 10))
        details.columnconfigure(1, weight=1)
        ttk.Label(details, text="Description of contents").grid(row=0, column=0, sticky="nw", padx=(0, 10))
        self.description = tk.Text(details, width=72, height=4, wrap="word")
        self.description.grid(row=0, column=1, sticky="ew")
        ttk.Label(details, text="Purpose in this case").grid(row=1, column=0, sticky="nw", padx=(0, 10), pady=(8, 0))
        self.purpose = tk.Text(details, width=72, height=4, wrap="word")
        self.purpose.grid(row=1, column=1, sticky="ew", pady=(8, 0))
        ttk.Label(
            details,
            text=(
                "Metadata is user-supplied context, not evidence or validation. Empty fields are retained as not supplied."
            ),
            wraplength=730,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save materials", command=self._save).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda _event: self.destroy())
        self.minsize(900, 690)
        self._rebuild_tree(select_index=0 if self.items else None)
        self.after_idle(lambda: finalize_dialog(self, parent))

    @staticmethod
    def _snapshot(items: list[dict[str, Any]]) -> tuple[tuple[str, ...], ...]:
        rows = []
        for item in items:
            rows.append((
                str(item.get("id") or ""),
                str(item.get("stored_path") or ""),
                str(item.get("source_path") or ""),
                str(item.get("original_filename") or ""),
                str(item.get("description") or "").strip(),
                str(item.get("purpose") or "").strip(),
            ))
        return tuple(rows)

    @staticmethod
    def _size_label(size: int) -> str:
        if size < 1024:
            return f"{size} B"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"

    def _item_path(self, item: dict[str, Any]) -> Path:
        source = str(item.get("source_path") or "")
        if source:
            return Path(source)
        return self.case_dir / str(item.get("stored_path") or "")

    def _store_details(self) -> None:
        if self._selected_index is None or self._selected_index >= len(self.items):
            return
        item = self.items[self._selected_index]
        item["description"] = self.description.get("1.0", "end-1c").strip()
        item["purpose"] = self.purpose.get("1.0", "end-1c").strip()

    def _load_details(self, index: int | None) -> None:
        self.description.configure(state="normal")
        self.purpose.configure(state="normal")
        self.description.delete("1.0", "end")
        self.purpose.delete("1.0", "end")
        self._selected_index = index
        state = "normal" if index is not None and 0 <= index < len(self.items) else "disabled"
        self.description.configure(state=state)
        self.purpose.configure(state=state)
        if state == "normal":
            item = self.items[index]
            self.description.insert("1.0", str(item.get("description") or ""))
            self.purpose.insert("1.0", str(item.get("purpose") or ""))

    def _rebuild_tree(self, select_index: int | None = None) -> None:
        self._selection_guard = True
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.items):
            path = self._item_path(item)
            try:
                size = path.stat().st_size
            except OSError:
                size = int(item.get("size_bytes") or 0)
            filename = str(item.get("original_filename") or path.name)
            suffix = Path(filename).suffix.lower().lstrip(".") or "file"
            description = " ".join(str(item.get("description") or "").split())
            if len(description) > 80:
                description = description[:79].rstrip() + "…"
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(filename, suffix.upper(), self._size_label(size), description or "—"),
            )
        self._selection_guard = False
        if select_index is not None and 0 <= select_index < len(self.items):
            iid = str(select_index)
            self.tree.selection_set(iid)
            self.tree.focus(iid)
            self.tree.see(iid)
            self._load_details(select_index)
        else:
            self._load_details(None)

    def _on_select(self, _event: object) -> None:
        if self._selection_guard:
            return
        self._store_details()
        selection = self.tree.selection()
        if not selection:
            self._load_details(None)
            return
        try:
            index = int(selection[0])
        except ValueError:
            self._load_details(None)
            return
        self._load_details(index)

    def _add_files(self) -> None:
        self._store_details()
        paths = filedialog.askopenfilenames(
            parent=self,
            title="Add case material files",
            filetypes=[
                ("Recommended ZIP package", "*.zip"),
                ("Documents and data", "*.pdf *.docx *.txt *.md *.csv *.xlsx *.xls *.json *.yaml *.yml"),
                ("Images", "*.png *.jpg *.jpeg *.webp *.gif *.tif *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not paths:
            return
        known_sources = {str(Path(str(item.get("source_path"))).resolve()) for item in self.items if item.get("source_path")}
        first_new: int | None = None
        for raw in paths:
            path = Path(raw).resolve()
            if not path.is_file() or str(path) in known_sources:
                continue
            if first_new is None:
                first_new = len(self.items)
            self.items.append({
                "id": None,
                "source_path": str(path),
                "original_filename": path.name,
                "stored_path": None,
                "description": "",
                "purpose": "",
                "size_bytes": path.stat().st_size,
            })
            known_sources.add(str(path))
        self._rebuild_tree(select_index=first_new if first_new is not None else self._selected_index)

    def _remove_selected(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No material selected", "Select a material first.", parent=self)
            return
        self._store_details()
        index = int(selection[0])
        filename = str(self.items[index].get("original_filename") or "selected material")
        confirmed = ask_centered_yes_no(
            self,
            "Remove case material",
            f"Remove {filename} from this case-material set? The saved revision is archived when the material list is committed.",
        )
        try:
            self.grab_set()
        except tk.TclError:
            pass
        if not confirmed:
            return
        self.items.pop(index)
        next_index = min(index, len(self.items) - 1) if self.items else None
        self._rebuild_tree(select_index=next_index)

    def _save(self) -> None:
        self._store_details()
        current = self._snapshot(self.items)
        self.result = {
            "changed": current != self._initial_snapshot,
            "items": [dict(item) for item in self.items],
        }
        self.destroy()


class RouteDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, recommendation: GateValue, gate_status: GateValue, existing: dict[str, Any] | None = None) -> None:
        super().__init__(parent)
        self.title("Route after Add-on Gate")
        self.transient(parent)
        self.grab_set()
        self.result: dict[str, Any] | None = None
        self.recommendation = recommendation
        self.gate_status = gate_status
        existing = existing or {}

        default_route = str(existing.get("route_type") or ("selected_addon" if recommendation.value in SUPPORTED_ADDONS else "core_only"))
        existing_addon = existing.get("selected_addon")
        default_addon = str(existing_addon or (recommendation.value if recommendation.value in SUPPORTED_ADDONS else SUPPORTED_ADDONS[0]))
        self.route_var = tk.StringVar(value=default_route)
        self.addon_var = tk.StringVar(value=default_addon)

        details = ttk.LabelFrame(self, text="Gate information", padding=10)
        details.pack(fill="x", padx=14, pady=(14, 8))
        ttk.Label(details, text=f"Recommended add-on: {recommendation.display_value}", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        ttk.Label(details, text=f"Gate status: {gate_status.display_value}").pack(anchor="w", pady=(3, 0))
        ttk.Label(details, text=f"Read status: {recommendation.status} · key: {recommendation.key_path}").pack(anchor="w", pady=(3, 0))
        if recommendation.source_step is not None:
            ttk.Label(details, text=f"Source: saved output from step #{recommendation.source_step}").pack(anchor="w", pady=(3, 0))
        if existing:
            ttk.Label(details, text=f"Current saved route: {existing.get('route_type')} / {existing.get('selected_addon') or 'none'}").pack(anchor="w", pady=(6, 0))

        ttk.Label(
            self,
            text="The recommendation is used only as a preselection. You may review and change the saved route later.",
            wraplength=570,
        ).pack(anchor="w", padx=14, pady=(2, 8))

        ttk.Radiobutton(self, text="Continue Core-only", variable=self.route_var, value="core_only", command=self._sync).pack(anchor="w", padx=14, pady=4)
        ttk.Radiobutton(self, text="Use exactly one add-on", variable=self.route_var, value="selected_addon", command=self._sync).pack(anchor="w", padx=14, pady=4)

        addon_frame = ttk.Frame(self)
        addon_frame.pack(fill="x", padx=34, pady=6)
        ttk.Label(addon_frame, text="Add-on:").pack(side="left")
        self.addon_box = ttk.Combobox(addon_frame, textvariable=self.addon_var, values=SUPPORTED_ADDONS, width=24)
        self.addon_box.pack(side="left", padx=8)
        self._sync()

        ttk.Label(self, text="Changing a route resets dependent active steps. Existing dependent files are archived before reset.", wraplength=570).pack(anchor="w", padx=14, pady=8)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(4, 14))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save route", command=self._save).pack(side="right")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _sync(self) -> None:
        self.addon_box.configure(state="readonly" if self.route_var.get() == "selected_addon" else "disabled")

    def _save(self) -> None:
        route_type = self.route_var.get()
        selected = self.addon_var.get() if route_type == "selected_addon" else None
        if route_type == "selected_addon" and selected == self.recommendation.value:
            basis = "gate_recommended"
        elif route_type == "core_only" and self.recommendation.value is None and self.recommendation.status in {"no_addon", "not_recommended", "scan_only"}:
            basis = "gate_recommended_core_only"
        elif route_type == "selected_addon":
            basis = "user_override"
        else:
            basis = "manual_user_route"
        self.result = {
            "route_type": route_type,
            "selected_addon": selected,
            "selection_basis": basis,
            "gate_recommendation": {
                "recommended_addon": self.recommendation.value,
                "read_status": self.recommendation.status,
                "key_path": self.recommendation.key_path,
                "raw_value": self.recommendation.raw_value,
                "source_step": self.recommendation.source_step,
                "gate_status": self.gate_status.value,
            },
        }
        self.destroy()


class BinaryLayerRouteDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Misc,
        *,
        title: str,
        layer_name: str,
        recommendation: GateValue,
        use_route: str,
        no_route: str,
        use_label: str,
        no_label: str,
        existing: dict[str, Any] | None = None,
        extra_recommendations: dict[str, GateValue] | None = None,
    ) -> None:
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result: dict[str, Any] | None = None
        self.layer_name = layer_name
        self.recommendation = recommendation
        self.use_route = use_route
        self.no_route = no_route
        self.extra_recommendations = extra_recommendations or {}
        existing = existing or {}

        recommended_use = recommendation.value == layer_name
        default_route = str(existing.get("route_type") or (use_route if recommended_use else no_route))
        self.route_var = tk.StringVar(value=default_route)

        details = ttk.LabelFrame(self, text="Gate information", padding=10)
        details.pack(fill="x", padx=14, pady=(14, 8))
        ttk.Label(details, text=f"Recommended {layer_name} route: {'USE ' + layer_name if recommended_use else 'NULL'}", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        ttk.Label(details, text=f"Read status: {recommendation.status} · key: {recommendation.key_path}").pack(anchor="w", pady=(3, 0))
        if recommendation.source_step is not None:
            ttk.Label(details, text=f"Source: saved output from step #{recommendation.source_step}").pack(anchor="w", pady=(3, 0))
        for label, value in self.extra_recommendations.items():
            readable_label = label.replace("_", " ").capitalize()
            ttk.Label(
                details,
                text=f"{readable_label}: {value.display_value}",
                font=("TkDefaultFont", 9, "bold"),
            ).pack(anchor="w", pady=(6, 0))
            ttk.Label(
                details,
                text=f"Read status: {value.status} · key: {value.key_path}",
                wraplength=540,
            ).pack(anchor="w", pady=(2, 0))
        if existing:
            ttk.Label(details, text=f"Current saved route: {existing.get('route_type')}").pack(anchor="w", pady=(6, 0))

        ttk.Label(self, text=f"Confirm the preselection or choose the other route. You may review and change the saved {layer_name} route later.", wraplength=560).pack(anchor="w", padx=14, pady=(2, 8))
        ttk.Radiobutton(self, text=no_label, variable=self.route_var, value=no_route).pack(anchor="w", padx=14, pady=4)
        ttk.Radiobutton(self, text=use_label, variable=self.route_var, value=use_route).pack(anchor="w", padx=14, pady=4)
        ttk.Label(self, text="Changing a route resets dependent active steps. Existing dependent files are archived before reset.", wraplength=560).pack(anchor="w", padx=14, pady=8)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(12, 14))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save route", command=self._save).pack(side="right")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _save(self) -> None:
        route_type = self.route_var.get()
        self.result = build_binary_layer_route_result(
            layer_name=self.layer_name,
            recommendation=self.recommendation,
            route_type=route_type,
            use_route=self.use_route,
            no_route=self.no_route,
            extra_recommendations=self.extra_recommendations,
        )
        self.destroy()


class MipRouteDialog(BinaryLayerRouteDialog):
    def __init__(self, parent: tk.Misc, details: MipGateDetails, existing: dict[str, Any] | None = None) -> None:
        super().__init__(
            parent,
            title="Route after MIP Gate",
            layer_name="MIP",
            recommendation=details.overall,
            use_route="use_mip",
            no_route="no_mip",
            use_label="Read and apply MIP",
            no_label="Continue without MIP",
            existing=existing,
            extra_recommendations={
                "source_read_recommendation": details.source_read,
                "case_application_recommendation": details.case_application,
            },
        )


class AhpRouteDialog(BinaryLayerRouteDialog):
    def __init__(self, parent: tk.Misc, recommendation: GateValue, existing: dict[str, Any] | None = None) -> None:
        super().__init__(
            parent,
            title="Route after AHP Gate",
            layer_name="AHP",
            recommendation=recommendation,
            use_route="use_ahp",
            no_route="no_ahp",
            use_label="Apply the AHP module",
            no_label="Continue without AHP",
            existing=existing,
        )


class ArticleRouteDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Misc,
        existing: dict[str, Any] | None = None,
        ai_review_steps_enabled: bool = True,
    ) -> None:
        super().__init__(parent)
        self.title("Optional Markdown article")
        self.transient(parent)
        self.grab_set()
        self.result: dict[str, Any] | None = None
        existing = existing or {}

        default_route = str(existing.get("route_type") or "no_article")
        default_profile = str(existing.get("article_profile") or "full_analysis_article")
        if default_profile not in {"case_article", "full_analysis_article"}:
            default_profile = "full_analysis_article"
        self.route_var = tk.StringVar(value=default_route)
        self.profile_var = tk.StringVar(value=default_profile)

        details = ttk.LabelFrame(self, text="Article decision", padding=10)
        details.pack(fill="x", padx=14, pady=(14, 8))
        ttk.Label(
            details,
            text="Is a Markdown case article intended for this case?",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            details,
            text=(
                "Article generation is optional and begins only after the Iteration Handoff step (#26)."
                if ai_review_steps_enabled
                else "Article generation is optional and begins after the Iteration Handoff step (#26). Semantic AI review was disabled by case setting."
            ),
            wraplength=610,
        ).pack(anchor="w", pady=(4, 0))
        if existing:
            profile_label = (
                str(existing.get("article_profile") or "full_analysis_article").replace("_", " ")
                if existing.get("route_type") == "generate_article"
                else "not applicable"
            )
            ttk.Label(
                details,
                text=f"Current saved route: {existing.get('route_type')} · profile: {profile_label}",
            ).pack(anchor="w", pady=(6, 0))

        ttk.Radiobutton(
            self,
            text="Finish the run without a Markdown article",
            variable=self.route_var,
            value="no_article",
            command=self._sync_profile_state,
        ).pack(anchor="w", padx=14, pady=4)
        ttk.Radiobutton(
            self,
            text=(
                "Generate the optional Markdown article (steps #27–#31)"
                if ai_review_steps_enabled
                else "Generate the optional Markdown article (steps #27–#30; final AI review skipped)"
            ),
            variable=self.route_var,
            value="generate_article",
            command=self._sync_profile_state,
        ).pack(anchor="w", padx=14, pady=4)

        profile_frame = ttk.LabelFrame(self, text="Article profile", padding=10)
        profile_frame.pack(fill="x", padx=14, pady=(8, 4))

        self.case_profile_button = ttk.Radiobutton(
            profile_frame,
            text="Case article",
            variable=self.profile_var,
            value="case_article",
        )
        self.case_profile_button.pack(anchor="w")
        ttk.Label(
            profile_frame,
            text=(
                "Focused case-specific prose. Workflow history, generic boundaries, "
                "and inactive-layer inventories are condensed."
            ),
            wraplength=590,
        ).pack(anchor="w", padx=(24, 0), pady=(0, 8))

        self.full_profile_button = ttk.Radiobutton(
            profile_frame,
            text="Full analysis article",
            variable=self.profile_var,
            value="full_analysis_article",
        )
        self.full_profile_button.pack(anchor="w")
        ttk.Label(
            profile_frame,
            text=(
                "Detailed, audit-rich narrative of the checked case record, "
                "including provenance, layer decisions, and bounded non-use records."
            ),
            wraplength=590,
        ).pack(anchor="w", padx=(24, 0))

        ttk.Label(
            self,
            text=(
                "Changing the article decision or profile resets only steps #27–#31. "
                "Existing article files are archived before reset."
            ),
            wraplength=610,
        ).pack(anchor="w", padx=14, pady=8)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(12, 14))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save article decision", command=self._save).pack(side="right")
        self.bind("<Escape>", lambda _event: self.destroy())
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)
        self._sync_profile_state()
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _sync_profile_state(self) -> None:
        state = "normal" if self.route_var.get() == "generate_article" else "disabled"
        self.case_profile_button.configure(state=state)
        self.full_profile_button.configure(state=state)

    def _save(self) -> None:
        route_type = self.route_var.get()
        result: dict[str, Any] = {
            "route_type": route_type,
            "selection_basis": "user_confirmed",
        }
        if route_type == "generate_article":
            result["article_profile"] = self.profile_var.get()
        self.result = result
        self.destroy()


class IterationHandoffNextActionDialog(tk.Toplevel):
    """Contextual action choice after step #26 has been confirmed."""

    def __init__(self, parent: tk.Misc, *, followup_available: bool, reason: str = "") -> None:
        super().__init__(parent)
        self.title("After Iteration Handoff")
        self.transient(parent)
        self.grab_set()
        self.result: str | None = None
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(
            frame,
            text="Step #26 is complete.",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            frame,
            text=(
                "Choose the next controlled action. A follow-up case is available only when the "
                "confirmed Iteration Handoff contains approved effective targets."
            ),
            wraplength=560,
            justify="left",
        ).pack(fill="x", pady=(6, 10))

        if followup_available:
            ttk.Button(
                frame,
                text="Create follow-up case now",
                command=lambda: self._choose("create_followup"),
            ).pack(fill="x", pady=3)
        else:
            ttk.Label(
                frame,
                text=f"Follow-up case creation is not currently available: {reason or 'no approved effective targets.'}",
                wraplength=560,
                justify="left",
            ).pack(fill="x", pady=(0, 8))

        ttk.Button(
            frame,
            text="Continue to article decision",
            command=lambda: self._choose("continue_article"),
        ).pack(fill="x", pady=3)
        ttk.Button(
            frame,
            text="Finish without article",
            command=lambda: self._choose("finish_without_article"),
        ).pack(fill="x", pady=3)
        ttk.Button(
            frame,
            text="Decide later",
            command=lambda: self._choose("decide_later"),
        ).pack(fill="x", pady=(10, 0))

        self.protocol("WM_DELETE_WINDOW", lambda: self._choose("decide_later"))
        self.bind("<Escape>", lambda _event: self._choose("decide_later"))
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _choose(self, value: str) -> None:
        self.result = value
        self.destroy()


class IterationHandoffDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, handoff_text: str) -> None:
        super().__init__(parent)
        self.title("Iteration Handoff review")
        self.transient(parent)
        self.grab_set()
        self.result_text: str | None = None
        self.result_data: dict[str, Any] | None = None
        self.handoff_data = parse_handoff_text(handoff_text)
        self.root_data = handoff_root(self.handoff_data)
        self.target_vars: dict[str, dict[str, Any]] = {}

        self.geometry("1080x780")
        self.minsize(980, 680)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        summary = ttk.LabelFrame(self, text="Model preselection and urgency", padding=10)
        summary.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        summary.columnconfigure(1, weight=1)
        pre = self.root_data.get("model_preselection") if isinstance(self.root_data.get("model_preselection"), dict) else {}
        depth = self.root_data.get("current_depth_assessment") if isinstance(self.root_data.get("current_depth_assessment"), dict) else {}
        urgency = self.root_data.get("iteration_urgency") if isinstance(self.root_data.get("iteration_urgency"), dict) else {}
        coverage = self.root_data.get("minimum_followup_coverage") if isinstance(self.root_data.get("minimum_followup_coverage"), dict) else {}
        rows = [
            ("Current depth", str(depth.get("status") or "unknown")),
            ("Sufficient for original use", str(depth.get("sufficient_for_original_intended_use") or "unknown")),
            ("Model recommendation", str(pre.get("recommendation") or "unknown")),
            ("Urgency", str(urgency.get("level") or "unknown").upper()),
            ("Minimum coverage", str(coverage.get("requirement_summary") or "not specified")),
        ]
        for row_index, (label, value) in enumerate(rows):
            ttk.Label(summary, text=f"{label}:", font=("TkDefaultFont", 9, "bold")).grid(row=row_index, column=0, sticky="nw", padx=(0, 10), pady=2)
            ttk.Label(summary, text=value, wraplength=820).grid(row=row_index, column=1, sticky="ew", pady=2)
        reason_text = self._bullets(urgency.get("reasons"))
        ttk.Label(summary, text="Urgency reasons:", font=("TkDefaultFont", 9, "bold")).grid(row=len(rows), column=0, sticky="nw", padx=(0, 10), pady=(6, 2))
        ttk.Label(summary, text=reason_text or "—", wraplength=820).grid(row=len(rows), column=1, sticky="ew", pady=(6, 2))

        outer = ttk.Frame(self)
        outer.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)
        self.scroll_frame.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))

        decision = ttk.LabelFrame(self.scroll_frame, text="Overall user decision", padding=10)
        decision.pack(fill="x", pady=(0, 8))
        default_decision = str(pre.get("proposed_user_action") or "accept_model_preselection")
        if default_decision not in OVERALL_ACTIONS:
            default_decision = "accept_model_preselection"
        self.overall_var = tk.StringVar(value=default_decision)
        decision_labels = {
            "accept_model_preselection": "Accept model preselection",
            "accept_with_notes_or_revisions": "Accept with target notes/revisions below",
            "prepare_despite_negative_recommendation": "Prepare handoff despite negative/low recommendation",
            "skip_iteration_handoff": "Skip iteration handoff",
            "regenerate_after_revised_focus": "Request regeneration after revised focus",
        }
        for value in OVERALL_ACTIONS:
            ttk.Radiobutton(decision, text=decision_labels[value], variable=self.overall_var, value=value).pack(anchor="w", pady=2)

        targets_frame = ttk.LabelFrame(self.scroll_frame, text="Proposed follow-up questions", padding=10)
        targets_frame.pack(fill="x", pady=(0, 8))
        for target in proposed_targets(self.root_data):
            if not isinstance(target, dict):
                continue
            self._add_target_editor(targets_frame, target)
        if not self.target_vars:
            ttk.Label(targets_frame, text="No model targets were proposed. You may add your own question below.").pack(anchor="w")

        additions = ttk.LabelFrame(self.scroll_frame, text="Additional user notes and trajectory", padding=10)
        additions.pack(fill="x", pady=(0, 8))
        additions.columnconfigure(1, weight=1)
        self.additional_questions = self._text_row(additions, 0, "Additional follow-up questions", height=4)
        self.general_case_notes = self._text_row(additions, 1, "Additional case notes", height=4)
        self.chronology_notes = self._text_row(additions, 2, "Chronology / trajectory notes", height=4)
        self.material_location_notes = self._text_row(additions, 3, "Material-location notes", height=3)
        self.general_handoff_note = self._text_row(additions, 4, "General handoff note", height=3)

        buttons = ttk.Frame(self)
        buttons.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save confirmed handoff", command=self._save).pack(side="right")
        ttk.Label(
            buttons,
            text="User notes guide follow-up preparation. They are not verified facts or current-case findings.",
            wraplength=620,
        ).pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda _event: self.destroy())
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _bullets(self, value: Any) -> str:
        if isinstance(value, list):
            return "\n".join(f"- {item}" for item in value if str(item).strip())
        return str(value or "")

    def _text_row(self, parent: tk.Misc, row: int, label: str, *, height: int) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="nw", padx=(0, 10), pady=4)
        text = tk.Text(parent, height=height, wrap="word")
        text.grid(row=row, column=1, sticky="ew", pady=4)
        return text

    def _add_target_editor(self, parent: tk.Misc, target: dict[str, Any]) -> None:
        summary = target_summary(target)
        target_id = summary["target_id"] or f"target_{len(self.target_vars) + 1}"
        frame = ttk.LabelFrame(parent, text=f"{target_id} · {summary['dimension']} · {summary['blocking_status']}", padding=8)
        frame.pack(fill="x", pady=(0, 8))
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="Model question", font=("TkDefaultFont", 9, "bold")).grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=2)
        ttk.Label(frame, text=summary["question"] or "—", wraplength=780).grid(row=0, column=1, sticky="ew", pady=2)
        ttk.Label(frame, text="Rationale").grid(row=1, column=0, sticky="nw", padx=(0, 10), pady=2)
        ttk.Label(frame, text=summary["basis"] or "—", wraplength=780).grid(row=1, column=1, sticky="ew", pady=2)
        ttk.Label(frame, text="Expected value").grid(row=2, column=0, sticky="nw", padx=(0, 10), pady=2)
        ttk.Label(frame, text=summary["expected_value"] or "—", wraplength=780).grid(row=2, column=1, sticky="ew", pady=2)
        ttk.Label(frame, text="Required material").grid(row=3, column=0, sticky="nw", padx=(0, 10), pady=2)
        ttk.Label(frame, text=summary["required_new_material"] or "—", wraplength=780).grid(row=3, column=1, sticky="ew", pady=2)

        controls = ttk.Frame(frame)
        controls.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 2))
        action_var = tk.StringVar(value="accept")
        ttk.Label(controls, text="Action:").pack(side="left")
        ttk.Combobox(controls, textvariable=action_var, values=USER_ACTIONS, state="readonly", width=10).pack(side="left", padx=(6, 16))
        visibility_var = tk.StringVar(value="exclude")
        ttk.Label(controls, text="Article visibility:").pack(side="left")
        ttk.Combobox(controls, textvariable=visibility_var, values=ARTICLE_VISIBILITY_VALUES, state="readonly", width=10).pack(side="left", padx=(6, 0))

        note = self._target_text(frame, 5, "User note")
        revised = self._target_text(frame, 6, "User version / revised question")
        rationale = self._target_text(frame, 7, "Why this is better or more precise")
        builds = self._target_text(frame, 8, "Relation to prior checked record")
        material = self._target_text(frame, 9, "Additional material needed")
        trajectory = self._target_text(frame, 10, "Trajectory note")
        split = self._target_text(frame, 11, "Split questions, one per line")
        merge = self._target_text(frame, 12, "Merge with target IDs")
        self.target_vars[target_id] = {
            "action": action_var,
            "visibility": visibility_var,
            "note": note,
            "revised_question": revised,
            "revision_rationale": rationale,
            "builds_on_prior_point": builds,
            "additional_material_needed": material,
            "trajectory_note": trajectory,
            "split_questions": split,
            "merge_with_target_ids": merge,
        }

    def _target_text(self, parent: tk.Misc, row: int, label: str) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="nw", padx=(0, 10), pady=2)
        text = tk.Text(parent, height=2, wrap="word")
        text.grid(row=row, column=1, sticky="ew", pady=2)
        return text

    @staticmethod
    def _get_text(widget: tk.Text) -> str:
        return widget.get("1.0", "end-1c").strip()

    def _save(self) -> None:
        target_responses: list[dict[str, Any]] = []
        for target_id, fields in self.target_vars.items():
            item = {
                "target_id": target_id,
                "action": fields["action"].get(),
                "note": self._get_text(fields["note"]),
                "revised_question": self._get_text(fields["revised_question"]),
                "revision_rationale": self._get_text(fields["revision_rationale"]),
                "builds_on_prior_point": self._get_text(fields["builds_on_prior_point"]),
                "additional_material_needed": self._get_text(fields["additional_material_needed"]),
                "trajectory_note": self._get_text(fields["trajectory_note"]),
                "split_questions": self._get_text(fields["split_questions"]),
                "merge_with_target_ids": self._get_text(fields["merge_with_target_ids"]),
                "article_visibility": fields["visibility"].get(),
            }
            target_responses.append(item)
        response = {
            "overall_decision": self.overall_var.get(),
            "target_responses": target_responses,
            "additional_questions": self._get_text(self.additional_questions),
            "general_case_notes": self._get_text(self.general_case_notes),
            "chronology_or_trajectory_notes": self._get_text(self.chronology_notes),
            "material_location_notes": self._get_text(self.material_location_notes),
            "general_handoff_note": self._get_text(self.general_handoff_note),
        }
        updated = apply_user_response(self.handoff_data, response)
        coverage = validate_effective_coverage(updated)
        if not coverage.ok:
            messagebox.showwarning(
                "Iteration coverage incomplete",
                "The confirmed handoff does not meet its urgency-based minimum coverage:\n\n" + "\n".join(f"- {issue}" for issue in coverage.issues),
                parent=self,
            )
            return
        self.result_data = updated
        self.result_text = dump_handoff_yaml(updated)
        self.destroy()


class YamlValidationDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, details: str) -> None:
        super().__init__(parent)
        self.title("Local YAML validation")
        self.transient(parent)
        self.grab_set()

        ttk.Label(
            self,
            text="Structural validation only — this does not evaluate semantic correctness or claim discipline.",
            wraplength=720,
        ).pack(fill="x", padx=14, pady=(14, 8))

        body = tk.Text(self, width=96, height=28, wrap="word")
        body.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        body.insert("1.0", details)
        body.configure(state="disabled")

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Button(buttons, text="Close", command=self.destroy).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.minsize(780, 560)
        self.after_idle(lambda: finalize_dialog(self, parent))


class SourceCheckDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, statuses: list[Any], manifest_path: str) -> None:
        super().__init__(parent)
        self.title("Resource availability")
        self.transient(parent)
        self.grab_set()
        self.result = False

        present_count = sum(1 for item in statuses if item.present)
        total_count = len(statuses)

        ttk.Label(
            self,
            text=f"Resource files present: {present_count} of {total_count}",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 4))
        ttk.Label(
            self,
            text=(
                "This check tests whether each expected source or template file "
                "exists at its configured destination."
            ),
            wraplength=760,
        ).pack(anchor="w", padx=14, pady=(0, 8))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        tree = ttk.Treeview(table_frame, columns=("label", "destination", "status"), show="headings", height=10)
        tree.heading("label", text="Resource")
        tree.heading("destination", text="Destination")
        tree.heading("status", text="Status")
        tree.column("label", width=190, stretch=False)
        tree.column("destination", width=450)
        tree.column("status", width=90, stretch=False, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for item in statuses:
            tree.insert("", "end", values=(item.entry.label, item.entry.destination, "Present" if item.present else "Missing"))

        ttk.Label(self, text=f"URL manifest: {manifest_path}", wraplength=760).pack(anchor="w", padx=14, pady=(0, 10))

        decision = ttk.LabelFrame(self, text="Download resources?", padding=10)
        decision.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Label(
            decision,
            text=(
                "Yes downloads all listed PMS, MIP/AHP, and PMS-DISCIPLINE "
                "YAML sources and templates. Existing files require a separate "
                "replacement confirmation."
            ),
            wraplength=720,
        ).pack(anchor="w", pady=(0, 8))
        buttons = ttk.Frame(decision)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="No", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Yes", command=self._accept).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.minsize(800, 470)
        self.after_idle(lambda: finalize_dialog(self, parent))

    def _accept(self) -> None:
        self.result = True
        self.destroy()
