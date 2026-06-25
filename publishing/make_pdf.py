#!/usr/bin/env python3.9
"""
Generate Mudgala Puranam PDF
Front matter → TOC → Chapters
Page size: 5.5 × 8.5 in, Ponnala titles, Gidugu body/shlokas.
"""

import io, os, re, subprocess, sys, urllib.request
from pathlib import Path
from html import escape as esc

BASE         = Path(__file__).resolve().parent.parent
CHAPTERS     = BASE / "chapters"
IMAGES       = BASE / "images"
FRONT_MATTER = BASE / "front-matter"
FONTS_DIR    = BASE / "publishing" / "fonts_cache"
OUTPUT       = str(BASE / "pdfs" / "mudgala-puranam.pdf")

GDRIVE_FOLDER_ID = "14KFkKgeSjzv9JhgJzQ-aEJNe2uX5gJ8X"

FONT_URLS = {
    "Ponnala.ttf":
        "https://fonts.gstatic.com/s/ponnala/v3/w8gaH2QxQOU08bbbrQs.ttf",
    "Gidugu.ttf":
        "https://fonts.gstatic.com/s/gidugu/v28/L0x8DFMkk1Uf6w3RvA.ttf",
}


# ─── Font download ─────────────────────────────────────────────

def download_fonts():
    FONTS_DIR.mkdir(exist_ok=True)
    for fname, url in FONT_URLS.items():
        fp = FONTS_DIR / fname
        if not fp.exists():
            print(f"  Downloading {fname}…")
            urllib.request.urlretrieve(url, fp)
    print("  Fonts ready.")


# ─── Google Drive image sync ────────────────────────────────────

def _ensure_package(pkg):
    import_name = {"google-api-python-client": "googleapiclient"}.get(pkg, pkg)
    try:
        __import__(import_name)
    except ImportError:
        print(f"  Installing {pkg}…", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"])


def sync_images_from_gdrive(force=False):
    """Download all PNG images from the Google Drive folder into images/.
    Requires GOOGLE_API_KEY env var; the Drive folder must be shared as
    'Anyone with the link' (Viewer).
    """
    existing = list(IMAGES.glob("*.png"))
    if existing and not force:
        print(f"  Images cached: {len(existing)} files in {IMAGES}")
        return

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("  WARNING: GOOGLE_API_KEY not set — skipping image download")
        return

    _ensure_package("google-api-python-client")
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    IMAGES.mkdir(exist_ok=True)
    service = build("drive", "v3", developerKey=api_key)

    print(f"  Syncing images from Drive folder {GDRIVE_FOLDER_ID}…", flush=True)
    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=f"'{GDRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="nextPageToken, files(id, name)",
            pageSize=1000,
            pageToken=page_token,
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    pngs = [f for f in files if f["name"].lower().endswith(".png")]
    print(f"  Found {len(pngs)} PNG images", flush=True)
    for f in pngs:
        dest = IMAGES / f["name"]
        req  = service.files().get_media(fileId=f["id"])
        buf  = io.FileIO(dest, mode="wb")
        dl   = MediaIoBaseDownload(buf, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        print(f"    {f['name']}", flush=True)
    print(f"  Downloaded {len(pngs)} images.")


# ─── Inline markdown → HTML ────────────────────────────────────

def inline(text):
    text = re.sub(r'\\([=\-!.,:()\[\]/])', r'\1', text)
    parts = re.split(r'(\*\*[^*\n]+\*\*)', text)
    out = []
    for p in parts:
        if p.startswith('**') and p.endswith('**') and len(p) > 4:
            out.append(f'<strong>{esc(p[2:-2])}</strong>')
        else:
            out.append(esc(p))
    return ''.join(out)


# ─── Chapter parser ────────────────────────────────────────────

def is_shloka_line(s):
    inner = s[2:-2] if s.startswith('**') and s.endswith('**') else ''
    return bool(re.search(r'[॥|]\s*\d+\s*[॥|]', inner))

def parse_chapter(path):
    text  = path.read_text(encoding='utf-8')
    lines = text.split('\n')

    m   = re.search(r'ch-(\d+)', path.stem)
    num = int(m.group(1)) if m else 0

    title = ''
    for line in lines:
        s = line.strip()
        if s.startswith('## '):
            title = s[3:].strip(); break
        if s.startswith('**') and s.endswith('**') and 'అధ్యాయము' in s:
            title = s[2:-2].strip(); break

    avatarika_lines = []
    sections        = []
    cur_sec_heading = None
    cur_sec_blocks  = []
    state = 'before_ava'

    def flush_section():
        if cur_sec_heading is not None or cur_sec_blocks:
            sections.append({
                'heading':      cur_sec_heading or '',
                'heading_html': inline(cur_sec_heading) if cur_sec_heading else '',
                'blocks':       list(cur_sec_blocks),
            })

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('## ') or (s.startswith('**') and s.endswith('**')
                                    and 'అధ్యాయము' in s and len(s) < 200):
            state = 'before_ava'
            continue
        if s in ('అవతారిక', '**అవతారిక**'):
            state = 'ava'
            continue
        if s.startswith('### '):
            flush_section()
            cur_sec_heading = s[4:].strip()
            cur_sec_blocks  = []
            state = 'sections'
            continue
        if (s.startswith('**') and s.endswith('**') and
                re.search(r'[：:]$', s[2:-2]) and
                not is_shloka_line(s) and len(s) < 150):
            flush_section()
            cur_sec_heading = s[2:-2].rstrip(':：').strip()
            cur_sec_blocks  = []
            state = 'sections'
            continue
        if state in ('before_ava', 'ava'):
            avatarika_lines.append(s)
            state = 'ava'
            continue
        if s.startswith('**') and s.endswith('**') and is_shloka_line(s):
            cur_sec_blocks.append(('shloka', s[2:-2]))
        elif s == '**సారాంశము:**' or s.startswith('**సారాంశము:'):
            cur_sec_blocks.append(('summary_label', 'సారాంశము'))
        elif s.startswith('**') and s.endswith('**') and not is_shloka_line(s):
            cur_sec_blocks.append(('bold_label', inline(s)))
        else:
            cur_sec_blocks.append(('body', inline(s)))

    flush_section()

    ava_html = '\n'.join(
        f'<p class="ava-text">{inline(l)}</p>' for l in avatarika_lines if l
    )
    return {'num': num, 'title': title, 'avatarika_html': ava_html, 'sections': sections}


def chapter_label(num, title):
    m = re.search(r'\((\d+)వ అధ్యాయము\)', title)
    n = m.group(1) if m else str(num)
    return f"{n}వ అధ్యాయము"


# ─── Front matter HTML ─────────────────────────────────────────

def build_front_matter_html():
    imgs = sorted(FRONT_MATTER.glob('*'))
    imgs = [p for p in imgs if p.suffix.lower() in ('.png', '.jpg', '.jpeg')]
    parts = []
    for img in imgs:
        # Infographic gets a centered fitted page; scanned pages fill the page
        if img.name.startswith('0_'):
            parts.append(
                f'<div class="fm-info-pg">'
                f'<img src="{img}" alt="Infographic">'
                f'</div>'
            )
        else:
            parts.append(
                f'<div class="fm-scan-pg">'
                f'<img src="{img}" alt="{esc(img.stem)}">'
                f'</div>'
            )
    print(f"  Front matter: {len(imgs)} images")
    return ''.join(parts)


# ─── TOC HTML ──────────────────────────────────────────────────

def build_toc_html(chapters):
    lines = [
        '<div class="toc-section">',
        '<h1 class="toc-title">విషయానుక్రమణిక</h1>',
    ]
    for ch in chapters:
        anchor = f"ch-{ch['num']}-anchor"
        lbl    = chapter_label(ch['num'], ch['title'])
        # Short title: adhyaya label + topic name (after ' - ')
        m = re.search(r'-\s*(.+)$', ch['title'])
        topic = m.group(1).strip() if m else ch['title']
        display = f"{lbl}  –  {topic}"
        lines.append(
            f'<div class="toc-entry">'
            f'<a class="toc-link" href="#{anchor}">{esc(display)}</a>'
            f'<span class="toc-dots"></span>'
            f'<span class="toc-pgnum"><a href="#{anchor}"></a></span>'
            f'</div>'
        )
    lines.append('</div>')
    return '\n'.join(lines)


# ─── Chapter HTML ──────────────────────────────────────────────

def build_chapter_html(ch, page_class, img_path):
    parts = []
    label = chapter_label(ch['num'], ch['title'])
    anchor = f"ch-{ch['num']}-anchor"

    if img_path and img_path.exists():
        parts.append(
            f'<div class="img-pg">'
            f'<img src="{img_path}" alt="{esc(label)}">'
            f'</div>'
        )

    parts.append(f'<div id="{anchor}" class="{page_class}">')

    parts.append(
        f'<div class="ch-title-block">'
        f'<h1 class="ch-title">{esc(ch["title"])}</h1>'
        f'</div>'
    )

    if ch['avatarika_html']:
        parts.append(
            f'<div class="avatarika">'
            f'<p class="ava-label">అవతారిక</p>'
            f'{ch["avatarika_html"]}'
            f'</div>'
        )

    for sec in ch['sections']:
        parts.append('<div class="section">')
        if sec['heading']:
            parts.append(f'<h3 class="sec-heading">{sec["heading_html"]}</h3>')
        in_shloka_block = False
        for btype, bhtml in sec['blocks']:
            if btype == 'shloka':
                if not in_shloka_block:
                    parts.append('<div class="shloka-block">')
                    in_shloka_block = True
                parts.append(f'<div class="shloka">{esc(bhtml)}</div>')
            else:
                if in_shloka_block:
                    parts.append('</div><div class="shloka-spacer"></div>')
                    in_shloka_block = False
                if btype == 'summary_label':
                    parts.append('<div class="summary-label">సారాంశము</div>')
                elif btype == 'bold_label':
                    parts.append(f'<div class="bold-label">{bhtml}</div>')
                else:
                    parts.append(f'<p class="body-text">{bhtml}</p>')
        if in_shloka_block:
            parts.append('</div><div class="shloka-spacer"></div>')
        parts.append('</div>')

    parts.append('</div>')
    return '\n'.join(parts)


# ─── CSS ───────────────────────────────────────────────────────

FOOTER_STYLE = """
    font-family:'Gidugu',sans-serif; font-size:8pt; color:#444;
    border-top:0.6pt solid #555; padding-top:4pt; margin-top:12pt;
    vertical-align:top;
"""
NO_FOOTER = "content:none; border:none;"

def page_rules(page_name, footer_label):
    return f"""
@page {page_name}:left {{
    margin:0.75in 0.65in 1.0in 0.9in;
    @bottom-left   {{ content:counter(page); {FOOTER_STYLE} }}
    @bottom-center {{ content:""; border-top:0.6pt solid #555; margin-top:12pt; padding-top:4pt; }}
    @bottom-right  {{ content:"{footer_label}"; {FOOTER_STYLE} text-align:right; }}
}}
@page {page_name}:right {{
    margin:0.75in 0.9in 1.0in 0.65in;
    @bottom-left   {{ content:"{footer_label}"; {FOOTER_STYLE} }}
    @bottom-center {{ content:""; border-top:0.6pt solid #555; margin-top:12pt; padding-top:4pt; }}
    @bottom-right  {{ content:counter(page); {FOOTER_STYLE} text-align:right; }}
}}"""


def build_css(chapters):
    fa = FONTS_DIR.resolve()

    named_pages = (
        # Front matter: no footer, tight margins
        f"""
@page fm-info-pg {{
    size:5.5in 8.5in; margin:0.5in;
    @bottom-left {{ {NO_FOOTER} }} @bottom-center {{ {NO_FOOTER} }} @bottom-right {{ {NO_FOOTER} }}
}}
@page fm-scan-pg {{
    size:5.5in 8.5in; margin:0.2in;
    @bottom-left {{ {NO_FOOTER} }} @bottom-center {{ {NO_FOOTER} }} @bottom-right {{ {NO_FOOTER} }}
}}
@page toc-pg {{
    size:5.5in 8.5in; margin:0.75in 0.9in 1.0in 0.9in;
    @bottom-left   {{ content:"విషయానుక్రమణిక"; {FOOTER_STYLE} }}
    @bottom-center {{ content:""; border-top:0.6pt solid #555; margin-top:12pt; padding-top:4pt; }}
    @bottom-right  {{ content:counter(page); {FOOTER_STYLE} text-align:right; }}
}}"""
    )
    for ch in chapters:
        lbl = chapter_label(ch['num'], ch['title'])
        named_pages += page_rules(f'ch{ch["num"]}-pg', lbl)

    page_classes = '\n'.join(
        f'.ch{ch["num"]}-section {{ page:ch{ch["num"]}-pg; page-break-before:always; }}'
        for ch in chapters
    )

    return f"""
@font-face {{
    font-family:'Ponnala';
    src:url('{fa}/Ponnala.ttf') format('truetype');
    font-weight:normal; font-style:normal;
}}
@font-face {{
    font-family:'Gidugu';
    src:url('{fa}/Gidugu.ttf') format('truetype');
    font-weight:normal; font-style:normal;
}}

@page {{ size:5.5in 8.5in; }}
{named_pages}

@page img-pg {{
    size:5.5in 8.5in; margin:0.6in;
    @bottom-left {{ {NO_FOOTER} }} @bottom-center {{ {NO_FOOTER} }} @bottom-right {{ {NO_FOOTER} }}
}}

* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ font-size:9pt; }}
body {{ font-family:'Gidugu',sans-serif; font-size:9pt; line-height:1.45; color:#111; }}

{page_classes}

/* ── Front matter ── */
.fm-info-pg {{
    page:fm-info-pg; page-break-before:always; page-break-after:always;
    display:flex; align-items:center; justify-content:center; height:100%;
}}
.fm-info-pg img {{
    max-width:4.3in; max-height:7.3in; display:block;
}}
.fm-scan-pg {{
    page:fm-scan-pg; page-break-before:always; page-break-after:always;
    display:flex; align-items:center; justify-content:center; height:100%;
}}
.fm-scan-pg img {{
    max-width:5.0in; max-height:8.0in; display:block;
}}

/* ── TOC ── */
.toc-section {{
    page:toc-pg; page-break-before:always;
}}
.toc-title {{
    font-family:'Ponnala',sans-serif; font-size:20pt;
    text-align:center; margin-bottom:0.4in;
    page-break-after:avoid;
}}
.toc-entry {{
    display:flex; align-items:baseline;
    margin:0.055in 0; font-size:9pt; line-height:1.4;
}}
.toc-link {{ text-decoration:none; color:#111; flex:0 0 auto; }}
.toc-dots {{
    flex:1; border-bottom:0.5pt dotted #888;
    margin:0 0.08in; align-self:flex-end; height:0.55em;
}}
.toc-pgnum {{ flex:0 0 auto; font-size:9pt; }}
.toc-pgnum a {{ text-decoration:none; color:#111; }}
.toc-pgnum a::after {{ content:target-counter(attr(href),page); }}

/* ── Chapter image page ── */
.img-pg {{
    page:img-pg; page-break-before:always; page-break-after:always;
    display:flex; align-items:center; justify-content:center; height:100%;
}}
.img-pg img {{
    max-width:4.0in; max-height:6.0in; display:block;
    border:2.5pt solid #555; padding:8pt;
}}

/* ── Chapter title ── */
.ch-title-block {{ text-align:center; margin-bottom:0.35in; padding-top:0.15in; }}
.ch-title {{
    font-family:'Ponnala',sans-serif; font-size:16pt;
    line-height:1.35; color:#111; page-break-after:avoid;
}}

/* ── Avatarika ── */
.avatarika {{ margin-bottom:0.25in; }}
.ava-label {{
    font-family:'Ponnala',sans-serif; font-size:11pt;
    color:#333; margin-bottom:0.08in; page-break-after:avoid;
}}
.ava-text {{ font-size:9pt; line-height:1.48; text-align:justify; margin:0.04in 0; }}

/* ── Sections ── */
.section {{ margin-bottom:0.1in; }}
.sec-heading {{
    font-family:'Ponnala',sans-serif; font-size:11pt;
    color:#222; margin:0.2in 0 0.08in 0; page-break-after:avoid;
}}

/* ── Shlokas ── */
.shloka-block {{ margin:0.05in 0 0 0.2in; page-break-inside:avoid; }}
.shloka {{
    font-family:'Gidugu',sans-serif; font-weight:bold; font-size:11pt;
    line-height:1.55; color:#000;
}}
.shloka-spacer {{ height:1.45em; }}

/* ── Labels ── */
.summary-label {{
    font-family:'Gidugu',sans-serif; font-weight:bold; font-size:9pt;
    color:#222; margin:0.1in 0 0.04in 0;
}}
.bold-label {{
    font-family:'Gidugu',sans-serif; font-weight:bold; font-size:9.5pt;
    color:#222; margin:0.15in 0 0.06in 0; page-break-after:avoid;
}}

/* ── Body text ── */
.body-text {{ font-size:9pt; line-height:1.48; margin:0.02in 0; text-align:justify; }}
"""


# ─── Main ──────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-download", action="store_true",
                        help="Skip Google Drive image sync (use cached images)")
    parser.add_argument("--force-download", action="store_true",
                        help="Re-download images even if already cached")
    args = parser.parse_args()

    print("Downloading fonts…")
    download_fonts()

    if not args.no_download:
        print("Syncing images from Google Drive…")
        sync_images_from_gdrive(force=args.force_download)

    ch_files = sorted(
        CHAPTERS.glob('ch-*.md'),
        key=lambda p: int(re.search(r'(\d+)', p.stem).group(1))
    )
    print(f"Found {len(ch_files)} chapter files.")

    chapters = []
    for cf in ch_files:
        ch = parse_chapter(cf)
        chapters.append(ch)
        print(f"  ch-{ch['num']:02d}  {ch['title'][:60]}")

    css = build_css(chapters)

    print("Building front matter…")
    fm_html = build_front_matter_html()

    print("Building TOC…")
    toc_html = build_toc_html(chapters)

    print("Building chapters…")
    ch_parts = []
    for ch in chapters:
        img_path   = IMAGES / f"ch-{ch['num']}.png"
        page_class = f"ch{ch['num']}-section"
        ch_parts.append(build_chapter_html(ch, page_class, img_path))

    html = f"""<!DOCTYPE html>
<html lang="te">
<head><meta charset="UTF-8">
<style>{css}</style>
</head>
<body>
{fm_html}
{toc_html}
{''.join(ch_parts)}
</body>
</html>"""

    preview_path = BASE / "publishing" / "preview.html"
    preview_path.write_text(html, encoding='utf-8')
    print(f"  HTML preview → {preview_path}")

    print("Generating PDF…")
    from weasyprint import HTML as WP
    (BASE / "pdfs").mkdir(exist_ok=True)
    WP(string=html, base_url=str(BASE)).write_pdf(OUTPUT)
    size_mb = Path(OUTPUT).stat().st_size / 1024 / 1024
    print(f"  Done → {OUTPUT}  ({size_mb:.1f} MB)")


if __name__ == '__main__':
    main()
