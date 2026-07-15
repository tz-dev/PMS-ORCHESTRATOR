from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable

from .gate_reader import GateValue
from .registry import SUPPORTED_ADDONS


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


def ask_centered_yes_no(parent: tk.Misc, title: str, message: str) -> bool:
    dialog = ConfirmationDialog(parent, title, message)
    parent.wait_window(dialog)
    return dialog.result


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
        recommended_use = self.recommendation.value == self.layer_name
        if route_type == self.use_route and recommended_use:
            basis = "gate_recommended"
        elif route_type == self.no_route and not recommended_use and self.recommendation.status in {"not_recommended", "ahp_not_recommended", "scan_only"}:
            basis = f"gate_recommended_no_{self.layer_name.lower()}"
        elif route_type == self.use_route:
            basis = "user_requested"
        else:
            basis = "manual_user_route"
        self.result = {
            "route_type": route_type,
            "selection_basis": basis,
            "gate_recommendation": {
                f"recommended_{self.layer_name.lower()}": recommended_use,
                "read_status": self.recommendation.status,
                "key_path": self.recommendation.key_path,
                "raw_value": self.recommendation.raw_value,
                "source_step": self.recommendation.source_step,
            },
        }
        self.destroy()


class MipRouteDialog(BinaryLayerRouteDialog):
    def __init__(self, parent: tk.Misc, recommendation: GateValue, existing: dict[str, Any] | None = None) -> None:
        super().__init__(
            parent,
            title="Route after MIP Gate",
            layer_name="MIP",
            recommendation=recommendation,
            use_route="use_mip",
            no_route="no_mip",
            use_label="Read and apply MIP",
            no_label="Continue without MIP",
            existing=existing,
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
                "Article generation is optional and begins only after checked Case Record Stage 3."
                if ai_review_steps_enabled
                else "Article generation is optional and begins after the unchecked Stage 3 output. Semantic AI review was disabled by case setting."
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
                "Generate the optional Markdown article (steps #26–#30)"
                if ai_review_steps_enabled
                else "Generate the optional Markdown article (steps #26–#29; final AI review skipped)"
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
                "Changing the article decision or profile resets only steps #26–#30. "
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
