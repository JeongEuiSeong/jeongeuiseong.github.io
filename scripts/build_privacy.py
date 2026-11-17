#!/usr/bin/env python3
"""다람 저장소의 개인정보 처리방침(마크다운)을 이 사이트의 HTML로 만든다.

쓰는 법 (이 폴더에서):
    python3 scripts/build_privacy.py ../daram

원본:
    <daram>/docs/appstore/privacy-policy-ko.md -> daram/privacy/index.html
    <daram>/docs/appstore/privacy-policy-en.md -> daram/privacy/en/index.html

원본 문서에 쓰인 마크다운만 다룬다: 제목(#~###), 구분선(---), 목록(-, 1.), 들여쓴 하위 목록,
표, **굵게**, `코드`, [링크](주소), 줄 끝 공백 두 칸 줄바꿈. 외부 패키지 없이 돈다.
"""
import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent

PAGES = [
    ("docs/appstore/privacy-policy-ko.md", "daram/privacy/index.html", "ko",
     "다람 가계부 — 개인정보 처리방침", '<a href="/daram/">← 다람 가계부</a> · <a href="/daram/privacy/en/">English</a>'),
    ("docs/appstore/privacy-policy-en.md", "daram/privacy/en/index.html", "en",
     "Daram — Privacy Policy", '<a href="/daram/">← Daram</a> · <a href="/daram/privacy/">한국어</a>'),
]


def inline(text: str) -> str:
    """한 줄 안의 꾸밈(코드, 링크, 굵게)을 HTML로 바꾼다."""
    out, pos = [], 0
    # 코드 조각은 먼저 떼어 내서 안의 기호를 꾸밈으로 읽지 않게 한다.
    for m in re.finditer(r"`([^`]+)`", text):
        out.append(_inline_plain(text[pos:m.start()]))
        out.append("<code>" + html.escape(m.group(1)) + "</code>")
        pos = m.end()
    out.append(_inline_plain(text[pos:]))
    return "".join(out)


def _inline_plain(text: str) -> str:
    s = html.escape(text, quote=False)

    def link(m):
        url = html.escape(m.group(2), quote=True)
        ext = ' rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{url}"{ext}>{m.group(1)}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w/:])([\w.+-]+@[\w-]+\.[\w.]+)", r'<a href="mailto:\1">\1</a>', s)
    return s


def list_item(line: str):
    """목록 줄이면 (들여쓰기, 종류, 내용)을, 아니면 None을 준다."""
    m = re.match(r"^( *)(?:([-*])|(\d+)\.) (.*)$", line)
    if not m:
        return None
    return len(m.group(1)), ("ul" if m.group(2) else "ol"), m.group(4)


def render_list(items) -> str:
    """(들여쓰기, 종류, 내용) 목록을 중첩 목록 HTML로 만든다."""
    out, stack = [], []  # stack: (들여쓰기, 종류)
    for indent, kind, content in items:
        if stack and indent > stack[-1][0]:
            out.append(f"<{kind}>")
            stack.append((indent, kind))
        else:
            while stack and indent < stack[-1][0]:
                out.append(f"</li></{stack.pop()[1]}>")
            if stack:
                out.append("</li>")
            else:
                out.append(f"<{kind}>")
                stack.append((indent, kind))
        out.append("<li>" + inline(content))
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "\n".join(out)


def render_table(rows) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]  # cells[1]은 |---| 줄
    out = ['<div class="table-wrap"><table>', "<thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif m := re.match(r"^(#{1,3}) (.*)$", line):
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
        elif re.match(r"^-{3,}\s*$", line):
            out.append("<hr>")
            i += 1
        elif line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows))
        elif list_item(line):
            items = []
            while i < len(lines) and (item := list_item(lines[i])):
                items.append(item)
                i += 1
            out.append(render_list(items))
        else:
            para = []
            while (i < len(lines) and lines[i].strip() and not list_item(lines[i])
                   and not re.match(r"^(#{1,3} |-{3,}\s*$|\s*\|)", lines[i])):
                para.append(lines[i])
                i += 1
            parts = [inline(p.rstrip()) + ("<br>" if p.endswith("  ") else "") for p in para]
            out.append("<p>" + "\n".join(parts) + "</p>")
    return "\n".join(out)


TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="/assets/favicon.png">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<main>
<nav class="top">{nav}</nav>
<!-- 이 파일은 scripts/build_privacy.py로 만든다. 직접 고치지 말고 다람 저장소의 원본을 고친 뒤 다시 만든다. -->
{body}
</main>
<footer>© 2026 Euisung Jung</footer>
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("쓰는 법: python3 scripts/build_privacy.py <다람 저장소 경로>")
    daram = Path(sys.argv[1]).expanduser().resolve()
    for src, dst, lang, title, nav in PAGES:
        body = markdown_to_html((daram / src).read_text(encoding="utf-8"))
        target = SITE / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(TEMPLATE.format(lang=lang, title=title, nav=nav, body=body), encoding="utf-8")
        print(f"{src} -> {dst}")


if __name__ == "__main__":
    main()
