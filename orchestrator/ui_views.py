from __future__ import annotations

import re
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Mapping

from .dialogs import finalize_dialog


YAML_TAG_NAMES = (
    "yaml_key",
    "yaml_string",
    "yaml_number",
    "yaml_literal",
    "yaml_comment",
    "yaml_marker",
)


def is_markdown_filename(filename: str) -> bool:
    return filename.lower().endswith((".md", ".markdown"))


def configure_yaml_tags(widget: tk.Text, *, dark: bool) -> None:
    colors = (
        {
            "yaml_key": "#79c0ff",
            "yaml_string": "#a5d6ff",
            "yaml_number": "#ffa657",
            "yaml_literal": "#ff7b72",
            "yaml_comment": "#8b949e",
            "yaml_marker": "#d2a8ff",
        }
        if dark
        else {
            "yaml_key": "#0550ae",
            "yaml_string": "#0a3069",
            "yaml_number": "#953800",
            "yaml_literal": "#cf222e",
            "yaml_comment": "#6e7781",
            "yaml_marker": "#8250df",
        }
    )
    for tag_name, color in colors.items():
        widget.tag_configure(tag_name, foreground=color)
    widget.tag_raise("yaml_comment")
    widget.tag_raise("yaml_string")


def apply_yaml_highlighting(widget: tk.Text, content: str, *, dark: bool) -> None:
    configure_yaml_tags(widget, dark=dark)
    for tag_name in YAML_TAG_NAMES:
        widget.tag_remove(tag_name, "1.0", "end")
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
            widget.tag_add(tag_name, f"1.0+{start}c", f"1.0+{stop}c")


def _font_copy(name: str, *, size_delta: int = 0, weight: str | None = None, slant: str | None = None, family: str | None = None) -> tkfont.Font:
    base = tkfont.nametofont(name).copy()
    if size_delta:
        size = int(base.cget("size"))
        base.configure(size=max(8, size + size_delta))
    if weight is not None:
        base.configure(weight=weight)
    if slant is not None:
        base.configure(slant=slant)
    if family is not None:
        base.configure(family=family)
    return base


def configure_markdown_tags(widget: tk.Text, palette: Mapping[str, str]) -> None:
    # Retain references on the widget so Tkinter font objects are not garbage-collected.
    fonts = {
        "h1": _font_copy("TkDefaultFont", size_delta=7, weight="bold"),
        "h2": _font_copy("TkDefaultFont", size_delta=5, weight="bold"),
        "h3": _font_copy("TkDefaultFont", size_delta=3, weight="bold"),
        "h4": _font_copy("TkDefaultFont", size_delta=2, weight="bold"),
        "h5": _font_copy("TkDefaultFont", size_delta=1, weight="bold"),
        "h6": _font_copy("TkDefaultFont", weight="bold"),
        "bold": _font_copy("TkDefaultFont", weight="bold"),
        "italic": _font_copy("TkDefaultFont", slant="italic"),
        "code": _font_copy("TkFixedFont"),
    }
    setattr(widget, "_markdown_fonts", fonts)
    widget.tag_configure("md_h1", font=fonts["h1"], spacing1=10, spacing3=6)
    widget.tag_configure("md_h2", font=fonts["h2"], spacing1=9, spacing3=5)
    widget.tag_configure("md_h3", font=fonts["h3"], spacing1=8, spacing3=4)
    widget.tag_configure("md_h4", font=fonts["h4"], spacing1=7, spacing3=3)
    widget.tag_configure("md_h5", font=fonts["h5"], spacing1=6, spacing3=3)
    widget.tag_configure("md_h6", font=fonts["h6"], spacing1=5, spacing3=2)
    widget.tag_configure("md_bold", font=fonts["bold"])
    widget.tag_configure("md_italic", font=fonts["italic"])
    widget.tag_configure(
        "md_inline_code",
        font=fonts["code"],
        background=palette.get("panel", palette.get("field", "#ffffff")),
    )
    widget.tag_configure(
        "md_code_block",
        font=fonts["code"],
        background=palette.get("panel", palette.get("field", "#ffffff")),
        lmargin1=16,
        lmargin2=16,
        spacing1=4,
        spacing3=4,
    )
    widget.tag_configure("md_quote", foreground=palette.get("muted", palette.get("fg", "#555555")), lmargin1=18, lmargin2=18)
    widget.tag_configure("md_list", lmargin1=12, lmargin2=30, spacing1=1, spacing3=1)
    widget.tag_configure("md_table", font=fonts["code"], lmargin1=8, lmargin2=8)
    widget.tag_configure("md_rule", foreground=palette.get("muted", palette.get("fg", "#555555")), justify="center")


_INLINE_PATTERN = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|__[^_]+__|(?<!\*)\*[^*]+\*(?!\*)|(?<!_)_[^_]+_(?!_))")


def _insert_inline(widget: tk.Text, text: str, base_tags: tuple[str, ...] = ()) -> None:
    position = 0
    for match in _INLINE_PATTERN.finditer(text):
        if match.start() > position:
            widget.insert("end", text[position:match.start()], base_tags)
        token = match.group(0)
        if token.startswith("`"):
            widget.insert("end", token[1:-1], base_tags + ("md_inline_code",))
        elif token.startswith(("**", "__")):
            widget.insert("end", token[2:-2], base_tags + ("md_bold",))
        else:
            widget.insert("end", token[1:-1], base_tags + ("md_italic",))
        position = match.end()
    if position < len(text):
        widget.insert("end", text[position:], base_tags)


def render_markdown(widget: tk.Text, text: str, palette: Mapping[str, str]) -> None:
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    configure_markdown_tags(widget, palette)
    in_code = False
    code_language = ""
    lines = text.splitlines()
    for line in lines:
        fence = re.match(r"^\s*```\s*([^`]*)$", line)
        if fence:
            if not in_code:
                in_code = True
                code_language = fence.group(1).strip()
                if code_language:
                    widget.insert("end", f"{code_language}\n", ("md_code_block", "md_italic"))
            else:
                in_code = False
                code_language = ""
                widget.insert("end", "\n")
            continue
        if in_code:
            widget.insert("end", line + "\n", ("md_code_block",))
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            _insert_inline(widget, heading.group(2), (f"md_h{level}",))
            widget.insert("end", "\n")
            continue
        if re.match(r"^\s*(?:---+|\*\*\*+|___+)\s*$", line):
            widget.insert("end", "────────────────────────────────────────\n", ("md_rule",))
            continue
        quote = re.match(r"^\s*>\s?(.*)$", line)
        if quote:
            _insert_inline(widget, quote.group(1), ("md_quote",))
            widget.insert("end", "\n", ("md_quote",))
            continue
        unordered = re.match(r"^(\s*)[-+*]\s+(.+)$", line)
        if unordered:
            indent = len(unordered.group(1)) // 2
            widget.insert("end", "  " * indent + "• ", ("md_list",))
            _insert_inline(widget, unordered.group(2), ("md_list",))
            widget.insert("end", "\n", ("md_list",))
            continue
        ordered = re.match(r"^(\s*)(\d+)\.\s+(.+)$", line)
        if ordered:
            indent = len(ordered.group(1)) // 2
            widget.insert("end", "  " * indent + ordered.group(2) + ". ", ("md_list",))
            _insert_inline(widget, ordered.group(3), ("md_list",))
            widget.insert("end", "\n", ("md_list",))
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            # Skip Markdown alignment-only rows; render all other table rows in a fixed-width font.
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
                continue
            widget.insert("end", " | ".join(cells) + "\n", ("md_table",))
            continue
        if not line.strip():
            widget.insert("end", "\n")
            continue
        _insert_inline(widget, line)
        widget.insert("end", "\n")
    widget.configure(state="disabled")


def render_plain(widget: tk.Text, text: str, palette: Mapping[str, str], *, yaml: bool = False) -> None:
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", text)
    if yaml:
        apply_yaml_highlighting(widget, text, dark=palette.get("bg") == "#202124")
    widget.configure(state="disabled")


class HelpDocumentDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, title: str, markdown_text: str) -> None:
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.minsize(780, 600)

        body = ScrolledText(self, width=104, height=34, wrap="word")
        body.pack(fill="both", expand=True, padx=14, pady=(14, 10))
        palette = getattr(parent, "theme_palette", {}) or {"fg": "#202124", "muted": "#5f6368", "panel": "#ffffff"}
        render_markdown(body, markdown_text, palette)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Button(buttons, text="Close", command=self.destroy).pack(side="right")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after_idle(lambda: finalize_dialog(self, parent))


class OutputReader(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Misc,
        *,
        title: str,
        content: str,
        content_kind: str,
        palette: Mapping[str, str],
    ) -> None:
        super().__init__(parent)
        self.title(title)
        self.content = content
        self.content_kind = content_kind
        self.palette = dict(palette)
        self.fullscreen = False
        self.wrap_var = tk.BooleanVar(value=True)
        self.view_var = tk.StringVar(value="preview" if content_kind == "markdown" else "raw")
        self.search_var = tk.StringVar(value="")
        self.search_status_var = tk.StringVar(value="")

        toolbar = ttk.Frame(self, padding=(8, 6))
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Copy", command=self.copy).pack(side="left")
        ttk.Button(toolbar, text="Select all", command=self.select_all).pack(side="left", padx=(6, 0))
        ttk.Checkbutton(toolbar, text="Wrap", variable=self.wrap_var, command=self._sync_wrap).pack(side="left", padx=(12, 0))

        if content_kind == "markdown":
            ttk.Label(toolbar, text="View:").pack(side="left", padx=(14, 4))
            ttk.Radiobutton(toolbar, text="Raw", variable=self.view_var, value="raw", command=self.render).pack(side="left")
            ttk.Radiobutton(toolbar, text="Preview", variable=self.view_var, value="preview", command=self.render).pack(side="left")

        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side="right")

        ttk.Label(search_frame, text="Find:").pack(side="left")

        entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=26,
        )
        entry.pack(side="left", padx=(5, 4))

        ttk.Label(
            search_frame,
            textvariable=self.search_status_var,
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            search_frame,
            text="Find",
            command=self.find,
        ).pack(side="left")

        ttk.Button(
            search_frame,
            text="Close Reader",
            command=self.destroy,
        ).pack(side="left", padx=(6, 0))

        entry.bind("<Return>", lambda _event: self.find())

        self.body = ScrolledText(self, wrap="word", undo=False)
        self.body.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.body.tag_configure("search_match", background="#ffd33d", foreground="#111111")
        self.body.bind("<Control-a>", self._select_all_event)
        self.body.bind("<Control-A>", self._select_all_event)

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.escape)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        apply_theme = getattr(parent, "apply_theme_to_window", None)
        if callable(apply_theme):
            apply_theme(self)
        self.render()
        self.after_idle(self._maximize)

    def _maximize(self) -> None:
        try:
            self.state("zoomed")
        except tk.TclError:
            width = self.winfo_screenwidth()
            height = self.winfo_screenheight()
            self.geometry(f"{width}x{height}+0+0")
        self.lift()

    def render(self) -> None:
        if self.content_kind == "markdown" and self.view_var.get() == "preview":
            render_markdown(self.body, self.content, self.palette)
        else:
            render_plain(self.body, self.content, self.palette, yaml=self.content_kind == "yaml")
        self.body.tag_configure("search_match", background="#ffd33d", foreground="#111111")
        self._sync_wrap()
        self.find(clear_only=True)

    def _sync_wrap(self) -> None:
        self.body.configure(wrap="word" if self.wrap_var.get() else "none")

    def copy(self) -> None:
        try:
            text = self.body.get("sel.first", "sel.last")
        except tk.TclError:
            text = self.content
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update_idletasks()

    def select_all(self) -> None:
        self.body.configure(state="normal")
        self.body.tag_add("sel", "1.0", "end-1c")
        self.body.mark_set("insert", "1.0")
        self.body.see("1.0")
        self.body.configure(state="disabled")

    def _select_all_event(self, _event: object) -> str:
        self.select_all()
        return "break"

    def find(self, *, clear_only: bool = False) -> None:
        self.body.configure(state="normal")
        self.body.tag_remove("search_match", "1.0", "end")
        term = self.search_var.get()
        if clear_only or not term:
            self.search_status_var.set("")
            self.body.configure(state="disabled")
            return
        start = "1.0"
        matches: list[str] = []
        while True:
            index = self.body.search(term, start, stopindex="end", nocase=True)
            if not index:
                break
            end = f"{index}+{len(term)}c"
            self.body.tag_add("search_match", index, end)
            matches.append(index)
            start = end
        if matches:
            self.body.see(matches[0])
            self.search_status_var.set(f"{len(matches)} match{'es' if len(matches) != 1 else ''}")
        else:
            self.search_status_var.set("No matches")
        self.body.configure(state="disabled")

    def toggle_fullscreen(self, _event: object | None = None) -> str:
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"

    def escape(self, _event: object | None = None) -> str:
        if self.fullscreen:
            self.fullscreen = False
            self.attributes("-fullscreen", False)
        else:
            self.destroy()
        return "break"
