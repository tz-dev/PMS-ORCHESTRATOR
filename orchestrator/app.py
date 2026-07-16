from __future__ import annotations

import re
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from .app_metadata import AppMetadata
from .case_materials import (
    CaseMaterialError,
    CaseMaterialStore,
    render_case_material_manifest_block,
    render_case_material_prompt_block,
)
from .dialogs import (
    AhpRouteDialog,
    ArticleRouteDialog,
    CaseDialog,
    MaterialManagerDialog,
    IterationHandoffDialog,
    IterationHandoffNextActionDialog,
    MipRouteDialog,
    RouteDialog,
    SourceCheckDialog,
    YamlValidationDialog,
    ask_centered_yes_no,
)
from .gate_reader import GateValue, read_addon_gate_status, read_addon_recommendation, read_ahp_recommendation, read_mip_recommendation
from .platform_utils import OpenPathError, open_parent, open_path, open_url
from .prompt_source import PromptSource, PromptSourceError, normalize_prompt_text
from .registry import (
    AI_REVIEW_STEP_IDS,
    REVIEW_SOURCE_STEP,
    STEPS,
    StepDefinition,
    get_step,
    is_completed_step_status,
    resolve_upload_files,
)
from .source_manager import SourceDownloadError, SourceManifest, SourceManifestError
from .storage import CaseSession, CaseStore, StorageError
from .ui_views import HelpDocumentDialog, OutputReader, is_markdown_filename, render_markdown
from .yaml_validator import LocalYamlValidator, YamlValidationResult
from .iteration_handoff import (
    IterationHandoffError,
    parse_handoff_text,
    render_article_outlook_handoff,
)


STATUS_MARKS = {
    "completed": "✓",
    "completed_by_runner_no_examples": "✓",
    "current": "▶",
    "draft": "◐",
    "open": "○",
    "locked": "🔒",
    "skipped": "—",
}


class OrchestratorApp(tk.Tk):
    def __init__(self, project_root: Path) -> None:
        super().__init__()
        self.project_root = project_root.resolve()
        self.withdraw()
        self.metadata = AppMetadata.load(self.project_root / "app_metadata.json")
        self.title(f"{self.metadata.name} — Guided Session v{self.metadata.version}")
        self.minsize(1080, 700)

        self.store = CaseStore(self.project_root)
        self.prompt_source = PromptSource(self.project_root / "resources" / "Prompts and Instructions.md")
        self.session: CaseSession | None = None
        self.selected_step_id = 1
        self.file_rows: list[Path | None] = []
        self.current_upload_paths: list[Path] = []
        self.theme_mode = "light"
        self.theme_palette: dict[str, str] = {}
        self.source_manifest_path = self.project_root / "source_manifest.json"
        self.yaml_validation_manifest_path = self.project_root / "yaml_validation_manifest.json"
        self.yaml_validator = LocalYamlValidator(self.project_root, self.yaml_validation_manifest_path)
        self.last_yaml_validation = YamlValidationResult(step_id=1, applicable=False)
        self._button_flash_jobs: dict[str, str] = {}
        self._yaml_highlight_after_id: str | None = None
        self._yaml_validation_after_id: str | None = None
        self._pending_new_case_materials: list[
            dict[str, object]
        ] = []

        self._build_menu()
        self._build_ui()
        self._apply_theme()
        self._set_no_case_state()
        self._center_on_screen(1420, 920)
        self.deiconify()
        self.protocol("WM_DELETE_WINDOW", self.exit_app)

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New case…", command=self.new_case)
        file_menu.add_command(label="Open case…", command=self.open_case)
        file_menu.add_command(label="Edit case…", command=self.edit_case)
        file_menu.add_separator()
        file_menu.add_command(label="Open case folder", command=self.open_case_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Check sources…", command=self.check_sources)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu.add_cascade(label="File", menu=file_menu)

        routes_menu = tk.Menu(menu, tearoff=False)
        routes_menu.add_command(label="Review Add-on route…", command=self.set_addon_route)
        routes_menu.add_command(label="Review MIP route…", command=self.set_mip_route)
        routes_menu.add_command(label="Review AHP route…", command=self.set_ahp_route)
        routes_menu.add_command(label="Review article decision…", command=self.set_article_route)
        menu.add_cascade(label="Routes", menu=routes_menu)

        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label="PMS-ORCHESTRATOR Guide", command=self.show_guide)
        help_menu.add_command(label="Keyboard and mouse controls", command=self.show_controls)
        help_menu.add_separator()
        help_menu.add_command(label="Open project folder", command=self.open_project_folder)
        help_menu.add_command(
            label="Open GitHub repository",
            command=self.open_github_repository,
            state="normal" if self.metadata.repository_url else "disabled",
        )
        help_menu.add_separator()
        help_menu.add_command(label="About PMS-ORCHESTRATOR", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)
        self.configure(menu=menu)

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self, padding=(8, 6))
        toolbar.pack(fill="x")

        self.exit_button = ttk.Button(toolbar, text="Exit", command=self.exit_app)
        self.exit_button.pack(side="right")

        self.theme_button = ttk.Button(toolbar, text="Switch to dark mode", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=(0, 8))

        ttk.Button(toolbar, text="New case", command=self.new_case).pack(side="left")
        ttk.Button(toolbar, text="Open case", command=self.open_case).pack(side="left", padx=(6, 0))
        ttk.Button(toolbar, text="Edit case", command=self.edit_case).pack(side="left", padx=(6, 0))
        ttk.Button(toolbar, text="Case folder", command=self.open_case_folder).pack(side="left", padx=(6, 0))

        ttk.Separator(toolbar, orient="vertical").pack(
            side="left",
            fill="y",
            padx=10,
            pady=2,
        )

        self.materials_button = ttk.Button(toolbar, text="Add materials", command=self.manage_materials)
        self.materials_button.pack(side="left")
        ttk.Button(toolbar, text="Check sources", command=self.check_sources).pack(side="left", padx=(6, 0))

        ttk.Separator(toolbar, orient="vertical").pack(
            side="left",
            fill="y",
            padx=10,
            pady=2,
        )

        self.iteration_handoff_review_button = ttk.Button(toolbar, text="Review Hand-off", command=self.review_iteration_handoff)
        self.iteration_handoff_review_button.pack(side="left")
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=10, pady=2)

        self.mip_review_button = ttk.Button(toolbar, text="Review MIP route", command=self.set_mip_route)
        self.mip_review_button.pack(side="left")
        self.ahp_review_button = ttk.Button(toolbar, text="Review AHP route", command=self.set_ahp_route)
        self.ahp_review_button.pack(side="left", padx=(6, 0))
        self.article_review_button = ttk.Button(toolbar, text="Review article decision", command=self.set_article_route)
        self.article_review_button.pack(side="left", padx=(6, 0))

        self.case_summary = ttk.Label(self, text="No case loaded", padding=(10, 4), anchor="w")
        self.case_summary.pack(fill="x")

        # Keep one persistent action/status line at the physical bottom edge.
        # It is packed before the expandable main pane so the pane can never
        # consume the space reserved for status feedback.
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Frame(self)
        self.status_bar.pack(fill="x", side="bottom")
        ttk.Separator(self.status_bar, orient="horizontal").pack(fill="x", side="top")
        status_content = ttk.Frame(self.status_bar, padding=(8, 4))
        status_content.pack(fill="x")
        ttk.Label(status_content, text="Status:", font=("TkDefaultFont", 9, "bold")).pack(side="left")
        self.status_label = ttk.Label(status_content, textvariable=self.status_var, anchor="w", padding=(6, 0))
        self.status_label.pack(side="left", fill="x", expand=True)

        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        left = ttk.Frame(paned, padding=6)
        right = ttk.Frame(paned, padding=6)
        paned.add(left, weight=1)
        paned.add(right, weight=4)

        ttk.Label(left, text="Pipeline — Guided Session through Step #31").pack(anchor="w", pady=(0, 6))
        self.step_tree = ttk.Treeview(
            left,
            columns=("mark", "step", "title"),
            show="headings",
            selectmode="browse",
            height=30,
        )
        self.step_tree.heading("mark", text="")
        self.step_tree.heading("step", text="Step")
        self.step_tree.heading("title", text="Title")
        self.step_tree.column("mark", width=42, minwidth=42, stretch=False, anchor="center")
        self.step_tree.column("step", width=58, minwidth=58, stretch=False, anchor="center")
        self.step_tree.column("title", width=285, minwidth=180, stretch=False, anchor="w")
        step_scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.step_tree.yview)
        self.step_tree.configure(yscrollcommand=step_scrollbar.set)
        self.step_tree.pack(side="left", fill="both", expand=True)
        step_scrollbar.pack(side="right", fill="y")
        self.step_tree.bind("<<TreeviewSelect>>", self._on_step_select)

        step_header = ttk.Frame(right)
        step_header.pack(fill="x")
        self.step_title = ttk.Label(step_header, text="", font=("TkDefaultFont", 12, "bold"))
        self.step_title.pack(side="left", anchor="w", fill="x", expand=True)
        self.reset_steps_button = ttk.Button(
            step_header,
            text="Reset this and following steps",
            command=self.reset_selected_step,
        )
        self.reset_steps_button.pack(side="right", padx=(8, 0))
        self.step_status = ttk.Label(right, text="")
        self.step_status.pack(anchor="w", fill="x", pady=(2, 8))

        file_frame = ttk.LabelFrame(right, text="Files for this step", padding=6)
        file_frame.pack(fill="x", pady=(0, 8))
        self.upload_summary = ttk.Label(file_frame, text="", anchor="w")
        self.upload_summary.pack(fill="x", pady=(0, 4))
        self.file_tree = ttk.Treeview(
            file_frame,
            columns=("role", "file", "state"),
            show="headings",
            height=6,
            selectmode="browse",
        )
        self.file_tree.heading("role", text="Role")
        self.file_tree.heading("file", text="Filename")
        self.file_tree.heading("state", text="Status")
        self.file_tree.column("role", width=210, stretch=False)
        self.file_tree.column("file", width=610)
        self.file_tree.column("state", width=110, stretch=False)
        self.file_tree.pack(fill="x", expand=True)
        file_buttons = ttk.Frame(file_frame)
        file_buttons.pack(fill="x", pady=(6, 0))
        ttk.Button(file_buttons, text="Open selected file", command=self.open_selected_file).pack(side="left")
        ttk.Button(file_buttons, text="Open selected folder", command=self.open_selected_file_folder).pack(side="left", padx=6)

        vertical = ttk.Panedwindow(right, orient="vertical")
        vertical.pack(fill="both", expand=True)
        prompt_frame = ttk.LabelFrame(vertical, text="Rendered prompt", padding=6)
        output_frame = ttk.LabelFrame(vertical, text="AI service output", padding=6)
        vertical.add(prompt_frame, weight=1)
        vertical.add(output_frame, weight=1)

        prompt_buttons = ttk.Frame(prompt_frame)
        prompt_buttons.pack(fill="x", pady=(0, 4))
        self.copy_prompt_button = ttk.Button(prompt_buttons, text="Copy prompt", command=self.copy_prompt)
        self.copy_prompt_button.pack(side="left")
        self.prompt_view_var = tk.StringVar(value="preview")
        prompt_view_controls = ttk.Frame(prompt_buttons)
        prompt_view_controls.pack(side="right")
        ttk.Label(prompt_view_controls, text="View:").pack(side="left", padx=(10, 4))
        self.prompt_raw_button = ttk.Radiobutton(
            prompt_view_controls, text="Raw", variable=self.prompt_view_var, value="raw", command=self._sync_prompt_view
        )
        self.prompt_raw_button.pack(side="left")
        self.prompt_preview_button = ttk.Radiobutton(
            prompt_view_controls, text="Preview", variable=self.prompt_view_var, value="preview", command=self._sync_prompt_view
        )
        self.prompt_preview_button.pack(side="left")
        self.prompt_text = ScrolledText(prompt_frame, wrap="word", height=18, undo=False)
        self.prompt_preview = ScrolledText(prompt_frame, wrap="word", height=18, undo=False)
        self.prompt_preview.pack(fill="both", expand=True)
        self.prompt_text.bind("<Button-3>", self._copy_prompt_event)
        self.prompt_preview.bind("<Button-3>", self._copy_prompt_event)

        output_buttons = ttk.Frame(output_frame)
        output_buttons.pack(fill="x", pady=(0, 4))
        ttk.Button(output_buttons, text="Import response file", command=self.import_output).pack(side="left")
        self.save_button = ttk.Button(output_buttons, text="Save changes", command=self.save_draft)
        self.save_button.pack(side="left", padx=6)
        self.open_output_reader_button = ttk.Button(output_buttons, text="Open output reader", command=self.open_output_reader)
        self.open_output_reader_button.pack(side="left")
        self.output_view_var = tk.StringVar(value="raw")
        self.output_view_label = ttk.Label(output_buttons, text="View:")
        self.output_view_label.pack(side="left", padx=(12, 4))
        self.output_raw_button = ttk.Radiobutton(
            output_buttons, text="Raw", variable=self.output_view_var, value="raw", command=self._sync_output_view
        )
        self.output_raw_button.pack(side="left")
        self.output_preview_button = ttk.Radiobutton(
            output_buttons, text="Preview", variable=self.output_view_var, value="preview", command=self._sync_output_view
        )
        self.output_preview_button.pack(side="left")
        self.complete_button = ttk.Button(output_buttons, text="Save output and complete step", command=self.complete_step)
        self.complete_button.pack(side="right")

        validation_frame = ttk.Frame(output_frame)
        validation_frame.pack(fill="x", pady=(0, 4))
        self.yaml_validation_var = tk.StringVar(value="YAML validation: Not applicable for this step.")
        self.yaml_validation_label = ttk.Label(validation_frame, textvariable=self.yaml_validation_var, anchor="w")
        self.yaml_validation_label.pack(side="left", fill="x", expand=True)
        self.yaml_validate_corrected_button = ttk.Button(
            validation_frame,
            text="Validate corrected YAML",
            command=self.validate_corrected_yaml,
        )
        self.yaml_validation_details_button = ttk.Button(
            validation_frame,
            text="View validation details",
            command=self.show_yaml_validation_details,
        )
        self.yaml_validation_details_button.pack(side="right", padx=(8, 0))

        self.output_text = ScrolledText(output_frame, wrap="word", height=18, undo=True)
        self.output_preview = ScrolledText(output_frame, wrap="word", height=18, undo=False)
        self.output_text.pack(fill="both", expand=True)
        self.output_text.bind("<<Modified>>", self._on_output_modified)
        self.output_text.bind("<Button-3>", self._paste_output_event)
        self.output_preview.bind("<Button-3>", self._paste_output_event)
        self.output_text.edit_modified(False)

    def _copy_prompt_event(self, _event: object) -> str:
        self.copy_prompt()
        return "break"

    def _paste_output_event(self, _event: object) -> str:
        self._paste_output_from_clipboard()
        return "break"

    def _paste_output_from_clipboard(self) -> None:
        if self.session is None:
            self._set_status("Paste output skipped: no case is loaded.")
            return
        try:
            text = self.clipboard_get()
        except tk.TclError:
            self._set_status("Paste output skipped: the clipboard does not contain text.")
            return
        if self.output_view_var.get() != "raw":
            self.output_view_var.set("raw")
            self._sync_output_view()
        try:
            self.output_text.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        self.output_text.insert("insert", text)
        self.output_text.edit_modified(True)
        self._apply_yaml_highlighting()
        validation = self._validate_output()
        self._set_status(f"Output pasted from clipboard · {validation.short_summary()}")

    def _sync_prompt_view(self) -> None:
        if self.prompt_view_var.get() == "preview":
            self.prompt_text.pack_forget()
            self.prompt_preview.pack(fill="both", expand=True)
            self._render_prompt_preview()
        else:
            self.prompt_preview.pack_forget()
            self.prompt_text.pack(fill="both", expand=True)


    def _iteration_outlook_article_handoff(self) -> str:
        assert self.session is not None
        if not hasattr(self.session, "output_path"):
            return "ITERATION OUTLOOK HANDOFF — RUNNER-GENERATED\nrender_iteration_outlook: no\nreason: no runtime case session is available for step #26 lookup.\nEND ITERATION OUTLOOK HANDOFF"
        path = self.session.output_path(26)
        if not path.is_file():
            return "ITERATION OUTLOOK HANDOFF — RUNNER-GENERATED\nrender_iteration_outlook: no\nreason: step #26 Iteration Handoff output is absent.\nEND ITERATION OUTLOOK HANDOFF"
        try:
            return render_article_outlook_handoff(path.read_text(encoding="utf-8-sig", errors="replace"), profile=self.session.article_profile)
        except (IterationHandoffError, OSError) as exc:
            return (
                "ITERATION OUTLOOK HANDOFF — RUNNER-GENERATED\n"
                "render_iteration_outlook: no\n"
                f"reason: step #26 Iteration Handoff could not be parsed safely: {exc}\n"
                "Article prompts must ignore Iteration Handoff content when this block is unsafe.\n"
                "END ITERATION OUTLOOK HANDOFF"
            )

    def _article_profile_contract(self, step_id: int) -> str:
        assert self.session is not None
        profile = self.session.article_profile
        common = [
            "ARTICLE PROFILE — RUNNER-GENERATED",
            f"selected_profile: {profile}",
            "The selected profile controls presentation depth and section structure only.",
            "It does not change the checked analysis, route state, source status, claim ceiling, unresolved items, or authority boundary.",
            "",
            "CANONICAL PMS OPERATOR NAMING RULE",
            "- Use the canonical PMS operator names exactly:",
            "  Δ (Difference), ∇ (Impulse), □ (Frame), Λ (Non-Event),",
            "  Α (Attractor), Ω (Asymmetry), Θ (Temporality),",
            "  Φ (Recontextualization), Χ (Distance), Σ (Integration),",
            "  Ψ (Self-Binding).",
            "- In article prose, the first occurrence of each operator in every paragraph must be followed by its canonical English name in parentheses.",
            "- When the symbol is emphasized, emphasize the symbol only, for example: `**Δ** (Difference)`.",
            "- Later occurrences of the same operator within that paragraph may use the symbol alone.",
            "- When several operators first occur in the same paragraph, label every one of them.",
            "- Symbolic formulas may remain symbol-only. The first prose occurrence in the paragraph must still use the canonical name.",
            "- Do not replace a canonical operator name with a case-specific gloss. Place the case-specific explanation after the canonical name.",
            "",
        ]
        if profile == "case_article":
            common.extend([
                "CASE ARTICLE CONTRACT",
                "- Produce a focused, readable, standalone case article.",
                "- Preserve the case-specific structural movement, active-layer contribution, controlling boundary, rival pressure, weakening conditions, and reopening conditions.",
                "- Use Stage 1 for provenance control, not as a visible audit narrative unless a provenance issue materially limits reliability.",
                "- Do not include an audit-style case capsule, full source-chain inventory, workflow correction history, report-readiness planning, examples-policy planning, or a generic misuse catalogue.",
                "- Center the structural reading on the operators that carry the case's main movement.",
                "- Group weak, conditional, dependency-limited, inactive, or analytic-only operators by shared calibration function unless one contributes a distinct case-specific result.",
                "- Do not create a separate paragraph or subsection for an operator merely to show that it was considered.",
                "- Do not narrate every inactive add-on, MIP, or AHP branch. Mention non-use only when it prevents a case-specific false trigger or materially explains the result.",
                "- Keep the case-specific boundary normally to the two to four misuse or escalation risks nearest to the material and actual analysis.",
                "- Mention broader legal, clinical, forensic, HR, automated-decision, publication, or institutional-use boundaries only when the case, intended use, active layer, or checked record creates concrete proximity to that misuse.",
                "- Do not restore generic boundary language already expressed elsewhere in the article. State each relevant limit once.",
                "- Omission of generic workflow history, inactive-layer inventories, repeated non-authority language, and non-material provenance detail is intentional compression, not source loss.",
                "- Normal guidance is approximately 1,500–3,500 words, but analytical sufficiency controls; there is no minimum length.",
                "- This profile-specific contract overrides any generic long-form structure or minimum-depth wording elsewhere in the prompt.",
            ])
        else:
            common.extend([
                "FULL ANALYSIS ARTICLE CONTRACT",
                "- Produce a detailed, audit-rich narrative rendering of the checked case-record chain.",
                "- Preserve provenance, branch decisions, layer status, claim boundaries, non-use records, rival pressure, weakening conditions, and reopening conditions where they matter.",
                "- Detailed does not mean repetitive. State each provenance fact, route decision, boundary, non-use result, and non-authority warning once at the point where it contributes most.",
                "- Do not import temporary runner execution metadata, local installation inventory, or drafting metadata into article prose.",
                "- Normal guidance is approximately 5,000–8,000 words; multi-layer cases may be longer when the checked record requires it. There is no artificial minimum.",
            ])
        common.extend([
            "",
            self._iteration_outlook_article_handoff(),
            "",
            f"CURRENT ARTICLE STEP: {step_id}",
            "END ARTICLE PROFILE",
        ])
        return "\n".join(common)

    def _render_prompt_preview(self) -> None:
        if not hasattr(self, "prompt_preview"):
            return
        render_markdown(
            self.prompt_preview,
            self.prompt_text.get("1.0", "end-1c"),
            self.theme_palette or {"fg": "#202124", "muted": "#5f6368", "panel": "#ffffff"},
        )

    def _output_supports_preview(self, step_id: int | None = None) -> bool:
        target_step_id = self.selected_step_id if step_id is None else step_id
        return is_markdown_filename(get_step(target_step_id).output_filename)

    def _sync_output_view_controls(self, step_id: int | None = None) -> None:
        supports_preview = bool(self.session) and self._output_supports_preview(step_id)
        self.output_preview_button.configure(state="normal" if supports_preview else "disabled")
        if supports_preview:
            self.output_view_var.set("preview")
        else:
            self.output_view_var.set("raw")

    def _sync_output_view(self) -> None:
        supports_preview = bool(self.session) and self._output_supports_preview()
        if self.output_view_var.get() == "preview" and supports_preview:
            self.output_text.pack_forget()
            self.output_preview.pack(fill="both", expand=True)
            self._render_output_preview()
        else:
            self.output_view_var.set("raw")
            self.output_preview.pack_forget()
            self.output_text.pack(fill="both", expand=True)

    def _render_output_preview(self) -> None:
        if not hasattr(self, "output_preview"):
            return
        render_markdown(
            self.output_preview,
            self.output_text.get("1.0", "end-1c"),
            self.theme_palette or {"fg": "#202124", "muted": "#5f6368", "panel": "#ffffff"},
        )

    def open_output_reader(self) -> None:
        if self.session is None:
            self._set_status("Output reader skipped: no case is loaded.")
            return
        text = self.output_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_status("Output reader opened with an empty output.")
        applicable, _profile_step, _review_yaml = self._yaml_validation_context(text=text)
        if applicable:
            content_kind = "yaml"
        elif self._output_supports_preview():
            content_kind = "markdown"
        else:
            content_kind = "text"
        step = get_step(self.selected_step_id)
        OutputReader(
            self,
            title=f"Step #{step.step_id} output — {step.title}",
            content=text,
            content_kind=content_kind,
            palette=self.theme_palette,
        )
        self._set_status(f"Output reader opened for step #{step.step_id}.")

    def show_guide(self) -> None:
        HelpDocumentDialog(self, "PMS-ORCHESTRATOR Guide", self._guide_markdown())
        self._set_status("Opened PMS-ORCHESTRATOR Guide.")

    def show_controls(self) -> None:
        HelpDocumentDialog(self, "Keyboard and mouse controls", self._controls_markdown())
        self._set_status("Opened keyboard and mouse controls.")

    def open_project_folder(self) -> None:
        if self._safe_open(self.project_root):
            self._set_status(f"Opened project folder: {self.project_root.name}")

    def open_github_repository(self) -> None:
        try:
            open_url(self.metadata.repository_url)
            self._set_status("Opened GitHub repository.")
        except OpenPathError as exc:
            messagebox.showerror("Could not open GitHub repository", str(exc), parent=self)

    def show_about(self) -> None:
        license_text = self.metadata.read_license(self.project_root)
        repository = self.metadata.repository_url or "Not configured"
        markdown = (
            f"# {self.metadata.name}\n\n"
            f"**Version:** {self.metadata.version}\n\n"
            f"**Project status:** {self.metadata.project_status}\n\n"
            f"**Repository:** `{repository}`\n\n"
            "**Runtime:** Python with Tkinter.\n\n"
            "**AI connection:** None. The application is a service-independent, human-guided runner. "
            "Prompts are copied to an external AI service manually, and outputs are pasted or imported manually.\n\n"
            f"## License file: {self.metadata.license_file}\n\n"
            f"```text\n{license_text}\n```"
        )
        HelpDocumentDialog(self, "About PMS-ORCHESTRATOR", markdown)
        self._set_status("Opened About PMS-ORCHESTRATOR.")

    @staticmethod
    def _guide_markdown() -> str:
        return """# PMS-ORCHESTRATOR Guide

## Guided Session

The runner presents exactly one valid pipeline step at a time. Copy the rendered prompt, upload the listed files to the AI service, paste or import the response, then save or complete the step.

## Full Review and Fast Mode

- **Full Review:** semantic AI review steps such as #3, #5, and #7 remain active.
- **Fast Mode:** unfinished semantic AI review steps are skipped. Route decisions remain human-confirmed, and local YAML validation can remain active.

## Local YAML validation

Local validation checks YAML syntax, duplicate keys, expected key structure, basic types, and explicitly allowed values. It does not evaluate case meaning or claim quality.

- A **green check** means the step completed without unresolved local YAML findings.
- A **yellow check** means the step completed with findings that remain part of the record.
- Clean corrected YAML in a review step can resolve the downstream handoff while preserving the original finding history.

## Route reviews

Add-on, MIP, AHP, and article routes are always confirmed by the user. Saved routes can be reviewed later. A changed route archives and resets only dependent work.

## Reset and resume

Use **Reset this and following steps** to reopen a completed or current step. Existing dependent prompts, outputs, and validation reports are archived under the case history before reset. Cases can be reopened later from their case folder.

## Case materials

Use **Add materials** to copy case-specific files into the active case. ZIP is recommended for related document packages. Each material can carry a description of its contents and its purpose in the case. Configured materials are uploaded and read with PMS.yaml in step #1. Changing materials after step #1 has begun requires a reset from step #1 so later outputs cannot silently rely on a different source packet.

## Sources

**Check sources** tests whether the configured PMS, MIP/AHP, and PMS-DISCIPLINE YAML source and template files exist. Downloads use `source_manifest.json` and never silently overwrite existing sources.

## Case Record

Stages 1–3 preserve the actual artifact chain, layer digests, route non-use, limits, correctability, and full-record integration. Stage 1 lists selected run resources rather than reproducing the complete local installation inventory. Current production outputs are not treated as their own upstream inputs.

## Iteration Handoff and article workflow

After Case Record Stages 1–3, step #26 prepares an optional Iteration Handoff. The user reviews the model preselection, urgency, targets, and notes before it can feed an article outlook or a separately bounded follow-up case. The handoff is not Case Record Stage 4 and does not change the checked analysis.

Use **Review Hand-off** after step #26 has completed to reopen the contextual handoff-action dialog without resetting the step or pasting the YAML again. This can create an approved follow-up case, continue to the article decision, finish without article, or defer the decision.

Article generation is optional after the Iteration Handoff. Choose **Case article** for focused case-specific prose or **Full analysis article** for a detailed, audit-rich rendering. The profile changes only steps #27–#31 and does not change the checked analysis or approved handoff. Markdown outputs open in Preview by default. When no examples are needed, the runner copies the base article to the final-article step without an unnecessary model rewrite.

## Non-authority

The runner does not validate truth, authorize claims, make route decisions automatically, or connect to an AI service. Human judgment remains controlling."""

    @staticmethod
    def _controls_markdown() -> str:
        return """# Keyboard and mouse controls

## Main window

- **Right-click in the prompt area:** copy the raw prompt.
- **Right-click in the output area:** paste clipboard text into the raw output editor.
- **Raw / Preview:** switch between exact source text and rendered Markdown where Preview is available.

## Output reader

- **F11:** enter or leave full-screen mode.
- **Esc:** leave full-screen mode; when not full-screen, close the reader.
- **Ctrl+A:** select all displayed text.
- **Find:** highlight every case-insensitive match in the displayed reader content.
- **Wrap:** toggle line wrapping.

## Editing and saving

- **Copy prompt:** copies raw prompt text even while Preview is displayed.
- **Save changes:** stores the current raw output without completing the step.
- **Save output and complete step:** stores raw output, records local validation state, and advances the pipeline.
- **Open output reader:** opens a maximized, read-only view with YAML colors or Markdown Preview as appropriate."""

    def _center_on_screen(self, preferred_width: int, preferred_height: int) -> None:
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = min(preferred_width, max(900, screen_width - 80))
        height = min(preferred_height, max(650, screen_height - 80))
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def _shorten(value: object, limit: int) -> str:
        text = " ".join(str(value or "").split())
        if len(text) <= limit:
            return text
        return text[: max(1, limit - 1)].rstrip() + "…"

    def _flash_button(self, button: ttk.Button, temporary_text: str, normal_text: str) -> None:
        key = str(button)
        previous_job = self._button_flash_jobs.pop(key, None)
        if previous_job is not None:
            try:
                self.after_cancel(previous_job)
            except tk.TclError:
                pass
        button.configure(text=temporary_text)

        def restore() -> None:
            self._button_flash_jobs.pop(key, None)
            if button.winfo_exists():
                button.configure(text=normal_text)

        self._button_flash_jobs[key] = self.after(2000, restore)

    def _step_expects_yaml(self, step_id: int | None = None) -> bool:
        target_step_id = self.selected_step_id if step_id is None else step_id
        return get_step(target_step_id).output_filename.lower().endswith((".yaml", ".yml"))

    def _review_yaml_profile_step(self, step_id: int | None = None) -> int | None:
        target_step_id = self.selected_step_id if step_id is None else step_id
        source_step_id = REVIEW_SOURCE_STEP.get(target_step_id)
        if source_step_id is None or not self._step_expects_yaml(source_step_id):
            return None
        return source_step_id

    def _yaml_validation_context(self, step_id: int | None = None, text: str | None = None) -> tuple[bool, int | None, bool]:
        target_step_id = self.selected_step_id if step_id is None else step_id
        if self._step_expects_yaml(target_step_id):
            return True, target_step_id, False
        source_step_id = self._review_yaml_profile_step(target_step_id)
        if source_step_id is None:
            return False, None, False
        candidate = self.output_text.get("1.0", "end-1c") if text is None and hasattr(self, "output_text") else (text or "")
        if self.yaml_validator.is_complete_yaml_mapping_or_sequence(candidate):
            return True, source_step_id, True
        return False, source_step_id, True

    def _configure_yaml_tags(self) -> None:
        if not hasattr(self, "output_text"):
            return
        if self.theme_mode == "dark":
            colors = {
                "yaml_key": "#79c0ff",
                "yaml_string": "#a5d6ff",
                "yaml_number": "#ffa657",
                "yaml_literal": "#ff7b72",
                "yaml_comment": "#8b949e",
                "yaml_marker": "#d2a8ff",
            }
        else:
            colors = {
                "yaml_key": "#0550ae",
                "yaml_string": "#0a3069",
                "yaml_number": "#953800",
                "yaml_literal": "#cf222e",
                "yaml_comment": "#6e7781",
                "yaml_marker": "#8250df",
            }
        for tag_name, color in colors.items():
            self.output_text.tag_configure(tag_name, foreground=color)
        self.output_text.tag_raise("yaml_comment")
        self.output_text.tag_raise("yaml_string")

    def _clear_yaml_highlighting(self) -> None:
        if not hasattr(self, "output_text"):
            return
        for tag_name in ("yaml_key", "yaml_string", "yaml_number", "yaml_literal", "yaml_comment", "yaml_marker"):
            self.output_text.tag_remove(tag_name, "1.0", "end")

    def _apply_yaml_highlighting(self) -> None:
        self._yaml_highlight_after_id = None
        content = self.output_text.get("1.0", "end-1c")
        applicable, _profile_step_id, _is_review_yaml = self._yaml_validation_context(text=content)
        if not applicable:
            self._clear_yaml_highlighting()
            return
        self._configure_yaml_tags()
        self._clear_yaml_highlighting()
        if not content:
            return

        patterns: tuple[tuple[str, re.Pattern[str], int], ...] = (
            ("yaml_marker", re.compile(r"(?m)^\s*(?:---|\.\.\.)\s*$"), 0),
            ("yaml_key", re.compile(r"(?m)^\s*(?:-\s+)?([A-Za-z0-9_.-]+)(?=\s*:)") , 1),
            ("yaml_string", re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\'\'|[^\'])*\''), 0),
            ("yaml_number", re.compile(r"(?<![A-Za-z0-9_.-])-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b"), 0),
            ("yaml_literal", re.compile(r"(?i)\b(?:true|false|null|none|yes|no|unknown|not_applicable|unresolved)\b"), 0),
            ("yaml_comment", re.compile(r"(?m)(?<!\S)#.*$"), 0),
        )
        for tag_name, pattern, group in patterns:
            for match in pattern.finditer(content):
                start, stop = match.span(group)
                self.output_text.tag_add(tag_name, f"1.0+{start}c", f"1.0+{stop}c")

    def _schedule_yaml_highlighting(self) -> None:
        if self._yaml_highlight_after_id is not None:
            try:
                self.after_cancel(self._yaml_highlight_after_id)
            except tk.TclError:
                pass
        self._yaml_highlight_after_id = self.after(250, self._apply_yaml_highlighting)

    def _on_output_modified(self, _event: object) -> None:
        if not self.output_text.edit_modified():
            return
        self.output_text.edit_modified(False)
        self._schedule_yaml_highlighting()
        self._schedule_yaml_validation()
        if hasattr(self, "output_view_var") and self.output_view_var.get() == "preview":
            self.after_idle(self._render_output_preview)

    def _schedule_yaml_validation(self) -> None:
        if self._yaml_validation_after_id is not None:
            try:
                self.after_cancel(self._yaml_validation_after_id)
            except tk.TclError:
                pass
        self._yaml_validation_after_id = self.after(450, self._validate_output)

    def _sync_corrected_yaml_button(self, *, is_review_yaml: bool, applicable: bool) -> None:
        if not hasattr(self, "yaml_validate_corrected_button"):
            return
        if self._review_yaml_profile_step() is None:
            if self.yaml_validate_corrected_button.winfo_manager():
                self.yaml_validate_corrected_button.pack_forget()
            return
        if not self.yaml_validate_corrected_button.winfo_manager():
            self.yaml_validate_corrected_button.pack(side="right", padx=(8, 0), before=self.yaml_validation_details_button)
        can_validate = bool(
            is_review_yaml
            and applicable
            and self.session
            and self.session.local_yaml_validation_enabled
            and self.yaml_validator.dependency_available
        )
        self.yaml_validate_corrected_button.configure(state="normal" if can_validate else "disabled")

    def _validate_output(self) -> YamlValidationResult:
        self._yaml_validation_after_id = None
        enabled = bool(self.session and self.session.local_yaml_validation_enabled)
        selected_addon = self.session.selected_addon if self.session else None
        text = self.output_text.get("1.0", "end-1c") if hasattr(self, "output_text") else ""
        applicable, profile_step_id, is_review_yaml = self._yaml_validation_context(text=text)
        result = self.yaml_validator.validate(
            step_id=self.selected_step_id,
            text=text,
            expects_yaml=applicable,
            enabled=enabled,
            selected_addon=selected_addon,
            profile_step_id=profile_step_id,
        )
        if self._review_yaml_profile_step() is not None and not applicable:
            result.note = "The entire check output must be one parseable YAML mapping or sequence before corrected-YAML validation applies."
        self.last_yaml_validation = result
        if hasattr(self, "yaml_validation_var"):
            if self._review_yaml_profile_step() is not None and not applicable:
                self.yaml_validation_var.set("YAML validation: Waiting for a complete corrected YAML document.")
            else:
                self.yaml_validation_var.set(result.short_summary())
            details_available = result.applicable and result.enabled
            self.yaml_validation_details_button.configure(state="normal" if details_available else "disabled")
            self._sync_corrected_yaml_button(is_review_yaml=is_review_yaml, applicable=applicable)
        return result

    def validate_corrected_yaml(self) -> None:
        result = self._validate_output()
        if not result.applicable:
            self._set_status("Corrected YAML validation is available only when the complete check output is one YAML mapping or sequence.")
            return
        self._apply_yaml_highlighting()
        dialog = YamlValidationDialog(self, result.detailed_text())
        self.wait_window(dialog)
        self._set_status(result.short_summary())

    def show_yaml_validation_details(self) -> None:
        result = self._validate_output()
        if not result.applicable or not result.enabled:
            self._set_status(result.short_summary())
            return
        dialog = YamlValidationDialog(self, result.detailed_text())
        self.wait_window(dialog)

    def _yaml_completion_allowed(self) -> bool:
        if self.session is None or not self.session.local_yaml_validation_enabled:
            return True
        result = self._validate_output()
        if not result.applicable:
            return True
        if not result.dependency_available:
            return ask_centered_yes_no(
                self,
                "YAML validation unavailable",
                "PyYAML is not installed, so local YAML validation cannot run. Continue without local validation?",
            )
        if not result.syntax_valid:
            messagebox.showerror(
                "Invalid YAML",
                f"The output cannot be completed because the YAML is not parseable.\n\n{result.syntax_error or 'Unknown parse error.'}",
                parent=self,
            )
            self._set_status("Step completion blocked by invalid YAML syntax.")
            return False
        if not result.issues:
            return True
        if self.session.yaml_validation_behavior == "block":
            messagebox.showwarning(
                "YAML structure does not match",
                result.short_summary() + "\n\nReview the validation details and correct the structural findings before completing this step.",
                parent=self,
            )
            self._set_status("Step completion blocked by local YAML structural findings.")
            return False
        return ask_centered_yes_no(
            self,
            "YAML structural findings",
            result.short_summary() + "\n\nThe case is configured to warn rather than block. Complete the step anyway?",
        )

    def _set_status(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
        self.update_idletasks()

    def toggle_theme(self) -> None:
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self._apply_theme()
        self._set_status(f"{self.theme_mode.capitalize()} mode enabled.")

    def _apply_theme(self) -> None:
        palettes = {
            "light": {
                "bg": "#f3f3f3",
                "panel": "#ffffff",
                "field": "#ffffff",
                "fg": "#202124",
                "muted": "#5f6368",
                "select": "#d7e8ff",
                "select_fg": "#111111",
                "border": "#c8c8c8",
            },
            "dark": {
                "bg": "#202124",
                "panel": "#292a2d",
                "field": "#171717",
                "fg": "#f1f3f4",
                "muted": "#bdc1c6",
                "select": "#3f5f85",
                "select_fg": "#ffffff",
                "border": "#5f6368",
            },
        }
        palette = palettes[self.theme_mode]
        self.theme_palette = palette
        self.configure(background=palette["bg"])

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=palette["bg"], foreground=palette["fg"])
        style.configure("TFrame", background=palette["bg"])
        style.configure("TLabel", background=palette["bg"], foreground=palette["fg"])
        style.configure("TLabelframe", background=palette["bg"], foreground=palette["fg"], bordercolor=palette["border"])
        style.configure("TLabelframe.Label", background=palette["bg"], foreground=palette["fg"])
        style.configure("TButton", background=palette["panel"], foreground=palette["fg"], bordercolor=palette["border"], padding=(7, 4))
        style.map("TButton", background=[("active", palette["select"]), ("disabled", palette["bg"])], foreground=[("disabled", palette["muted"])])
        style.configure("TEntry", fieldbackground=palette["field"], foreground=palette["fg"], insertcolor=palette["fg"])
        style.configure("TCombobox", fieldbackground=palette["field"], background=palette["panel"], foreground=palette["fg"], arrowcolor=palette["fg"])
        style.map("TCombobox", fieldbackground=[("readonly", palette["field"])], foreground=[("readonly", palette["fg"])])
        style.configure("TRadiobutton", background=palette["bg"], foreground=palette["fg"])
        style.map("TRadiobutton", background=[("active", palette["bg"])])
        style.configure("Treeview", background=palette["field"], fieldbackground=palette["field"], foreground=palette["fg"], bordercolor=palette["border"])
        style.map("Treeview", background=[("selected", palette["select"])], foreground=[("selected", palette["select_fg"])])
        style.configure("Treeview.Heading", background=palette["panel"], foreground=palette["fg"])
        self.step_tree.tag_configure("completed", foreground="#7ee787" if self.theme_mode == "dark" else "#1a7f37")
        self.step_tree.tag_configure("completed_findings", foreground="#e3b341" if self.theme_mode == "dark" else "#9a6700")
        self.step_tree.tag_configure("current", foreground="#a5d6ff" if self.theme_mode == "dark" else "#0550ae")
        self.step_tree.tag_configure("skipped", foreground=palette["muted"])
        style.configure("TSeparator", background=palette["border"])
        style.configure("TPanedwindow", background=palette["bg"])

        self.apply_theme_to_window(self)
        self._configure_yaml_tags()
        self._apply_yaml_highlighting()
        if hasattr(self, "prompt_preview"):
            self._render_prompt_preview()
        if hasattr(self, "output_preview") and self.output_view_var.get() == "preview":
            self._render_output_preview()
        self.theme_button.configure(text="Switch to light mode" if self.theme_mode == "dark" else "Switch to dark mode")

    def apply_theme_to_window(self, window: tk.Misc) -> None:
        palette = self.theme_palette
        if not palette:
            return
        try:
            window.configure(background=palette["bg"])
        except (tk.TclError, AttributeError):
            pass

        def apply(widget: tk.Misc) -> None:
            if isinstance(widget, (tk.Text, ScrolledText)):
                widget.configure(
                    background=palette["field"],
                    foreground=palette["fg"],
                    insertbackground=palette["fg"],
                    selectbackground=palette["select"],
                    selectforeground=palette["select_fg"],
                    highlightbackground=palette["border"],
                    highlightcolor=palette["border"],
                )
            elif isinstance(widget, tk.Listbox):
                widget.configure(
                    background=palette["field"],
                    foreground=palette["fg"],
                    selectbackground=palette["select"],
                    selectforeground=palette["select_fg"],
                    highlightbackground=palette["border"],
                    highlightcolor=palette["border"],
                )
            elif isinstance(widget, tk.Toplevel):
                try:
                    widget.configure(background=palette["bg"])
                except tk.TclError:
                    pass
            for child in widget.winfo_children():
                apply(child)

        apply(window)

    def _set_no_case_state(self) -> None:
        self.step_tree.delete(*self.step_tree.get_children())
        for step in STEPS:
            mark = "🔒" if step.branch != "base" else "○"
            self.step_tree.insert("", "end", iid=str(step.step_id), values=(mark, f"#{step.step_id}", step.title))
        self.prompt_text.delete("1.0", "end")
        self.prompt_view_var.set("preview")
        self._sync_prompt_view()
        self.output_text.delete("1.0", "end")
        self.output_text.edit_modified(False)
        self.output_view_var.set("raw")
        self.output_preview_button.configure(state="disabled")
        self._sync_output_view()
        self.open_output_reader_button.configure(state="disabled")
        self._clear_yaml_highlighting()
        self.file_tree.delete(*self.file_tree.get_children())
        self.step_title.configure(text="No case loaded")
        self.step_status.configure(text="Create a new case or open an existing case.")
        self.upload_summary.configure(text="")
        self.reset_steps_button.configure(state="disabled")
        self.complete_button.configure(state="disabled")
        self.save_button.configure(state="disabled", text="Save changes")
        self.copy_prompt_button.configure(text="Copy prompt")
        self.yaml_validation_var.set("YAML validation: Not applicable for this step.")
        self.yaml_validation_details_button.configure(state="disabled")
        if self.yaml_validate_corrected_button.winfo_manager():
            self.yaml_validate_corrected_button.pack_forget()
        self.iteration_handoff_review_button.configure(state="disabled")
        self.mip_review_button.configure(state="disabled")
        self.ahp_review_button.configure(state="disabled")
        self.article_review_button.configure(state="disabled")
        self.materials_button.configure(state="disabled", text="Add materials")

    def _material_store(self) -> CaseMaterialStore:
        if self.session is None:
            raise CaseMaterialError("No case is loaded.")
        return CaseMaterialStore(self.session.case_dir, self.session.case_id)

    def _material_manifest_entries(self) -> list[dict[str, object]]:
        store = self._material_store()
        entries: list[dict[str, object]] = []
        for raw in store.entries():
            entry: dict[str, object] = dict(raw)
            entry["_present"] = store.path_for(raw).is_file()
            entries.append(entry)
        return entries

    def _material_change_requires_reset(self) -> bool:
        assert self.session is not None
        if self._has_unsaved_output():
            return True
        step_1_state = self.session.step_state(1)
        if is_completed_step_status(step_1_state.get("status")):
            return True
        if step_1_state.get("status") == "draft" or self.session.output_path(1).exists():
            return True
        current = self.session.current_step_id()
        if current is None or current != 1:
            return True
        for step_id in range(2, 32):
            state = self.session.step_state(step_id)
            if is_completed_step_status(state.get("status")) or state.get("status") in {"current", "draft"}:
                return True
            if self.session.prompt_path(step_id).exists() or self.session.output_path(step_id).exists():
                return True
        return False

    def manage_materials(self, parent: tk.Misc | None = None) -> int | None:
        host = parent or self
        if self.session is None:
            messagebox.showinfo("No case", "Create or open a case first.", parent=host)
            return None
        try:
            store = self._material_store()
            entries = store.entries()
        except CaseMaterialError as exc:
            messagebox.showerror("Could not open case materials", str(exc), parent=host)
            return None

        dialog = MaterialManagerDialog(host, entries, self.session.case_dir)
        host.wait_window(dialog)
        if isinstance(host, tk.Toplevel) and host.winfo_exists():
            try:
                host.grab_set()
            except tk.TclError:
                pass
        if dialog.result is None:
            self._set_status("Case-material edit cancelled.")
            return len(entries)
        if not dialog.result.get("changed"):
            self._set_status("Case materials unchanged.")
            return len(entries)

        requires_reset = self._material_change_requires_reset()
        if requires_reset:
            message = (
                "Case materials are read in step #1. Saving these changes will reset step #1 and every "
                "following step, archive saved prompts, outputs, validation reports, and route records, "
                "and restart the pipeline from step #1. Continue?"
            )
            if self._has_unsaved_output():
                message += " The currently displayed output also contains unsaved text that cannot be archived."
            if not ask_centered_yes_no(host, "Reset pipeline for changed materials", message):
                self._set_status("Case-material changes cancelled before pipeline reset.")
                return len(entries)

        try:
            updated = store.replace(list(dialog.result.get("items") or []))
            archive_dir = None
            if requires_reset:
                archive_dir = self.session.reset_from_step(1)
            else:
                self.session.invalidate_prompt(1)
            self.selected_step_id = 1
        except (CaseMaterialError, StorageError, OSError) as exc:
            messagebox.showerror("Could not save case materials", str(exc), parent=host)
            self._set_status("Case-material save failed.")
            return len(entries)

        self._refresh_all()
        archive_note = f" Pipeline work archived in {archive_dir.name}." if archive_dir is not None else ""
        self._set_status(
            f"Case materials saved: {len(updated)} file(s). Step #1 will read PMS.yaml first.{archive_note}"
        )
        return len(updated)

    def _manage_pending_new_case_materials(
        self,
        parent: tk.Misc,
    ) -> int | None:
        dialog = MaterialManagerDialog(
            parent,
            self._pending_new_case_materials,
            self.project_root,
        )
        parent.wait_window(dialog)

        if (
            isinstance(parent, tk.Toplevel)
            and parent.winfo_exists()
        ):
            try:
                parent.grab_set()
            except tk.TclError:
                pass

        if dialog.result is None:
            return len(self._pending_new_case_materials)

        self._pending_new_case_materials = [
            dict(item)
            for item in list(
                dialog.result.get("items") or []
            )
            if isinstance(item, dict)
        ]
        return len(self._pending_new_case_materials)


    def _iteration_handoff_review_available(self) -> bool:
        if self.session is None:
            return False
        try:
            return self.session.route_ready("article") and self.session.output_path(26).is_file()
        except StorageError:
            return False

    def review_iteration_handoff(self) -> None:
        if self.session is None:
            messagebox.showinfo("No case loaded", "Open or create a case first.", parent=self)
            return
        required = self.session.required_route_step("article")
        if not self.session.route_ready("article"):
            messagebox.showinfo(
                "Iteration Handoff not ready",
                f"Complete step #{required} before reviewing the Iteration Handoff actions.",
                parent=self,
            )
            return
        if not self.session.output_path(26).is_file():
            messagebox.showinfo(
                "Iteration Handoff not available",
                "Step #26 is marked complete, but the Iteration Handoff output file is missing.",
                parent=self,
            )
            return
        self._handle_iteration_handoff_next_action()

    def _load_approved_iteration_handoff(self) -> tuple[dict[str, object] | None, str]:
        if self.session is None:
            return None, "No case is loaded."
        path = self.session.output_path(26)
        if not path.is_file():
            return None, "Step #26 Iteration Handoff has not been completed."
        try:
            data = parse_handoff_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        except (IterationHandoffError, OSError) as exc:
            return None, f"Step #26 Iteration Handoff could not be parsed: {exc}"
        root = data.get("pms_discipline_iteration_handoff")
        if not isinstance(root, dict):
            return None, "Step #26 Iteration Handoff has no valid root."
        effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
        status = str(effective.get("status") or "")
        if status != "approved":
            return None, f"Step #26 Iteration Handoff is not approved for follow-up creation (status: {status or 'unknown'})."
        targets = effective.get("effective_targets") if isinstance(effective.get("effective_targets"), list) else []
        if not targets:
            return None, "Step #26 Iteration Handoff has no approved effective targets."
        return data, ""

    def _can_create_followup_case(self) -> bool:
        data, _reason = self._load_approved_iteration_handoff()
        return data is not None

    @staticmethod
    def _lines_from_yaml_list(value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        text = str(value or "").strip()
        if not text:
            return []
        return [line.strip(" -\t") for line in text.splitlines() if line.strip(" -\t")]

    def _followup_case_defaults_from_handoff(self, handoff: dict[str, object]) -> dict[str, object]:
        assert self.session is not None
        root = handoff["pms_discipline_iteration_handoff"]
        assert isinstance(root, dict)
        effective = root.get("effective_followup_preparation") if isinstance(root.get("effective_followup_preparation"), dict) else {}
        seed = effective.get("followup_case_seed") if isinstance(effective.get("followup_case_seed"), dict) else {}
        targets = effective.get("effective_targets") if isinstance(effective.get("effective_targets"), list) else []
        urgency = root.get("iteration_urgency") if isinstance(root.get("iteration_urgency"), dict) else {}
        depth = root.get("current_depth_assessment") if isinstance(root.get("current_depth_assessment"), dict) else {}
        model = root.get("model_preselection") if isinstance(root.get("model_preselection"), dict) else {}

        title = str(seed.get("working_title") or "").strip()
        if not title or title.lower() in {"optional or pending", "pending", "unknown"}:
            title = f"Follow-up — {self.session.case_data.get('title', 'Untitled case')}"

        question_lines: list[str] = []
        material_lines: list[str] = []
        for index, target in enumerate(targets, start=1):
            if not isinstance(target, dict):
                continue
            question = str(target.get("question") or "").strip()
            if question:
                question_lines.append(f"{index}. {question}")
            basis = str(target.get("basis_in_checked_record") or "").strip()
            value = str(target.get("expected_discriminative_value") or "").strip()
            if basis:
                question_lines.append(f"   Prior-record basis: {basis}")
            if value:
                question_lines.append(f"   Expected discriminative value: {value}")
            for material in self._lines_from_yaml_list(target.get("required_new_material")):
                material_lines.append(f"- {material}")

        primary = str(seed.get("primary_question") or "").strip()
        if not primary or primary.lower() in {"optional or pending", "pending", "unknown"}:
            primary = str((targets[0] if targets and isinstance(targets[0], dict) else {}).get("question") or "").strip()

        boundary = str(seed.get("proposed_case_boundary") or "").strip()
        if not boundary or boundary.lower() in {"optional or pending", "pending", "unknown"}:
            boundary = "A separately bounded follow-up case defined by the approved Iteration Handoff targets below. The analyst must confirm or narrow this boundary before using the case for stronger claims."

        description = (
            "FOLLOW-UP CASE CREATED FROM APPROVED ITERATION HANDOFF\n\n"
            f"Parent case: {self.session.case_id}\n"
            f"Parent title: {self.session.case_data.get('title', '')}\n\n"
            "Boundary proposal:\n"
            f"{boundary}\n\n"
            "Primary follow-up question:\n"
            f"{primary or 'requires human confirmation'}\n\n"
            "Approved effective follow-up targets:\n"
            + ("\n".join(question_lines) if question_lines else "requires human confirmation")
            + "\n\nRequired new or comparison material named by the handoff:\n"
            + ("\n".join(dict.fromkeys(material_lines)) if material_lines else "- requires human confirmation")
            + "\n\nSource-role warning:\n"
            "The prior checked Stage 1–3 artifacts and the Iteration Handoff provide bounded analytical context only. "
            "They are not evidence for this follow-up case and must not be used to confirm their own prior findings. "
            "Inherited original materials retain their original source status. Newly supplied materials require explicit source-status confirmation."
        )
        source_status = (
            "Follow-up case seeded from an approved PMS-DISCIPLINE Iteration Handoff. "
            "Prior checked analysis artifacts are analytical context only, not evidence. "
            "User notes in the handoff are planning/context notes unless explicitly reclassified as new user-supplied case material. "
            "Inherited original materials retain their original source status; newly supplied materials require confirmation."
        )
        intended_use = (
            "Run a separately bounded PMS-DISCIPLINE follow-up analysis to test, weaken, differentiate, or redirect the approved follow-up questions. "
            "No finding, route, operator status, add-on selection, MIP/AHP status, or claim ceiling is inherited from the parent case."
        )
        return {
            "title": title,
            "description": description,
            "source_status": source_status,
            "intended_use": intended_use,
            "ai_review_steps_enabled": self.session.ai_review_steps_enabled,
            "local_yaml_validation_enabled": self.session.local_yaml_validation_enabled,
            "yaml_validation_behavior": self.session.yaml_validation_behavior,
            "parent_case_id": self.session.case_id,
            "parent_case_title": self.session.case_data.get("title", ""),
            "parent_case_dir": str(self.session.case_dir),
            "created_from_iteration_handoff": True,
            "followup_lineage": {
                "schema_version": "PMS_ORCHESTRATOR_FOLLOWUP_LINEAGE_1.0",
                "parent_case_id": self.session.case_id,
                "parent_case_title": self.session.case_data.get("title", ""),
                "parent_case_dir": str(self.session.case_dir),
                "iteration_handoff_output": str(self.session.output_path(26).relative_to(self.session.case_dir)),
                "current_depth_status": str(depth.get("status") or "unknown"),
                "sufficient_for_original_intended_use": str(depth.get("sufficient_for_original_intended_use") or "unknown"),
                "model_recommendation": str(model.get("recommendation") or "unknown"),
                "iteration_urgency_level": str(urgency.get("level") or "unknown"),
                "effective_targets": targets,
                "required_new_material": self._lines_from_yaml_list(effective.get("required_new_material")),
                "boundary_rules": {
                    "prior_analysis_is_not_evidence": True,
                    "no_route_inheritance": True,
                    "no_claim_ceiling_inheritance": True,
                    "user_notes_are_not_verified_facts": True,
                },
            },
        }

    def _followup_materials_from_current_case(self) -> list[dict[str, object]]:
        assert self.session is not None
        entries: list[dict[str, object]] = []
        def add(path: Path, description: str, purpose: str) -> None:
            if path.is_file():
                entries.append({
                    "source_path": str(path),
                    "description": description,
                    "purpose": purpose,
                })
        add(
            self.session.output_path(26),
            "Approved Iteration Handoff YAML from the parent case.",
            "Planning record for the follow-up case; not evidence and not a current-case finding.",
        )
        for step_id, label in ((20, "Stage 1 artifact index"), (21, "Stage 1 check"), (22, "Stage 2 layer digests"), (23, "Stage 2 check"), (24, "Stage 3 full record"), (25, "Stage 3 check")):
            add(
                self.session.output_path(step_id),
                f"Parent-case {label} output.",
                "Prior analytical context only; not evidence for the follow-up case and not inherited claim authority.",
            )
        try:
            material_store = self._material_store()
            for material in material_store.entries():
                path = material_store.path_for(material)
                add(
                    path,
                    f"Inherited original case material from parent case: {material.get('description') or material.get('original_filename') or path.name}",
                    "Inherited source material. Preserve its original source status and re-confirm relevance to the follow-up case.",
                )
        except CaseMaterialError:
            pass
        return entries

    def create_followup_case_from_handoff(self) -> None:
        if self.session is None:
            messagebox.showinfo("No case loaded", "Open or create a case first.", parent=self)
            return
        handoff, reason = self._load_approved_iteration_handoff()
        if handoff is None:
            messagebox.showinfo("Follow-up case unavailable", reason, parent=self)
            self._set_status(f"Follow-up case skipped: {reason}")
            return
        defaults = self._followup_case_defaults_from_handoff(handoff)
        self._pending_new_case_materials = self._followup_materials_from_current_case()
        dialog = CaseDialog(
            self,
            "Create follow-up PMS-DISCIPLINE case",
            initial=defaults,
            materials_count=len(self._pending_new_case_materials),
            materials_command=self._manage_pending_new_case_materials,
        )
        self.wait_window(dialog)
        if dialog.result is None:
            self._pending_new_case_materials = []
            self._set_status("Follow-up case creation cancelled.")
            return
        pending_materials = [dict(item) for item in self._pending_new_case_materials]
        self._pending_new_case_materials = []
        values = dict(dialog.result)
        for key in ("parent_case_id", "parent_case_title", "parent_case_dir", "created_from_iteration_handoff", "followup_lineage"):
            if key in defaults:
                values[key] = defaults[key]
        try:
            self.session = self.store.create_case(values)
        except StorageError as exc:
            messagebox.showerror("Could not create follow-up case", str(exc), parent=self)
            return
        material_count = 0
        if pending_materials:
            try:
                store = CaseMaterialStore(self.session.case_dir, self.session.case_id)
                material_count = len(store.replace(pending_materials))
            except (CaseMaterialError, OSError) as exc:
                messagebox.showerror(
                    "Follow-up case created, but materials were not saved",
                    f"The follow-up case was created successfully, but its materials could not be copied.\n\n{exc}\n\nUse Add materials to add them again.",
                    parent=self,
                )
        self.selected_step_id = 1
        self._refresh_all()
        self._set_status(f"Follow-up case created with {material_count} inherited/context material file(s).")
        messagebox.showinfo(
            "Follow-up case created",
            "The follow-up case was created. Confirm the case boundary, source status, intended use, and material roles before completing step #1.",
            parent=self,
        )

    def new_case(self) -> None:
        self._pending_new_case_materials = []

        dialog = CaseDialog(
            self,
            "New PMS-DISCIPLINE case",
            materials_count=0,
            materials_command=(
                self._manage_pending_new_case_materials
            ),
        )
        self.wait_window(dialog)

        if dialog.result is None:
            self._pending_new_case_materials = []
            self._set_status("New case cancelled.")
            return

        pending_materials = [
            dict(item)
            for item in self._pending_new_case_materials
        ]
        self._pending_new_case_materials = []

        try:
            self.session = self.store.create_case(
                dialog.result
            )
        except StorageError as exc:
            messagebox.showerror(
                "Could not create case",
                str(exc),
                parent=self,
            )
            return

        material_count = 0

        if pending_materials:
            try:
                store = CaseMaterialStore(
                    self.session.case_dir,
                    self.session.case_id,
                )
                material_count = len(
                    store.replace(pending_materials)
                )
            except (CaseMaterialError, OSError) as exc:
                messagebox.showerror(
                    "Case created, but materials were not saved",
                    (
                        "The case was created successfully, "
                        "but its materials could not be "
                        f"copied.\n\n{exc}\n\n"
                        "Use Add materials to add them again."
                    ),
                    parent=self,
                )

        self.selected_step_id = 1
        self._refresh_all()

        if material_count:
            self._set_status(
                f"Case created: {self.session.case_id} · "
                f"{material_count} material file(s) added."
            )
        else:
            self._set_status(
                f"Case created: {self.session.case_id}"
            )

    def open_case(self) -> None:
        path = filedialog.askdirectory(title="Select case folder", initialdir=self.store.cases_dir)
        if not path:
            return
        try:
            self.session = self.store.load_case(Path(path))
            current = self.session.current_step_id()
            if current is not None:
                self.selected_step_id = current
            else:
                completed = [
                    step.step_id
                    for step in STEPS
                    if is_completed_step_status(self.session.step_state(step.step_id).get("status"))
                ]
                self.selected_step_id = max(completed, default=1)
            self._refresh_all()
            self._set_status(f"Case loaded: {self.session.case_id}")
        except StorageError as exc:
            messagebox.showerror("Could not load case", str(exc), parent=self)

    def edit_case(self) -> None:
        if self.session is None:
            messagebox.showinfo("No case", "Create or open a case first.", parent=self)
            return
        initial = {
            "title": str(self.session.case_data.get("title", "")),
            "description": str(self.session.case_data.get("description", "")),
            "source_status": str(self.session.case_data.get("source_status", "")),
            "intended_use": str(self.session.case_data.get("intended_use", "")),
            "ai_review_steps_enabled": self.session.ai_review_steps_enabled,
            "local_yaml_validation_enabled": self.session.local_yaml_validation_enabled,
            "yaml_validation_behavior": self.session.yaml_validation_behavior,
        }
        try:
            materials_count = len(self._material_store().entries())
        except CaseMaterialError:
            materials_count = 0
        dialog = CaseDialog(
            self,
            "Edit case",
            initial,
            materials_count=materials_count,
            materials_command=self.manage_materials,
        )
        self.wait_window(dialog)
        if dialog.result is None:
            return
        old_review_mode = self.session.ai_review_steps_enabled
        new_review_mode = bool(dialog.result.get("ai_review_steps_enabled", old_review_mode))
        if old_review_mode and not new_review_mode:
            message = (
                "Disable unfinished semantic AI review steps for this case? Completed reviews remain preserved. "
                "Current and future unfinished review prompts/outputs are archived before being skipped."
            )
            if self.session.current_step_id() in AI_REVIEW_STEP_IDS and self._has_unsaved_output():
                message += " The currently displayed review output also contains unsaved text that will not be archived."
            if not ask_centered_yes_no(self, "Disable AI review steps", message):
                self._set_status("Case edit cancelled before changing AI review mode.")
                return
        self.session.update_case(dialog.result)
        current = self.session.current_step_id()
        if current is not None:
            self.selected_step_id = current
        self._refresh_all()
        self._set_status("Case settings saved; pending prompts will be rendered again.")

    def _refresh_all(self) -> None:
        if self.session is None:
            self._set_no_case_state()
            return
        self._refresh_case_summary()
        self._refresh_step_list()
        self._show_step(self.selected_step_id)
        self.iteration_handoff_review_button.configure(state="normal" if self._iteration_handoff_review_available() else "disabled")
        self.mip_review_button.configure(state="normal" if self.session.route_ready("mip") else "disabled")
        self.ahp_review_button.configure(state="normal" if self.session.route_ready("ahp") else "disabled")
        self.article_review_button.configure(state="normal" if self.session.route_ready("article") else "disabled")
        try:
            material_count = len(self._material_store().entries())
            self.materials_button.configure(
                state="normal",
                text=f"Add materials ({material_count})" if material_count else "Add materials",
            )
        except CaseMaterialError:
            self.materials_button.configure(state="normal", text="Add materials (!)")

    def _refresh_case_summary(self) -> None:
        assert self.session is not None
        route = self.session.session_data.get("route") or {}
        mip_route = self.session.session_data.get("mip_route") or {}
        ahp_route = self.session.session_data.get("ahp_route") or {}
        article_route = self.session.session_data.get("article_route") or {}
        addon = route.get("selected_addon") or "none"
        mip = "use" if mip_route.get("route_type") == "use_mip" else ("none" if mip_route.get("route_type") == "no_mip" else "not set")
        ahp = "use" if ahp_route.get("route_type") == "use_ahp" else ("none" if ahp_route.get("route_type") == "no_ahp" else "not set")
        article = (self.session.article_profile.replace("_", " ") if article_route.get("route_type") == "generate_article" else ("no" if article_route.get("route_type") == "no_article" else "not set"))
        case_title = self._shorten(self.session.case_data.get("title"), 24)
        source_status = self._shorten(self.session.case_data.get("source_status"), 18)
        addon = self._shorten(addon, 14)
        run_status = self._shorten(self.session.session_data.get("run_status"), 22)
        checks = "on" if self.session.ai_review_steps_enabled else "off"
        yaml_mode = (
            self.session.yaml_validation_behavior
            if self.session.local_yaml_validation_enabled
            else "off"
        )
        self.case_summary.configure(
            text=(
                f"Case: {case_title}  |  Source: {source_status}  |  Add-on: {addon}  |  "
                f"MIP: {mip}  |  AHP: {ahp}  |  Article: {article}  |  "
                f"Checks: {checks}  |  YAML: {yaml_mode}  |  Run: {run_status}"
            )
        )

    def _refresh_step_list(self) -> None:
        assert self.session is not None
        self.step_tree.delete(*self.step_tree.get_children())
        for step in STEPS:
            status = self.session.step_state(step.step_id).get("status", "open")
            mark = STATUS_MARKS.get(status, "?")
            tag = "completed" if is_completed_step_status(status) else status
            if is_completed_step_status(status) and self.session.step_has_yaml_findings(step.step_id):
                tag = "completed_findings"
            self.step_tree.insert(
                "",
                "end",
                iid=str(step.step_id),
                values=(mark, f"#{step.step_id}", step.title),
                tags=(tag,),
            )
        selected_iid = str(self.selected_step_id)
        if self.step_tree.exists(selected_iid):
            self.step_tree.selection_set(selected_iid)
            self.step_tree.focus(selected_iid)
            self.step_tree.see(selected_iid)

    def _on_step_select(self, _event: object) -> None:
        selection = self.step_tree.selection()
        if not selection:
            return
        try:
            self.selected_step_id = int(selection[0])
        except ValueError:
            return
        self._show_step(self.selected_step_id)

    def _selected_run_resources_block(self) -> str:
        assert self.session is not None

        route = self.session.session_data.get("route") or {}
        mip_route = self.session.session_data.get("mip_route") or {}
        ahp_route = self.session.session_data.get("ahp_route") or {}
        selected_addon = str(route.get("selected_addon") or "none")

        def presence(relative: str) -> str:
            return "present" if (self.project_root / relative).is_file() else "missing"

        lines = [
            "SELECTED RUN RESOURCES",
            "This is run provenance, not a complete installation inventory.",
            "Only resources selected, read, applied, or required by the current run are listed.",
            "Unselected local files are represented by route state and must not be expanded from disk availability.",
            "",
            "pms_base:",
            "  path: pms/PMS.yaml",
            f"  local_presence: {presence('pms/PMS.yaml')}",
            "  selected: yes",
            f"  read_status: {'completed' if is_completed_step_status(self.session.step_state(1).get('status')) else self.session.step_state(1).get('status', 'unknown')}",
            "",
            "used_templates:",
        ]

        template_steps: list[tuple[int, str]] = [
            (2, "templates/pms_discipline_pre_analysis_template.yaml"),
            (4, "templates/pms_core_case_application_template.yaml"),
            (6, "templates/pms_discipline_addon_recommendation_gate_template.yaml"),
            (11, "templates/pms_discipline_mip_gate_template.yaml"),
            (16, "templates/pms_discipline_ahp_gate_template.yaml"),
            (20, "templates/pms_case_record_stage_1_artifact_index_template.yaml"),
        ]
        if route.get("route_type") == "selected_addon" and selected_addon != "none":
            template_steps.insert(
                3,
                (9, f"templates/pms_addon_{selected_addon.lower()}_case_application_template.yaml"),
            )

        used_template_count = 0
        for step_id, relative in template_steps:
            status = str(self.session.step_state(step_id).get("status") or "unknown")
            if step_id == 20 or status in {"current", "draft"} or is_completed_step_status(status):
                lines.append(
                    f"  - path: {relative}; local_presence={presence(relative)}; "
                    f"selected=yes; used_at_step={step_id:02d}; step_status={status}"
                )
                used_template_count += 1
        if not used_template_count:
            lines.append("  - none")

        addon_route = str(route.get("route_type") or "not_set")
        lines.extend([
            "",
            "selected_addon:",
            f"  route: {addon_route}",
            f"  family: {selected_addon}",
        ])
        if addon_route == "selected_addon" and selected_addon != "none":
            addon_source = f"pms/PMS-{selected_addon}.yaml"
            addon_template = f"templates/pms_addon_{selected_addon.lower()}_case_application_template.yaml"
            lines.extend([
                f"  source_path: {addon_source}",
                f"  source_local_presence: {presence(addon_source)}",
                f"  source_read_status: {self.session.step_state(8).get('status', 'unknown')}",
                f"  application_template_path: {addon_template}",
                f"  application_template_local_presence: {presence(addon_template)}",
            ])
        else:
            lines.extend([
                "  source_path: not_applicable",
                "  source_local_presence: not_checked_for_run",
                "  source_read_status: not_applicable",
                "  application_template_path: not_applicable",
                "  application_template_local_presence: not_checked_for_run",
            ])

        mip_type = str(mip_route.get("route_type") or "not_set")
        mip_source = "mip/MIP - Maturity in Practice.yaml"
        lines.extend([
            "",
            "mip:",
            f"  route: {mip_type}",
        ])
        if mip_type == "use_mip":
            lines.extend([
                f"  source_path: {mip_source}",
                f"  source_local_presence: {presence(mip_source)}",
                f"  source_read_status: {self.session.step_state(13).get('status', 'unknown')}",
            ])
        else:
            lines.extend([
                "  source_path: not_selected",
                "  source_local_presence: not_checked_for_run",
                "  source_read_status: not_applicable",
            ])

        ahp_type = str(ahp_route.get("route_type") or "not_set")
        ahp_source = "mip/MIP - Maturity in Practice - AHP Module.yaml"
        lines.extend([
            "",
            "ahp:",
            f"  route: {ahp_type}",
        ])
        if ahp_type == "use_ahp":
            lines.extend([
                f"  source_path: {ahp_source}",
                f"  source_local_presence: {presence(ahp_source)}",
                f"  source_read_or_application_status: {self.session.step_state(18).get('status', 'unknown')}",
            ])
        else:
            lines.extend([
                "  source_path: not_selected",
                "  source_local_presence: not_checked_for_run",
                "  source_read_or_application_status: not_applicable",
            ])

        lines.extend([
            "",
            "future_templates:",
            "  - path: templates/pms_case_record_stage_2_layer_digest_extraction_template.yaml",
            "    status: deferred_future_step",
            "    blocks_stage_1_readiness: false",
            "  - path: templates/pms_case_record_stage_3_full_case_record_integration_template.yaml",
            "    status: deferred_future_step",
            "    blocks_stage_1_readiness: false",
        ])
        return "\n".join(lines)

    def _stage_1_runner_manifest(self, through_step: int = 19) -> str:
        assert self.session is not None

        route = self.session.session_data.get("route") or {}
        mip_route = self.session.session_data.get("mip_route") or {}
        ahp_route = self.session.session_data.get("ahp_route") or {}
        current_output = self.session.output_path(20).relative_to(self.session.case_dir).as_posix()

        lines = [
            "RUNNER-GENERATED STAGE 1 MANIFEST",
            "This block is authoritative for selected run resources, route status, exact paths, and upstream run artifacts.",
            "Metadata authority order: runner manifest > checked upstream artifact > generated downstream artifact > template default > model inference.",
            "When values conflict, copy the runner-manifest value exactly. Do not normalize paths or substitute session.json.",
            "Do not replace it with AI-service attachment names, temporary paths, inferred hashes, or chat-sandbox state.",
            "",
            f"case_id: {self.session.case_id}",
            f"run_id: {self.session.case_id}",
            f"case_record_source: {self.session.case_json_path.relative_to(self.session.case_dir).as_posix()}",
            f"session_record_source: {self.session.session_json_path.relative_to(self.session.case_dir).as_posix()}",
            f"semantic_ai_review_steps: {'enabled' if self.session.ai_review_steps_enabled else 'disabled'}",
            f"review_status: {'checked_pipeline' if self.session.ai_review_steps_enabled else 'unchecked_by_user_choice'}",
            "",
            "ROUTES",
            f"add_on_route: {route.get('route_type') or 'not_set'}",
            f"selected_add_on: {route.get('selected_addon') or 'none'}",
            f"add_on_selection_basis: {route.get('selection_basis') or 'unknown'}",
            f"mip_route: {mip_route.get('route_type') or 'not_set'}",
            f"mip_selection_basis: {mip_route.get('selection_basis') or 'unknown'}",
            f"ahp_route: {ahp_route.get('route_type') or 'not_set'}",
            f"ahp_selection_basis: {ahp_route.get('selection_basis') or 'unknown'}",
            "",
            f"UPSTREAM PRODUCED OR SKIPPED STEP ARTIFACTS (STEPS 1-{through_step})",
        ]

        for step in STEPS:
            if step.step_id > through_step:
                break
            state = self.session.step_state(step.step_id)
            output_path = self.session.output_path(step.step_id)
            if output_path.exists():
                output_ref = output_path.relative_to(self.session.case_dir).as_posix()
                output_exists = "yes"
            else:
                output_ref = "none"
                output_exists = "no"
            lines.append(
                f"step_{step.step_id:02d}: status={state.get('status', 'unknown')}; "
                f"output={output_ref}; output_exists={output_exists}"
            )

        lines.extend([
            "",
            "CURRENT STEP EXECUTION METADATA",
            "This block describes the output currently being produced. It is not an upstream artifact and must not be copied into the Stage 1 YAML.",
            "step: 20",
            f"expected_output: {current_output}",
            f"status: {self.session.step_state(20).get('status', 'unknown')}",
            f"output_exists_before_generation: {'yes' if self.session.output_path(20).is_file() else 'no'}",
            "",
            self._selected_run_resources_block(),
            "",
            render_case_material_manifest_block(
                self._material_manifest_entries(),
                step_1_status=str(self.session.step_state(1).get("status") or "unknown"),
            ),
            "",
            "NORMALIZATION RULES",
            "- Use only the selected project-relative source/template paths, case-relative material paths, and upstream case-relative output paths listed above.",
            "- Ignore /mnt/data paths, AI-service sandbox paths, renamed uploads, duplicate attachment names, and helper scripts.",
            "- Do not invent SHA-256 values. Set sha256_if_available to unknown unless a hash is explicitly supplied by this manifest.",
            "- Do not infer local presence for unselected add-on, MIP, or AHP files from installation state.",
            "- Unselected add-on sources and templates are not_applicable or not_selected for this run; unselected outputs receive no output path.",
            "- A skipped MIP or AHP branch is not a missing-artifact defect.",
            "- Stage 1 readiness depends on actual upstream artifacts and route states, not on current-output existence or future-template upload state.",
            "- The Stage 1 output must not index its own current production path as an upstream artifact.",
        ])
        return "\n".join(lines)

    def _stage_1_check_runner_manifest(self) -> str:
        assert self.session is not None
        route = self.session.session_data.get("route") or {}
        mip_route = self.session.session_data.get("mip_route") or {}
        ahp_route = self.session.session_data.get("ahp_route") or {}
        step_20_path = self.session.output_path(20)
        lines = [
            "RUNNER-GENERATED STAGE 1 CHECK MANIFEST",
            "Authority hierarchy: runner manifest > checked upstream artifact > Stage 1 output > template default > model inference.",
            "Copy exact runner paths and states. deferred_future_step is not missing. Never substitute session.json, sandbox paths, attachment names, helper scripts, or invented hashes.",
            "",
            f"case_id: {self.session.case_id}",
            f"run_id: {self.session.case_id}",
            "routes:",
            f"  add_on_route: {route.get('route_type') or 'not_set'}",
            f"  selected_add_on: {route.get('selected_addon') or 'none'}",
            f"  mip_route: {mip_route.get('route_type') or 'not_set'}",
            f"  ahp_route: {ahp_route.get('route_type') or 'not_set'}",
            "upstream_produced_or_skipped_artifacts:",
        ]
        for step in STEPS:
            if step.step_id > 19:
                break
            state = self.session.step_state(step.step_id).get("status", "unknown")
            path = self.session.output_path(step.step_id)
            output_ref = path.relative_to(self.session.case_dir).as_posix() if path.is_file() else "none"
            lines.append(
                f"  step_{step.step_id:02d}: status={state}; output={output_ref}; "
                f"output_exists={'yes' if path.is_file() else 'no'}"
            )

        lines.extend([
            "current_stage_1_output_under_review:",
            "  step: 20",
            f"  path: {step_20_path.relative_to(self.session.case_dir).as_posix()}",
            f"  status: {self.session.step_state(20).get('status', 'unknown')}",
            f"  output_exists: {'yes' if step_20_path.is_file() else 'no'}",
            "  self_index_required: false",
            "  rule: The Stage 1 output is the artifact under review, not an upstream artifact that must appear in its own inventory.",
            self._selected_run_resources_block(),
            render_case_material_manifest_block(
                self._material_manifest_entries(),
                step_1_status=str(self.session.step_state(1).get("status") or "unknown"),
            ),
        ])
        return "\n".join(lines)

    def _case_record_runner_manifest(self, current_step_id: int) -> str:
        assert self.session is not None

        route = self.session.session_data.get("route") or {}
        mip_route = self.session.session_data.get("mip_route") or {}
        ahp_route = self.session.session_data.get("ahp_route") or {}
        current_path = self.session.output_path(current_step_id)

        lines = [
            "RUNNER-GENERATED CASE-RECORD MANIFEST",
            "This block is authoritative for exact run metadata, route state, step state, file existence, and upstream output paths.",
            "Metadata authority order: runner manifest > checked upstream artifact > generated downstream artifact > template default > model inference.",
            "When values conflict, copy this manifest exactly. Do not normalize paths and do not substitute session.json unless this manifest explicitly names session.json.",
            "Template defaults are placeholders, not evidence. Model inference is never allowed to override recorded metadata.",
            "",
            f"case_id: {self.session.case_id}",
            f"run_id: {self.session.case_id}",
            f"current_step: {current_step_id}",
            f"semantic_ai_review_steps: {'enabled' if self.session.ai_review_steps_enabled else 'disabled'}",
            f"review_status: {'checked_pipeline' if self.session.ai_review_steps_enabled else 'unchecked_by_user_choice'}",
            "",
            "ROUTES",
            f"add_on_route: {route.get('route_type') or 'not_set'}",
            f"selected_add_on: {route.get('selected_addon') or 'none'}",
            f"add_on_selection_basis: {route.get('selection_basis') or 'unknown'}",
            f"mip_route: {mip_route.get('route_type') or 'not_set'}",
            f"mip_selection_basis: {mip_route.get('selection_basis') or 'unknown'}",
            f"ahp_route: {ahp_route.get('route_type') or 'not_set'}",
            f"ahp_selection_basis: {ahp_route.get('selection_basis') or 'unknown'}",
            "",
            "UPSTREAM CASE-RECORD OUTPUTS",
        ]

        upstream_case_record_steps = range(20, min(current_step_id, 26))
        if not list(upstream_case_record_steps):
            lines.append("none")
        else:
            for step_id in range(20, min(current_step_id, 26)):
                state = self.session.step_state(step_id).get("status", "unknown")
                path = self.session.output_path(step_id)
                path_ref = path.relative_to(self.session.case_dir).as_posix() if path.is_file() else "none"
                lines.append(
                    f"step_{step_id:02d}: status={state}; output={path_ref}; "
                    f"output_exists={'yes' if path.is_file() else 'no'}"
                )

        lines.extend([
            "",
            "CURRENT STEP EXECUTION METADATA",
            "This block is runner execution metadata only. Do not copy it into the generated or reviewed case-record YAML.",
            f"step: {current_step_id}",
            f"expected_output: {current_path.relative_to(self.session.case_dir).as_posix()}",
            f"status: {self.session.step_state(current_step_id).get('status', 'unknown')}",
            f"output_exists_before_or_during_current_step: {'yes' if current_path.is_file() else 'no'}",
            "current_output_is_upstream_input: false",
            "",
            "FUTURE CASE-RECORD STEPS",
        ])
        future_ids = list(range(current_step_id + 1, 26))
        if not future_ids:
            lines.append("none")
        for step_id in future_ids:
            path = self.session.output_path(step_id)
            lines.append(
                f"step_{step_id:02d}: status=future_step; expected_output={path.relative_to(self.session.case_dir).as_posix()}; "
                "output_exists_not_relevant_to_current_step=true"
            )

        lines.extend([
            "",
            "UPSTREAM STEP ARTIFACTS",
        ])
        for step in STEPS:
            if step.step_id >= current_step_id:
                break
            state = self.session.step_state(step.step_id).get("status", "unknown")
            path = self.session.output_path(step.step_id)
            output_ref = path.relative_to(self.session.case_dir).as_posix() if path.is_file() else "none"
            lines.append(
                f"step_{step.step_id:02d}: status={state}; output={output_ref}; "
                f"output_exists={'yes' if path.is_file() else 'no'}"
            )

        stage_1_label = "Checked Stage 1" if self.session.ai_review_steps_enabled else "Unchecked Stage 1 output"
        layer_label = "Checked layer artifacts" if self.session.ai_review_steps_enabled else "Available direct layer outputs"
        stage_2_label = "Checked Stage 2" if self.session.ai_review_steps_enabled else "Unchecked Stage 2 output"
        upstream_label = "checked upstream values" if self.session.ai_review_steps_enabled else "available upstream values"
        lines.extend([
            "",
            "CONFLICT AND CURRENT-STEP RULES",
            "- Exact upstream path, file-existence, route, branch, and step-status conflicts are resolved by this runner manifest.",
            f"- {stage_1_label} controls artifact selection and provenance imported into Stage 2 and Stage 3.",
            f"- {layer_label} control substantive case content for their own layer.",
            f"- {stage_2_label} controls digest substance imported into Stage 3.",
            f"- Template defaults never override {upstream_label}.",
            "- Preserve genuine substantive contradictions.",
            "- Do not import current-step execution state, temporary output-existence metadata, or future-step output state into notes, missing-item registers, deliberately-not-imported items, tensions, blockers, readiness fields, or case findings.",
            "- The current output does not need to exist before generation and must not be classified as missing, deferred, excluded, unresolved, or deliberately not imported.",
            "- Workflow metadata drift is not case substance and must not be turned into a case finding.",
            "- When semantic AI reviews are disabled, never relabel an unchecked direct output as checked, corrected, validated, or certified.",
        ])
        return "\n".join(lines)

    def _iteration_handoff_runner_manifest(self) -> str:
        assert self.session is not None
        current_path = self.session.output_path(26)

        def step_ref(step_id: int) -> str:
            state = self.session.step_state(step_id).get("status", "unknown")
            path = self.session.output_path(step_id)
            output_ref = path.relative_to(self.session.case_dir).as_posix() if path.is_file() else "none"
            return f"step_{step_id:02d}: status={state}; output={output_ref}; output_exists={'yes' if path.is_file() else 'no'}"

        stage_1 = 21 if self.session.ai_review_steps_enabled else 20
        stage_2 = 23 if self.session.ai_review_steps_enabled else 22
        stage_3 = 25 if self.session.ai_review_steps_enabled else 24
        lines = [
            "RUNNER-GENERATED ITERATION HANDOFF MANIFEST",
            "This block is authoritative for the Iteration Handoff source basis, exact paths, and current-step boundary.",
            "The Iteration Handoff is not Case Record Stage 4. It is a prospective handoff for possible follow-up work after Stages 1–3.",
            "Derive only from checked Case Record Stages 1–3 when semantic reviews are enabled, or from the corresponding unchecked direct outputs when reviews are disabled.",
            "Do not derive from article drafts, final article prose, example outputs, old prompts, validation history, route revision history, or current-step output state.",
            "Prior checked analysis artifacts provide bounded analytical context for a future case; they are not evidence for the future case and must not confirm their own findings.",
            "",
            f"case_id: {self.session.case_id}",
            f"semantic_ai_review_steps: {'enabled' if self.session.ai_review_steps_enabled else 'disabled'}",
            f"review_status: {'checked_pipeline' if self.session.ai_review_steps_enabled else 'unchecked_by_user_choice'}",
            "",
            "CONTROLLING CASE-RECORD SOURCES",
            f"stage_1_source_step: {stage_1}",
            f"stage_2_source_step: {stage_2}",
            f"stage_3_source_step: {stage_3}",
            step_ref(stage_1),
            step_ref(stage_2),
            step_ref(stage_3),
            "",
            "CURRENT STEP EXECUTION METADATA",
            "This block describes the output currently being produced. It is not an upstream artifact and must not be copied as a case finding.",
            "step: 26",
            f"expected_output: {current_path.relative_to(self.session.case_dir).as_posix()}",
            f"status: {self.session.step_state(26).get('status', 'unknown')}",
            f"output_exists_before_generation: {'yes' if current_path.is_file() else 'no'}",
            "current_output_is_upstream_input: false",
            "",
            "SOURCE ROLE RULES",
            "- Checked Stage 3 controls current integrated result, claim ceiling, limits, unresolved items, rivals, and final posture.",
            "- Checked Stage 2 supplies layer-specific depth and selective shallowness.",
            "- Checked Stage 1 supplies provenance, actual artifacts, branch state, and eligible carry-forward references.",
            "- Runner metadata controls exact paths and file availability.",
            "- Article outputs are presentation artifacts and are not sources for the Iteration Handoff.",
            "- User notes and future follow-up questions are not verified facts, evidence, operator findings, or route authorization.",
        ]
        return "\n".join(lines)

    @staticmethod
    def _fast_mode_prompt_text(text: str) -> str:
        text = re.sub(r"\bChecked\b", "Unchecked", text)
        text = re.sub(r"\bchecked\b", "unchecked", text)
        return text

    def _ai_review_mode_override(self, step: StepDefinition) -> str:
        assert self.session is not None
        if self.session.ai_review_steps_enabled:
            return ""
        relevant = [
            (review, REVIEW_SOURCE_STEP[review])
            for review in step.context_steps
            if review in REVIEW_SOURCE_STEP
        ]
        if not relevant:
            return ""
        mappings = ", ".join(
            f"#{review}=use unchecked output from #{source}"
            for review, source in relevant
        )
        return (
            "RUN MODE OVERRIDE — SEMANTIC AI REVIEW STEPS DISABLED\n"
            "Use the direct outputs listed below wherever this prompt refers to AI-reviewed versions.\n"
            "Do not relabel them as AI-reviewed, validated, patched, certified, or accepted by semantic review.\n"
            "Preserve review_status: unchecked_by_user_choice wherever the output structure permits it.\n"
            f"Relevant fallback map: {mappings}.\n"
            "Local YAML validation checks structure only and does not replace semantic review.\n"
            "END RUN MODE OVERRIDE\n\n"
        )

    def _yaml_review_responsibility_block(self, step: StepDefinition) -> str:
        assert self.session is not None
        source_step_id = self._review_yaml_profile_step(step.step_id)
        if source_step_id is None:
            return ""
        source_report = self.session.load_yaml_validation_report(source_step_id)
        local_authoritative = (
            self.session.local_yaml_validation_enabled
            and self.yaml_validator.dependency_available
            and self.yaml_validator.has_profile(source_step_id, self.session.selected_addon)
            and bool(source_report)
            and str(source_report.get("status")) not in {"disabled", "unavailable", "empty", "not_applicable"}
        )
        if local_authoritative:
            return (
                "YAML VALIDATION / SEMANTIC REVIEW SEPARATION — RUNNER-GENERATED\n"
                "The runner-generated local validation result and any LOCAL YAML VALIDATION HANDOFF are authoritative for YAML syntax, duplicate keys, missing keys, unexpected keys, type mismatches, and explicitly allowed values.\n"
                "Do not independently re-audit the complete YAML key tree. This instruction overrides generic full-structure or full-key-audit wording elsewhere in this prompt.\n"
                "Check semantic field use, claim boundaries, source and route consistency, contradictions, over-triggering, and whether every listed local finding was safely resolved.\n"
                "A locally clean YAML structure is not evidence and does not establish semantic adequacy.\n"
                "END YAML VALIDATION / SEMANTIC REVIEW SEPARATION\n\n"
            )
        return (
            "YAML REVIEW FALLBACK — RUNNER-GENERATED\n"
            "Local YAML validation is disabled, unavailable, or has no profile for the reviewed source step. Perform the prompt's basic YAML syntax, key-structure, type, and allowed-value checks in addition to semantic review.\n"
            "Do not treat this fallback review as deterministic validation or certification.\n"
            "END YAML REVIEW FALLBACK\n\n"
        )

    def _local_yaml_validation_handoff(self, step: StepDefinition) -> str:
        assert self.session is not None
        reports = self.session.claim_yaml_validation_handoffs(step.step_id)
        if not reports:
            return ""

        lines = [
            "LOCAL YAML VALIDATION HANDOFF — RUNNER-GENERATED",
            "The runner detected unresolved structural findings in previously completed YAML output.",
            "This block is authoritative only for the local validator's structural findings; it is not case evidence and it is not a semantic review.",
            "",
        ]
        for report in reports:
            source_step = int(report.get("step_id") or 0)
            counts = report.get("counts") or {}
            lines.extend([
                f"SOURCE STEP: #{source_step}",
                f"SOURCE OUTPUT: {report.get('source_output') or 'unknown'}",
                f"REFERENCE: {report.get('reference_path') or 'unknown'}",
                (
                    "COUNTS: "
                    f"{int(counts.get('missing_keys') or 0)} missing · "
                    f"{int(counts.get('unexpected_keys') or 0)} unexpected · "
                    f"{int(counts.get('type_mismatches') or 0)} type · "
                    f"{int(counts.get('invalid_values') or 0)} invalid value"
                ),
                "FINDINGS:",
            ])
            syntax_error = report.get("syntax_error")
            if syntax_error:
                lines.append(f"- [syntax_error] <document>: {syntax_error}")
            issues = report.get("issues") or []
            for issue in issues:
                category = str(issue.get("category") or "finding")
                path = str(issue.get("path") or "<root>")
                message = str(issue.get("message") or "")
                lines.append(f"- [{category}] {path}: {message}")
            lines.append("")

        lines.extend([
            "CURRENT-STEP INSTRUCTIONS:",
            "- Treat every listed item as an unresolved deterministic structural finding, not as a semantic finding, factual source, or authorization.",
            "- If the current prompt reviews the source artifact, address each finding explicitly within the current prompt's output contract.",
            "- If the current prompt is not a review step, preserve these findings as unresolved provenance and do not silently infer missing content.",
            "- Do not invent case facts merely to fill a missing key. Use missing, unknown, not_applicable, or unresolved where the template and source material warrant it.",
            "- Do not treat a structurally clean YAML shape as proof of semantic correctness.",
            "END LOCAL YAML VALIDATION HANDOFF",
            "",
        ])
        return "\n".join(lines)

    def _persist_yaml_validation(self, result: YamlValidationResult, *, completion_state: str) -> None:
        if (
            self.session is None
            or not result.applicable
            or result.empty
            or not result.enabled
            or not result.dependency_available
        ):
            return
        if result.report_status() == "syntax_only" and self.session.step_has_unresolved_yaml_findings(self.selected_step_id):
            return
        self.session.save_yaml_validation_report(
            self.selected_step_id,
            result.to_report_dict(),
            completion_state=completion_state,
        )

    def _render_prompt(self, step: StepDefinition) -> str:
        runtime_values: dict[str, str] = {}
        if step.prompt_number == 1:
            runtime_values["RUNNER_CASE_MATERIALS"] = render_case_material_prompt_block(
                self._material_manifest_entries()
            )
        if step.prompt_number == 20:
            runtime_values["RUNNER_STAGE_1_MANIFEST"] = self._stage_1_runner_manifest(through_step=19)
        elif step.prompt_number == 21:
            runtime_values["RUNNER_STAGE_1_MANIFEST"] = self._stage_1_check_runner_manifest()
        if step.prompt_number in {22, 23, 24, 25}:
            runtime_values["RUNNER_CASE_RECORD_MANIFEST"] = self._case_record_runner_manifest(step.step_id)
        if step.prompt_number == 26:
            runtime_values["RUNNER_ITERATION_HANDOFF_MANIFEST"] = self._iteration_handoff_runner_manifest()
        if step.prompt_number in {27, 28, 29, 30, 31}:
            runtime_values["RUNNER_ARTICLE_PROFILE_CONTRACT"] = self._article_profile_contract(step.step_id)
        rendered = self.prompt_source.render(
            step.prompt_number,
            self.session.case_data,
            selected_addon=self.session.selected_addon,
            runtime_values=runtime_values,
        )
        if not self.session.ai_review_steps_enabled and step.step_id not in AI_REVIEW_STEP_IDS:
            rendered = self._fast_mode_prompt_text(rendered)
        prefix = self._yaml_review_responsibility_block(step)
        prefix += self._local_yaml_validation_handoff(step)
        if not self.session.ai_review_steps_enabled and step.step_id not in AI_REVIEW_STEP_IDS:
            prefix += self._ai_review_mode_override(step)
        return normalize_prompt_text(prefix + rendered)

    def _show_step(self, step_id: int) -> None:
        if self.session is None:
            return
        step = get_step(step_id)
        state = self.session.step_state(step_id)
        self.step_title.configure(text=f"Step #{step.step_id} — {step.title}")
        validation_note = ""
        if self.session.step_has_yaml_findings(step_id):
            count = int(state.get("yaml_validation_issue_count") or 0)
            resolved_by = self.session.yaml_findings_resolution(step_id)
            if resolved_by is None:
                validation_note = f"  |  Local YAML: {count} unresolved finding{'s' if count != 1 else ''}"
            else:
                validation_note = (
                    f"  |  Local YAML: {count} finding{'s' if count != 1 else ''} "
                    f"resolved by step #{resolved_by}"
                )
        self.step_status.configure(
            text=f"Step status: {state['status']}  |  Expected output: {step.output_label}{validation_note}"
        )
        self._refresh_file_tree(step)

        review_disabled_here = (
            not self.session.ai_review_steps_enabled
            and step_id in AI_REVIEW_STEP_IDS
            and state.get("status") == "skipped"
        )
        prompt_is_dynamic = (step.prompt_number == 1 or step.prompt_number in set(range(20, 32))) and not is_completed_step_status(state.get("status"))
        prompt = "" if prompt_is_dynamic else self.session.load_prompt(step_id)
        if review_disabled_here:
            source_step = REVIEW_SOURCE_STEP[step_id]
            prompt = (
                f"AI review step #{step_id} is disabled for this case.\n\n"
                f"The pipeline uses the saved output from step #{source_step} directly as an unchecked artifact.\n"
                "This saves a model call and accepts a higher risk of semantic imprecision.\n"
                "Local YAML validation does not replace this skipped semantic review."
            )
        elif not prompt:
            try:
                prompt = self._render_prompt(step)
                self.session.write_prompt(step_id, prompt, overwrite=prompt_is_dynamic)
            except (CaseMaterialError, PromptSourceError, StorageError) as exc:
                prompt = f"PROMPT ERROR: {exc}"
        self.prompt_text.delete("1.0", "end")
        self.prompt_text.insert("1.0", prompt)
        self.prompt_view_var.set("preview")
        self._sync_prompt_view()

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", self.session.load_output(step_id))
        self.output_text.edit_modified(False)
        self._sync_output_view_controls(step_id)
        self._sync_output_view()
        self.open_output_reader_button.configure(state="normal")
        self._apply_yaml_highlighting()
        self._validate_output()
        status = state.get("status")
        editable = status not in {"locked", "skipped"}
        resettable = is_completed_step_status(status) or status in {"current", "draft"}
        self.reset_steps_button.configure(state="normal" if resettable else "disabled")
        self.copy_prompt_button.configure(text="Copy prompt")
        self.save_button.configure(
            state="normal" if editable else "disabled",
            text="Save changes",
        )
        self.complete_button.configure(state="normal" if self.session.current_step_id() == step_id else "disabled")

    def _refresh_file_tree(self, step: StepDefinition) -> None:
        assert self.session is not None
        self.file_tree.delete(*self.file_tree.get_children())
        self.file_rows = []

        base_upload_paths = resolve_upload_files(step, self.project_root, self.session.selected_addon)
        material_entries: list[dict[str, object]] = []
        material_paths: list[Path] = []
        material_error: str | None = None
        if step.step_id == 1:
            try:
                store = self._material_store()
                material_entries = store.entries()
                material_paths = [store.path_for(entry) for entry in material_entries]
            except CaseMaterialError as exc:
                material_error = str(exc)

        self.current_upload_paths = base_upload_paths + material_paths
        if self.current_upload_paths:
            names = ", ".join(path.name for path in self.current_upload_paths)
            self.upload_summary.configure(text=f"Upload now: {names}")
            for path in base_upload_paths:
                self._insert_file_row("Upload now", path)
            for entry, path in zip(material_entries, material_paths):
                role = "Case material"
                material_id = str(entry.get("id") or "")
                if material_id:
                    role += f" · {material_id}"
                self._insert_file_row(role, path)
            first_upload_row = self.file_tree.get_children()[0]
            self.file_tree.selection_set(first_upload_row)
            self.file_tree.focus(first_upload_row)
            self.file_tree.see(first_upload_row)
        else:
            self.upload_summary.configure(text="Upload now: none — continue in the same AI service session.")

        if material_error:
            self.upload_summary.configure(text=f"Case-material manifest error: {material_error}")
            self._insert_file_row("Case materials", None, state_override="manifest error")

        for source_step in step.context_steps:
            source_state = self.session.step_state(source_step).get("status")
            path = self.session.output_path(source_step)
            role = f"Session context · Step #{source_step}"
            if (
                source_state == "skipped"
                and not self.session.ai_review_steps_enabled
                and source_step in REVIEW_SOURCE_STEP
            ):
                fallback_step = REVIEW_SOURCE_STEP[source_step]
                fallback_path = self.session.output_path(fallback_step)
                if fallback_path.exists() and fallback_path not in self.file_rows:
                    self._insert_file_row(
                        f"Unchecked context · Step #{fallback_step} (review #{source_step} skipped)",
                        fallback_path,
                    )
                else:
                    self._insert_file_row(role, None, state_override="skipped")
            elif source_state == "skipped":
                self._insert_file_row(role, None, state_override="skipped")
            elif path.exists() and path not in self.file_rows:
                self._insert_file_row(role, path)

    def _insert_file_row(self, kind: str, path: Path | None, state_override: str | None = None) -> None:
        filename = path.name if path is not None else "—"
        state = state_override or ("available" if path is not None and path.exists() else "missing")
        self.file_rows.append(path)
        self.file_tree.insert("", "end", iid=str(len(self.file_rows) - 1), values=(kind, filename, state))

    def reset_selected_step(self) -> None:
        if self.session is None:
            return
        step_id = self.selected_step_id
        status = self.session.step_state(step_id).get("status")
        if not is_completed_step_status(status) and status not in {"current", "draft"}:
            self._set_status(f"Step #{step_id} cannot be reset from its current state: {status}.")
            return
        confirmed = ask_centered_yes_no(
            self,
            "Reset step and following steps",
            (
                f"Reset step #{step_id} and every following step? Existing prompt and output files "
                "will be archived under history/route_revisions before they are cleared. "
                "Dependent route decisions will also be cleared when necessary."
            ),
        )
        if not confirmed:
            self._set_status(f"Reset cancelled for step #{step_id}.")
            return
        try:
            archive_dir = self.session.reset_from_step(step_id)
        except StorageError as exc:
            messagebox.showerror("Could not reset steps", str(exc), parent=self)
            return
        self.selected_step_id = step_id
        self._refresh_all()
        archive_note = f" Archived previous work in {archive_dir.name}." if archive_dir is not None else ""
        self._set_status(f"Step #{step_id} and following steps reset.{archive_note}")

    def select_current_step(self) -> None:
        if self.session is None:
            return
        current = self.session.current_step_id()
        if current is None:
            messagebox.showinfo("No open step", "This run is waiting for a route or is complete through the implemented steps.", parent=self)
            return
        self.selected_step_id = current
        self._refresh_step_list()
        self._show_step(current)

    def copy_prompt(self) -> None:
        text = self.prompt_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_status("Copy prompt skipped: the rendered prompt is empty.")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update_idletasks()
        self._flash_button(self.copy_prompt_button, "Copied!", "Copy prompt")
        self._set_status(f"Prompt for step #{self.selected_step_id} copied to clipboard.")

    def import_output(self) -> None:
        path = filedialog.askopenfilename(title="Import AI response", filetypes=[("Text files", "*.txt *.md *.yaml *.yml *.json"), ("All files", "*.*")])
        if not path:
            self._set_status("Import response cancelled.")
            return
        try:
            data = Path(path).read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            data = Path(path).read_text(encoding="cp1252", errors="replace")
        except OSError as exc:
            messagebox.showerror("Import failed", str(exc), parent=self)
            return
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", data)
        self.output_text.edit_modified(False)
        self._apply_yaml_highlighting()
        if self.output_view_var.get() == "preview":
            self._render_output_preview()
        validation = self._validate_output()
        self._set_status(f"Response imported: {path} · {validation.short_summary()}")

    def save_draft(self) -> None:
        if self.session is None:
            return
        text = self.output_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_status("Save skipped: the output field is empty.")
            messagebox.showwarning("Empty output", "There is no output to save.", parent=self)
            return
        validation = self._validate_output()
        try:
            path = self.session.write_output(self.selected_step_id, text, complete=False)
            completion_state = (
                "completed"
                if is_completed_step_status(self.session.step_state(self.selected_step_id).get("status"))
                else "draft"
            )
            self._persist_yaml_validation(validation, completion_state=completion_state)
            self._refresh_step_list()
            self._flash_button(self.save_button, "Saved!", "Save changes")
            self._set_status(f"Output saved: {path.name} · {validation.short_summary()}")
        except StorageError as exc:
            messagebox.showerror("Save failed", str(exc), parent=self)


    def _review_iteration_handoff_before_completion(self, text: str) -> str | None:
        try:
            dialog = IterationHandoffDialog(self, text)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(
                "Iteration Handoff review unavailable",
                f"The Iteration Handoff YAML could not be opened for user review.\n\n{exc}",
                parent=self,
            )
            self._set_status("Step #26 completion cancelled: Iteration Handoff review could not open.")
            return None
        self.wait_window(dialog)
        if dialog.result_text is None:
            self._set_status("Step #26 completion cancelled before confirming Iteration Handoff user response.")
            return None
        return dialog.result_text

    def _finish_without_article_after_handoff(self) -> None:
        assert self.session is not None
        route = {"route_type": "no_article"}
        existing = self.session.session_data.get("article_route")
        if not self._confirm_route_change("article", existing, route, ("route_type", "article_profile")):
            self._set_status("No-article decision cancelled; article route remains pending.")
            return
        try:
            self.session.set_article_route(route)
        except StorageError as exc:
            messagebox.showerror("Could not save article decision", str(exc), parent=self)
            return
        self.selected_step_id = 26
        self._refresh_all()
        message = "No article selected. The guided pipeline is complete through the confirmed Iteration Handoff."
        self._set_status(message)
        messagebox.showinfo("Article decision saved", message, parent=self)

    def _handle_iteration_handoff_next_action(self) -> bool:
        if self.session is None:
            return False
        handoff, reason = self._load_approved_iteration_handoff()
        dialog = IterationHandoffNextActionDialog(
            self,
            followup_available=handoff is not None,
            reason=reason,
        )
        self.wait_window(dialog)
        action = dialog.result or "decide_later"
        if action == "create_followup":
            self.create_followup_case_from_handoff()
            return True
        if action == "continue_article":
            self.set_article_route()
            return True
        if action == "finish_without_article":
            self._finish_without_article_after_handoff()
            return True
        self._set_status("Step #26 completed; follow-up and article decisions can be made later from the current case state.")
        return True

    def complete_step(self) -> None:
        if self.session is None:
            return
        current = self.session.current_step_id()
        if current != self.selected_step_id:
            self._set_status("Complete step skipped: only the current step can be completed.")
            messagebox.showwarning("Not the current step", "Only the current step can be completed.", parent=self)
            return
        text = self.output_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_status("Complete step skipped: the output field is empty.")
            messagebox.showwarning("Empty output", "Paste the AI service response first.", parent=self)
            return
        if not self._yaml_completion_allowed():
            return
        if current == 26:
            reviewed_text = self._review_iteration_handoff_before_completion(text)
            if reviewed_text is None:
                return
            text = reviewed_text
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", text)
            self.output_text.edit_modified(True)
            self._apply_yaml_highlighting()
            validation = self._validate_output()
            if validation.has_blocking_syntax_error:
                messagebox.showerror(
                    "Invalid annotated handoff",
                    validation.short_summary(),
                    parent=self,
                )
                return
        if not ask_centered_yes_no(self, "Complete step", "Save the current output and complete this step?"):
            self._set_status(f"Step #{current} completion cancelled.")
            return
        try:
            post_completion_action_handled = False
            validation = self._validate_output()
            self.session.write_output(current, text, complete=False)
            self._persist_yaml_validation(validation, completion_state="draft")
            self.session.complete_step(current)
            self._persist_yaml_validation(validation, completion_state="completed")
            run_status = str(self.session.session_data.get("run_status"))
            if run_status == "awaiting_addon_route":
                self.selected_step_id = self.session.required_route_step("addon")
                self._refresh_all()
                self.set_addon_route()
            elif run_status == "awaiting_mip_route":
                self.selected_step_id = self.session.required_route_step("mip")
                self._refresh_all()
                self.set_mip_route()
            elif run_status == "awaiting_ahp_route":
                self.selected_step_id = self.session.required_route_step("ahp")
                self._refresh_all()
                self.set_ahp_route()
            elif run_status == "awaiting_article_route":
                self.selected_step_id = self.session.required_route_step("article")
                self._refresh_all()
                if current == 26:
                    post_completion_action_handled = self._handle_iteration_handoff_next_action()
                else:
                    self.set_article_route()
                    post_completion_action_handled = True
            elif run_status == "pipeline_complete_with_article":
                self.selected_step_id = current
                self._refresh_all()
                messagebox.showinfo(
                    "Pipeline complete",
                    "The guided run and optional Markdown article workflow are complete.",
                    parent=self,
                )
            else:
                next_step = self.session.current_step_id()
                if next_step is not None:
                    self.selected_step_id = next_step
                self._refresh_all()
            if not post_completion_action_handled:
                if validation.issues:
                    self._set_status(
                        f"Step #{current} completed with {len(validation.issues)} unresolved local YAML finding"
                        f"{'s' if len(validation.issues) != 1 else ''}."
                    )
                else:
                    self._set_status(f"Step #{current} completed.")
        except StorageError as exc:
            messagebox.showerror("Could not complete step", str(exc), parent=self)

    def _first_gate_value(self, step_ids: tuple[int, ...], reader) -> GateValue:
        assert self.session is not None
        fallback: GateValue | None = None
        for step_id in step_ids:
            text = self.session.load_output(step_id)
            if not text.strip():
                continue
            result = reader(text, source_step=step_id)
            fallback = result
            if result.status != "key_not_found":
                return result
        return fallback or GateValue(None, "key_not_found", "unknown", source_step=None)

    def set_active_route(self) -> None:
        if self.session is None:
            return
        status = self.session.session_data.get("run_status")
        if status == "awaiting_addon_route":
            self.set_addon_route()
        elif status == "awaiting_mip_route":
            self.set_mip_route()
        elif status == "awaiting_ahp_route":
            self.set_ahp_route()
        elif status == "awaiting_article_route":
            self.set_article_route()
        elif self.session.route_ready("article"):
            self.set_article_route()
        elif self.session.route_ready("ahp"):
            self.set_ahp_route()
        elif self.session.route_ready("mip"):
            self.set_mip_route()
        elif self.session.route_ready("addon"):
            self.set_addon_route()
        else:
            messagebox.showinfo("Route not available", "No route decision is available yet.", parent=self)

    @staticmethod
    def _route_signature(route: dict | None, fields: tuple[str, ...]) -> tuple | None:
        if not route:
            return None
        return tuple(route.get(field) for field in fields)

    def _confirm_route_change(self, label: str, existing: dict | None, proposed: dict, fields: tuple[str, ...]) -> bool:
        if not existing:
            return True
        if self._route_signature(existing, fields) == self._route_signature(proposed, fields):
            return True
        return ask_centered_yes_no(
            self,
            f"Change {label} route",
            "This changes the saved route. Dependent active steps will be reset. Existing dependent prompt/output files will be archived under history/route_revisions first. Continue?",
        )

    def set_addon_route(self) -> None:
        if self.session is None:
            return
        if not self.session.route_ready("addon"):
            required = self.session.required_route_step("addon")
            messagebox.showinfo("Route not available", f"Complete step #{required} first.", parent=self)
            return
        recommendation = self._first_gate_value((7, 6), read_addon_recommendation)
        gate_status = self._first_gate_value((7, 6), read_addon_gate_status)
        existing = self.session.session_data.get("route")
        dialog = RouteDialog(self, recommendation, gate_status, existing=existing)
        self.wait_window(dialog)
        if dialog.result is None:
            return
        if not self._confirm_route_change("Add-on", existing, dialog.result, ("route_type", "selected_addon")):
            return
        try:
            changed = self.session.set_route(dialog.result)
        except StorageError as exc:
            messagebox.showerror("Could not save route", str(exc), parent=self)
            return

        if changed or not existing:
            if dialog.result["route_type"] == "selected_addon":
                self.selected_step_id = 8
                message = f"Route saved: {dialog.result.get('selected_addon')}. Continue with step #8."
            else:
                self.selected_step_id = 11
                message = "Core-only route saved. Steps #8–#10 were skipped; continue with step #11."
        else:
            message = "Add-on route metadata refreshed; the active pipeline position was preserved."
        self._refresh_all()
        self._set_status(message)
        messagebox.showinfo("Add-on route saved", message, parent=self)

    def set_mip_route(self) -> None:
        if self.session is None:
            return
        if not self.session.route_ready("mip"):
            required = self.session.required_route_step("mip")
            messagebox.showinfo("Route not available", f"Complete step #{required} first.", parent=self)
            return
        recommendation = self._first_gate_value((12, 11), read_mip_recommendation)
        existing = self.session.session_data.get("mip_route")
        dialog = MipRouteDialog(self, recommendation, existing=existing)
        self.wait_window(dialog)
        if dialog.result is None:
            return
        if not self._confirm_route_change("MIP", existing, dialog.result, ("route_type",)):
            return
        try:
            changed = self.session.set_mip_route(dialog.result)
        except StorageError as exc:
            messagebox.showerror("Could not save MIP route", str(exc), parent=self)
            return

        if changed or not existing:
            if dialog.result["route_type"] == "use_mip":
                self.selected_step_id = 13
                message = "MIP route saved. Continue with step #13."
            else:
                self.selected_step_id = 20
                message = "No-MIP route saved. Steps #13–#19 were skipped; continue with step #20."
        else:
            message = "MIP route metadata refreshed; the active pipeline position was preserved."
        self._refresh_all()
        self._set_status(message)
        messagebox.showinfo("MIP route saved", message, parent=self)

    def set_ahp_route(self) -> None:
        if self.session is None:
            return
        if not self.session.route_ready("ahp"):
            required = self.session.required_route_step("ahp")
            messagebox.showinfo("Route not available", f"Complete step #{required} first.", parent=self)
            return
        recommendation = self._first_gate_value((17, 16), read_ahp_recommendation)
        existing = self.session.session_data.get("ahp_route")
        dialog = AhpRouteDialog(self, recommendation, existing=existing)
        self.wait_window(dialog)
        if dialog.result is None:
            return
        if not self._confirm_route_change("AHP", existing, dialog.result, ("route_type",)):
            return
        try:
            changed = self.session.set_ahp_route(dialog.result)
        except StorageError as exc:
            messagebox.showerror("Could not save AHP route", str(exc), parent=self)
            return

        if changed or not existing:
            if dialog.result["route_type"] == "use_ahp":
                self.selected_step_id = 18
                message = "AHP route saved. Continue with step #18."
            else:
                self.selected_step_id = 20
                message = "No-AHP route saved. Steps #18–#19 were skipped; continue with step #20."
        else:
            message = "AHP route metadata refreshed; the active pipeline position was preserved."
        self._refresh_all()
        self._set_status(message)
        messagebox.showinfo("AHP route saved", message, parent=self)

    def set_article_route(self) -> None:
        if self.session is None:
            return
        if not self.session.route_ready("article"):
            required = self.session.required_route_step("article")
            messagebox.showinfo("Article decision not available", f"Complete step #{required} first.", parent=self)
            return
        existing = self.session.session_data.get("article_route")
        dialog = ArticleRouteDialog(
            self,
            existing=existing,
            ai_review_steps_enabled=self.session.ai_review_steps_enabled,
        )
        self.wait_window(dialog)
        if dialog.result is None:
            return
        if not self._confirm_route_change("article", existing, dialog.result, ("route_type", "article_profile")):
            return
        try:
            changed = self.session.set_article_route(dialog.result)
        except StorageError as exc:
            messagebox.showerror("Could not save article decision", str(exc), parent=self)
            return

        if changed or not existing:
            if dialog.result["route_type"] == "generate_article":
                self.selected_step_id = 27
                message = f"Article generation selected: {dialog.result.get('article_profile', 'full_analysis_article').replace('_', ' ')}. Continue with step #27."
            else:
                self.selected_step_id = 26
                message = "No article selected. The guided pipeline is complete through the Iteration Handoff."
        else:
            message = "Article decision metadata refreshed; the active pipeline position was preserved."
        self._refresh_all()
        self._set_status(message)
        messagebox.showinfo("Article decision saved", message, parent=self)

    def _selected_file_path(self) -> Path | None:
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showinfo("No file selected", "Select a row in the file list first.", parent=self)
            return None
        try:
            return self.file_rows[int(selection[0])]
        except (IndexError, ValueError):
            return None

    def open_selected_file(self) -> None:
        path = self._selected_file_path()
        if path is not None and self._safe_open(path):
            self._set_status(f"Opened file: {path.name}")

    def open_selected_file_folder(self) -> None:
        path = self._selected_file_path()
        if path is None:
            return
        try:
            open_parent(path)
            self._set_status(f"Opened folder for: {path.name}")
        except OpenPathError as exc:
            messagebox.showerror("Could not open folder", str(exc), parent=self)

    def check_sources(self) -> None:
        try:
            manifest = SourceManifest.load(self.source_manifest_path, self.project_root)
        except SourceManifestError as exc:
            messagebox.showerror("Could not check sources", str(exc), parent=self)
            return

        statuses = manifest.check()
        dialog = SourceCheckDialog(self, statuses, self.source_manifest_path.name)
        self.wait_window(dialog)
        if not dialog.result:
            missing = sum(1 for item in statuses if not item.present)
            self._set_status(f"Source check complete: {missing} missing of {len(statuses)}.")
            return

        existing_count = sum(1 for item in statuses if item.present)
        if existing_count:
            confirmed = ask_centered_yes_no(
                self,
                "Replace existing resources",
                (
                    f"{existing_count} existing resource file(s) will be replaced. "
                    f"Download all {len(statuses)} sources and templates from the URLs "
                    f"in {self.source_manifest_path.name}?"
                ),
            )
            if not confirmed:
                self._set_status("Source download cancelled.")
                return

        def progress(index: int, total: int, entry) -> None:
            self._set_status(f"Downloading resource {index} of {total}: {entry.label}")
            self.update_idletasks()

        try:
            results = manifest.download_all(progress=progress)
        except SourceDownloadError as exc:
            messagebox.showerror(
                "Resource download failed",
                f"No source or template files were replaced.\n\n{exc}",
                parent=self,
            )
            self._set_status("Resource download failed.")
            return

        after = manifest.check()
        missing_after = [item for item in after if not item.present]
        if missing_after:
            messagebox.showwarning(
                "Resource download incomplete",
                (
                    f"Downloaded {len(results)} resource file(s), but "
                    f"{len(missing_after)} expected source or template file(s) "
                    "are still missing."
                ),
                parent=self,
            )
        else:
            messagebox.showinfo(
                "Resources downloaded",
                (
                    f"All {len(results)} configured PMS, MIP/AHP, and "
                    "PMS-DISCIPLINE YAML files were downloaded successfully."
                ),
                parent=self,
            )

        self._set_status(
            f"Resource download complete: {len(results)} file(s)."
        )
        if self.session is not None:
            self._refresh_all()

    def _has_unsaved_output(self) -> bool:
        if self.session is None:
            return False
        current_text = self.output_text.get("1.0", "end-1c")
        saved_text = self.session.load_output(self.selected_step_id)
        return current_text != saved_text

    def exit_app(self) -> None:
        if self._has_unsaved_output():
            confirmed = ask_centered_yes_no(
                self,
                "Exit PMS-ORCHESTRATOR",
                "The current AI service output contains unsaved changes. Exit without saving them?",
            )
            if not confirmed:
                return
        self.destroy()

    def open_case_folder(self) -> None:
        if self.session is None:
            messagebox.showinfo("No case", "Create or open a case first.", parent=self)
            return
        if self._safe_open(self.session.case_dir):
            self._set_status(f"Opened case folder: {self.session.case_dir.name}")

    def _safe_open(self, path: Path) -> bool:
        try:
            open_path(path)
            return True
        except OpenPathError as exc:
            messagebox.showerror("Could not open path", str(exc), parent=self)
            return False


def run(project_root: Path) -> None:
    try:
        app = OrchestratorApp(project_root)
    except (PromptSourceError, StorageError) as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("PMS-ORCHESTRATOR startup error", str(exc))
        root.destroy()
        return
    app.mainloop()
