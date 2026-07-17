from __future__ import annotations

import difflib
import re
from dataclasses import dataclass


class ArticlePatchError(ValueError):
    pass


ARTICLE_READY_WITH_NO_PATCH = "article_ready_with_no_patch_required"
ARTICLE_READY_AFTER_MINOR_PATCH = "article_ready_after_minor_patch"
VALID_ARTICLE_CHECK_STATUSES = {
    ARTICLE_READY_WITH_NO_PATCH,
    ARTICLE_READY_AFTER_MINOR_PATCH,
    "major_revision_required",
    "source_record_insufficient_for_article",
    "human_review_required_before_article_use",
}


@dataclass(frozen=True)
class ArticlePatch:
    title: str
    operation: str
    anchor: str
    replacement: str


@dataclass(frozen=True)
class ArticlePatchReview:
    status: str
    patches: tuple[ArticlePatch, ...]


_STATUS_RE = re.compile(
    r"^### Final check status\s*$\n+(?P<status>[a-z_]+)\s*$",
    re.MULTILINE,
)
_PATCH_HEADER_RE = re.compile(r"^\*\*Patch\s+\d+\s+—\s+(?P<title>.+?)\*\*\s*$", re.MULTILINE)


def parse_article_patch_review(text: str) -> ArticlePatchReview:
    status_match = _STATUS_RE.search(text)
    if not status_match:
        raise ArticlePatchError("Missing or malformed '### Final check status' section.")
    status = status_match.group("status")
    if status not in VALID_ARTICLE_CHECK_STATUSES:
        raise ArticlePatchError(f"Unsupported final article check status: {status}")

    headers = list(_PATCH_HEADER_RE.finditer(text))
    patches: list[ArticlePatch] = []
    for index, header in enumerate(headers):
        start = header.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        block = text[start:end].strip()
        title = header.group("title").strip()
        if block.startswith("Find:\n"):
            body = block[len("Find:\n"):].lstrip("\n")
            marker = "\n\nReplace with:\n"
            if marker not in body:
                raise ArticlePatchError(f"Patch '{title}' is missing 'Replace with:'.")
            anchor, replacement = body.split(marker, 1)
            patches.append(
                ArticlePatch(
                    title=title,
                    operation="replace",
                    anchor=anchor.strip("\n"),
                    replacement=replacement.lstrip("\n").rstrip(),
                )
            )
        elif block.startswith("Insert after:\n"):
            body = block[len("Insert after:\n"):].lstrip("\n")
            marker = "\n\nInsert:\n"
            if marker not in body:
                raise ArticlePatchError(f"Patch '{title}' is missing 'Insert:'.")
            anchor, replacement = body.split(marker, 1)
            patches.append(
                ArticlePatch(
                    title=title,
                    operation="insert_after",
                    anchor=anchor.strip("\n"),
                    replacement=replacement.lstrip("\n").rstrip(),
                )
            )
        else:
            raise ArticlePatchError(f"Patch '{title}' has an unsupported patch shape.")

    if status == ARTICLE_READY_AFTER_MINOR_PATCH and not patches:
        raise ArticlePatchError("Minor-patch status requires at least one exact patch.")
    if status != ARTICLE_READY_AFTER_MINOR_PATCH and patches:
        raise ArticlePatchError(f"Status '{status}' must not contain executable patches.")
    return ArticlePatchReview(status=status, patches=tuple(patches))


def apply_article_patches(article: str, patches: tuple[ArticlePatch, ...]) -> str:
    result = article
    for patch in patches:
        if not patch.anchor:
            raise ArticlePatchError(f"Patch '{patch.title}' has an empty anchor.")
        count = result.count(patch.anchor)
        if count != 1:
            raise ArticlePatchError(
                f"Patch '{patch.title}' requires exactly one anchor match; found {count}."
            )
        if patch.operation == "replace":
            result = result.replace(patch.anchor, patch.replacement, 1)
        elif patch.operation == "insert_after":
            insertion = patch.anchor + "\n\n" + patch.replacement
            result = result.replace(patch.anchor, insertion, 1)
        else:
            raise ArticlePatchError(f"Patch '{patch.title}' uses unsupported operation '{patch.operation}'.")
    return result


def render_article_patch_diff(
    article: str,
    patches: tuple[ArticlePatch, ...],
    *,
    fromfile: str = "step_30_final_article.md",
    tofile: str = "step_30_final_article.patched.md",
) -> tuple[str, str]:
    """Return the fully patched article and a unified diff preview."""
    patched = apply_article_patches(article, patches)
    diff = "\n".join(
        difflib.unified_diff(
            article.splitlines(),
            patched.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    )
    return patched, diff
