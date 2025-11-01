#!/usr/bin/env python3
# populate_art.py
#
# Scans images/portfolio/<YEAR>/ for files and injects simple HTML sections
# right after the first <main> tag in art.html.
#
# Output format per year (only if that year has files):
#
#   <h2>2015</h2>
#   <ul style="list-style-type: none; padding: 0;">
#     <li><a href="images/portfolio/2015/filename.jpg">filename.jpg</a></li>
#     ...
#   </ul>
#
# Notes:
# - Only folder names that are all digits (e.g., "2014", "2020") are treated as years.
# - Only common image extensions are included. Extend FILE_EXTS if needed.
# - The script creates a backup art.html.bak before writing.
# - Re-running replaces the auto-generated block between the BEGIN/END markers.

from pathlib import Path
from urllib.parse import quote
import html
import re
import sys

ART_HTML = Path("art.html")
PORTFOLIO_DIR = Path("images/portfolio")

FILE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".pdf"}

BEGIN_MARK = "<!-- BEGIN AUTO-GENERATED ART -->"
END_MARK = "<!-- END AUTO-GENERATED ART -->"

def find_year_dirs(base: Path):
    if not base.exists():
        return []
    years = []
    for p in base.iterdir():
        if p.is_dir() and p.name.isdigit():
            years.append(p)
    # sort ascending like the example (2014, 2015, ...). Change to reverse=True for newest first.
    years.sort(key=lambda d: int(d.name))
    return years

def list_year_files(year_dir: Path):
    files = []
    for p in sorted(year_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in FILE_EXTS and not p.name.startswith("."):
            files.append(p.name)
    return files

def build_year_block(year: str, filenames: list[str]) -> str:
    # Builds exactly the requested structure (no <section> wrapper).
    lines = []
    lines.append(f'\t\t\t\t<h2>{year}</h2>')
    lines.append('\t\t\t\t<ul style="list-style-type: none; padding: 0;">')
    for name in filenames:
        # URL path should include the year folder; display uses raw filename.
        href_path = f"images/portfolio/{year}/{quote(name)}"
        display_name = html.escape(name)
        lines.append(f'\t\t\t\t\t<li><a href="{href_path}">{display_name}</a></li>')
    lines.append('\t\t\t\t</ul>')
    return "\n".join(lines)

def generate_all_blocks() -> str:
    blocks = []
    for yd in find_year_dirs(PORTFOLIO_DIR):
        files = list_year_files(yd)
        if not files:
            continue
        blocks.append(build_year_block(yd.name, files))
    return ("\n\n".join(blocks) + "\n") if blocks else ""

def inject_after_main(html_text: str, payload: str) -> str:
    """
    Insert payload right after the first <main> ... > tag.
    If markers exist, replace the content between them instead.
    """
    if not payload:
        return html_text  # nothing to insert

    # Replace existing generated block if present
    if BEGIN_MARK in html_text and END_MARK in html_text:
        pattern = re.compile(
            rf"{re.escape(BEGIN_MARK)}.*?{re.escape(END_MARK)}",
            flags=re.DOTALL
        )
        replacement = f"{BEGIN_MARK}\n{payload}{END_MARK}"
        return pattern.sub(replacement, html_text, count=1)

    # Otherwise inject after the first <main ...>
    main_open = re.search(r"<main\b[^>]*>", html_text, flags=re.IGNORECASE)
    if not main_open:
        raise RuntimeError("Could not find a <main> tag in art.html")
    insert_at = main_open.end()
    before = html_text[:insert_at]
    after = html_text[insert_at:]
    injection = f"\n{BEGIN_MARK}\n{payload}{END_MARK}\n"
    return before + injection + after

def main():
    if not ART_HTML.exists():
        print(f"Error: {ART_HTML} not found", file=sys.stderr)
        sys.exit(1)

    payload = generate_all_blocks()
    # Read, inject, write (with backup)
    original = ART_HTML.read_text(encoding="utf-8")

    try:
        updated = inject_after_main(original, payload)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    ART_HTML.write_text(updated, encoding="utf-8")
    print(f"Updated {ART_HTML} ({'with' if payload else 'no'} content).")

if __name__ == "__main__":
    main()

