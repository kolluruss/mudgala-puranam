# ముద్గల పురాణము (Mudgala Puranam)

A Telugu translation of the Sanskrit **ముద్గల పురాణము**, an Upapurana devoted to Lord Ganesha — specifically his form as **ఏకదంత** (Ekadanta). The source text narrates the birth and exploits of Ganesha across two major sections: a cosmological prologue and the complete **ఏకదంత చరిత్ర** (Ekadanta Charitra).

**Translator:** Kolluru Seetarama Sarma

Content is authored in Markdown, illustrated with AI-generated images, and typeset into a PDF using a custom Python/WeasyPrint pipeline.

**[Download latest PDF](https://github.com/kolluruss/mudgala-puranam/releases/latest/download/mudgala-puranam.pdf)**

---

## Table of Contents

- [About the Work](#about-the-work)
- [Book Organization](#book-organization)
- [Repository Structure](#repository-structure)
- [Content File Format](#content-file-format)
- [Chapter Overview](#chapter-overview)
- [About the Translator](#about-the-translator)
- [Project Architecture](#project-architecture)
- [For Developers — Local Setup](#for-developers--local-setup)
- [For Content Editors — Updating Content via GitHub](#for-content-editors--updating-content-via-github)

---

## About the Work

*Mudgala Puranam* is a Sanskrit Upapurana dedicated to Lord Ganesha, focusing on his manifestation as **Ekadanta** (the single-tusked one). The Telugu translation here covers **74 adhyayas** organized into two parts:

- **Prathama Khanda (ప్రథమ ఖండము)** — Chapters 1–30: Cosmological prologue narrating Brahma's creation, early Puranic lineages, cosmography (continents, solar system, nether worlds), and stories of key sages and kings, all framed as a dialogue between Mudgala Muni and Daksha Prajapati.

- **Dvitiya Khanda — Ekadanta Charitra (ద్వితీయ ఖండము — ఏకదంత చరిత్ర)** — Chapters 31–74: The complete Ekadanta narrative — the birth of Gajasura, his conquest of the gods, Ekadanta's intervention and victory, the stories of devoted sages (Bhrishundi, Cyavana), and the concluding description of Ekadanta's sacred kshetra and the phala shruti (rewards of recitation).

The work is framed as Suta Muni's recitation to the assembled sages at Naimisharanya, who in turn relay the dialogue between Mudgala Muni and Daksha Prajapati.

---

## Book Organization

| Level | Term | Description |
|---|---|---|
| Chapter | Adhyaya (అధ్యాయము) | 74 chapters, each narrating a major episode |
| Section | Heading (విభాగం) | Logical grouping of related verses within an adhyaya |
| Unit | Shloka (శ్లోకము) | Individual Sanskrit verse with Telugu commentary |

Each chapter opens with an **అవతారిక** (avatarika) — a prose summary of the episode — followed by the Sanskrit shlokas and their Telugu commentary.

---

## Repository Structure

```
mudgala-puranam/
├── chapters/                      # Telugu translation (one file per adhyaya)
│   ├── ch-1.md                    # ప్రథమోధ్యాయః - బ్రహ్మ సృష్టి
│   ├── ch-2.md                    # ద్వితీయోధ్యాయః - నారద శాప నివర్తనమ్
│   ├── …
│   └── ch-74.md                   # చతుఃసప్తతితమోऽధ్యాయః - ఏకదంత చరిత మాహాత్మ్యము
│
├── front-matter/                  # Front matter pages (scanned originals + infographic)
│   ├── 0_Mudgala_Purana_Ekadanta_Infographic.png
│   └── IMG_*.jpg                  # Scanned source pages (printed in reading order)
│
├── image_prompts/                 # AI image generation prompts (one .txt per chapter)
├── images/                        # Chapter illustrations (ch-N.png, one per adhyaya)
├── pdfs/                          # Generated PDF output
│   └── mudgala-puranam.pdf
│
├── publishing/
│   ├── make_pdf.py                # Builds the full PDF (front matter → TOC → chapters)
│   ├── book_prompt.md             # Typesetting specification and layout rules
│   ├── preview.html               # Last generated HTML preview
│   ├── requirements.txt           # Python dependencies
│   └── fonts_cache/               # Telugu fonts (Ponnala, Gidugu) cached locally
│
├── raw/                           # Raw transcription files (ch-N-NN.md, pre-editing)
├── raw-images/                    # Original scanned images (batch 1)
├── raw_images_2/                  # Original scanned images (batch 2)
├── done/                          # Processed scans (archived after transcription)
├── prompts/                       # Miscellaneous generation prompts
│
├── .github/
│   └── workflows/
│       └── generate-pdf.yml       # CI pipeline (auto-builds PDF on push)
└── .gitignore
```

**Total:** 74 adhyayas · 2 khanda · organized into sections within each adhyaya

---

## Content File Format

Each chapter file (`chapters/ch-N.md`) follows this structure:

### Chapter heading

```markdown
## <Sanskrit ordinal>ధ్యాయః (<N>వ అధ్యాయము) - <Telugu episode title>
```

### Avatarika (అవతారిక)

A paragraph of Telugu prose summarizing the entire episode. Printed on the chapter title page before the first shloka.

### Sections and shlokas

```markdown
### <Section heading in Telugu>

**<Sanskrit shloka line 1>**
**<Sanskrit shloka line 2>॥ N ॥**

Telugu commentary prose explaining the meaning and significance of the shloka(s).

**సారాంశము:**
Optional summary paragraph for longer sections.
```

| Element | Format | Content |
|---|---|---|
| Section heading | `### …` | Telugu description of the episode sub-section |
| Shloka | `**…॥N॥**` bold line | Sanskrit verse with verse number |
| Commentary | Plain paragraph | Telugu prose translation and explanation |
| Summary | `**సారాంశము:**` | Optional closing summary for complex sections |

> **Note:** Unlike *Ganapati Sambhavam*, the Mudgala Puranam format does not include పదచ్ఛేదము, అన్వయము, or ప్రతిపదార్థము sections. Each shloka is followed directly by Telugu commentary.

---

## Chapter Overview

### Prathama Khanda (ప్రథమ ఖండము) — Chapters 1–30

| Chapter | Telugu Title | Episode |
|---|---|---|
| 1 | బ్రహ్మ సృష్టి | Brahma's vision of Ganesha in the primordial waters; creation begins |
| 2 | నారద శాప నివర్తనమ్ | Narada's curse and its resolution |
| 3 | నారద భక్తి వర్ణనమ్ | Narada's devotion to Ekadanta |
| 4 | మధు కైటభ వధ | Slaying of Madhu and Kaitabha |
| 5 | స్వాయంభువ మనువుకు వరప్రదానము | Boon granted to Svayambhuva Manu |
| 6 | దక్ష కన్యా వంశ వర్ణనము | Lineage of Daksha's daughters |
| 7 | భోగ మోక్ష వర్ణనము | Description of worldly enjoyment and liberation |
| 8 | దత్త చరిత్ర | Story of Dattatreya |
| 9 | ప్రియవ్రత రాజ్యప్రాప్తి వర్ణనము | Priyavrata's kingdom |
| 10 | ద్వీప వర్ణనము | Description of the seven continents |
| 11 | భూగోళ వర్ణనము | Cosmography of the earth |
| 12 | సూర్యమండల వర్ణనము | Description of the solar sphere |
| 13 | నవగ్రహ రథ వర్ణనము | The chariots of the nine planets |
| 14 | ఊర్ధ్వ లోకముల వర్ణనము | Description of the upper worlds |
| 15 | సప్త పాతాల వర్ణనము | Description of the seven nether worlds |
| 16 | ఋషభదేవ చరిత్ర వర్ణనము | Story of Rishabhadeva |
| 17 | పులహునకు ఉపదేశము మరియు భరతుని చరిత్ర | Instruction to Pulaha; story of Bharata |
| 18 | *(అధ్యాయము 18 — pending)* | — |
| 19 | జడభరతుని జననము మరియు చోరుల వధ | Birth of Jadabharata; slaying of robbers |
| 20 | జడభరత మరియు రఘూగణ మహారాజుల కలయిక | Meeting of Jadabharata and King Rahugana |
| 21 | రఘూగణునకు సిద్ధి ప్రాప్తి వర్ణనము | Rahugana's attainment of liberation |
| 22 | జడభరతుని ముక్తి | Jadabharata's final liberation |
| 23 | *(అధ్యాయము 23 — see ch-23.md)* | — |
| 24 | పృథు మహారాజు యశోవర్ణనము | Glory of King Prithu |
| 25 | సనకాదుల ఉపదేశము మరియు శివగీత | Sanakadi's teaching and the Shiva Gita |
| 26 | *(అధ్యాయము 26 — pending)* | — |
| 27 | ప్రచేతసుల చరిత్ర మరియు ముక్తి | Story and liberation of the Prachetasas |
| 28 | కశ్యప సృష్టి వర్ణనము | Kashyapa's creation |
| 29 | వశిష్ఠ తపోవర్ణనము మరియు రావణాదుల వృత్తాంతము | Vasishtha's penance; Ravana's story |
| 30 | పరాశరునకు వరప్రదానము | Boon granted to Parashara |

### Dvitiya Khanda — Ekadanta Charitra (ద్వితీయ ఖండము) — Chapters 31–74

| Chapter | Telugu Title | Episode |
|---|---|---|
| 31 | గజాసురుని జననము మరియు దేవతల తపస్సు | Birth of Gajasura; gods perform penance |
| 32 | గజాసురుని సేనా వధ | Slaughter of Gajasura's army |
| 33 | గజాసుర వధాఖ్యానము | Slaying of Gajasura |
| 34 | వ్యాస మహాత్మ్యము | Glory of Vyasa |
| 35 | శుక మహర్షి ఉపాఖ్యానము | Story of Shuka Muni |
| 36 | గౌతమ చరితము | Story of Gautama |
| 37 | నృసింహ మహాత్మ్యము | Glory of Narasimha |
| 38 | వారాహ మాహాత్మ్యము | Glory of Varaha |
| 39 | చ్యవనోత్పత్తి కథ | Birth of Cyavana |
| 40 | అగ్ని మాహాత్మ్యము | Glory of Agni |
| 41 | చ్యవన మహర్షి తపోవర్ణనము | Cyavana's penance |
| 42 | భృగు మహర్షి చరిత్ర | Story of Bhrigu Muni |
| 43 | చ్యవన మాహాత్మ్యము | Glory of Cyavana |
| 44 | మదాసుర రాజ్యాభిషేకము | Coronation of Madasura |
| 45 | మదాసుర స్వర్గవిజయము | Madasura's conquest of heaven |
| 46 | తారకాసురుని దౌత్యము మరియు జగదంబ ధర్మబోధ | Tarakasura's embassy; Jagadamba's teaching |
| 47 | ఇంద్ర తారక యుద్ధ ప్రారంభము | Battle between Indra and Taraka begins |
| 48 | ఇంద్రుని పరాజయము | Indra's defeat |
| 49 | శివాదుల పరాజయము | Defeat of Shiva and the gods |
| 50 | మదాసుర విజయము | Madasura's victory |
| 51 | సనత్కుమార దేవ సమాగమము | Sanatkumara meets the gods |
| 52 | ఏకదంత ప్రసన్నము | Ekadanta becomes gracious |
| 53 | మదాసుర పరాజయము | Defeat of Madasura |
| 54 | మదాసుర శాంతి ప్రాప్తి | Madasura attains peace |
| 55 | మదాసుర చరిత్ర ముగింపు | Conclusion of Madasura's story |
| 56 | వినాయకుని కాశీ ప్రవేశము | Vinayaka enters Kashi |
| 57 | భృశుండి భక్తి వర్ణన | Bhrishundi's devotion |
| 58 | యమ శాప వర్ణనము | Yama's curse |
| 59 | కుండ సంభవ చరిత్ర | Story of Kundasambhava |
| 60 | భృశుండి చాండాలుడు బ్రాహ్మణుడగుట | Bhrishundi's transformation from Chandala to Brahmin |
| 61 | భృశుండి చరిత్ర (మానసిక పూజా వర్ణన) | Bhrishundi's mental worship of Ganesha |
| 62 | వినాయక చరితము (రాక్షస వధ) | Vinayaka slays demons |
| 63 | శని సమాగమము | Saturn's encounter with Ganesha |
| 64 | విష్ణు దౌత్య వర్ణనము | Vishnu's embassy |
| 65 | అగస్త్యుని ద్రవ్య ప్రయత్నము | Agastya's quest for resources |
| 66 | ఇల్వల భక్షణ, రాధా-కృష్ణుల శాప వృత్తాంతము | Agastya consumes Ilvala; Radha-Krishna's curse |
| 67 | రాధా కృష్ణుల గోలోక ప్రాప్తి వర్ణన | Radha and Krishna reach Goloka |
| 68 | పుష్టీపతి చరితము (అగస్త్యుని సముద్ర పానము) | Agastya drinks the ocean |
| 69 | దేవహూతి మరియు కర్దములకు శాంతి ప్రాప్తి | Devahuti and Kardama attain peace |
| 70 | చింతామణి హరణము | Theft of the Chintamani gem |
| 71 | కపిలునకు వరప్రదానము (గణాసుర జననము) | Boon to Kapila; birth of Ganasura |
| 72 | గణాసుర వధ | Slaying of Ganasura |
| 73 | గృత్సమద ప్రహ్లాద సంవాదము (ఏకదంత యోగోపదేశము) | Gritsamada and Prahlada; Ekadanta's yoga teaching |
| 74 | ఏకదంత చరిత మాహాత్మ్యము (క్షేత్ర వర్ణన - ఫలశ్రుతి) | Ekadanta's sacred kshetra; phala shruti (conclusion) |

---

## About the Translator

**Kolluru Seetarama Sarma** undertook this translation to bring the rare *Mudgala Puranam* — a text largely inaccessible to Telugu readers — into print, inspired by deep devotion to Ganesha in his Ekadanta form. The translation preserves the shloka-by-shloka structure of the original Sanskrit while making the meaning fully accessible through Telugu prose commentary.

---

## Project Architecture

```
Markdown files (chapters/ch-N.md)
        │
        │  edit on GitHub or locally
        ▼
GitHub Actions (on push to main)
        │
        ├── Runs publishing/make_pdf.py
        │       │
        │       ├── Reads front-matter/ images (infographic + scans)
        │       ├── Builds a TOC (విషయానుక్రమణిక)
        │       ├── Parses all chapter markdown files in adhyaya order
        │       ├── Builds styled HTML (Telugu fonts, chapter footers)
        │       └── Renders to PDF via WeasyPrint (5.5 × 8.5 in)
        │
        └── Publishes PDF → GitHub Release (vMAJOR.MINOR.PATCH)
                   └── Every push creates a new versioned release
```

**Key design decisions:**
- Content lives in plain Markdown — no special software needed to edit
- One file per chapter (`ch-N.md`) — easy to locate and update any episode
- Front matter is image-based (scanned originals) — rendered before the TOC
- Images are optional per chapter — if `images/ch-N.png` exists it gets a dedicated page
- PDF generation is fully automated — editors never touch the publishing scripts
- Every push creates a new versioned GitHub Release — full history is preserved

### Versioning

| Part | Source | When to change |
|---|---|---|
| MAJOR | `publishing/VERSION` file | Major restructuring, format overhaul |
| MINOR | `publishing/VERSION` file | New content sections, significant additions |
| PATCH | Auto-computed (total git commit count) | Every push — automatic |

---

## For Developers — Local Setup

### Prerequisites

- Python 3.9+
- `pip install -r publishing/requirements.txt`
- WeasyPrint system libraries

**macOS:**
```bash
brew install pango cairo libffi
```

**Ubuntu / Debian:**
```bash
sudo apt-get install -y \
  libpango-1.0-0 libpangoft2-1.0-0 \
  libcairo2 libgobject-2.0-0 \
  libharfbuzz0b libfribidi0
```

### Running locally

```bash
# Generate the full book PDF
python3.9 publishing/make_pdf.py
```

The script downloads Telugu fonts (Ponnala, Gidugu) into `publishing/fonts_cache/` on first run, generates an HTML preview at `publishing/preview.html`, then renders the final PDF to `pdfs/mudgala-puranam.pdf`.

### Inspecting the output without regenerating the PDF

```bash
# Open the last generated HTML preview in a browser
open publishing/preview.html
```

---

## For Content Editors — Updating Content via GitHub

You do **not** need to install anything. All editing happens on GitHub's website. The PDF regenerates automatically within a few minutes of saving.

**PDF download link (always the latest):**
```
https://github.com/kolluruss/mudgala-puranam/releases/latest/download/mudgala-puranam.pdf
```

### Editing an existing chapter

1. Go to [github.com/kolluruss/mudgala-puranam](https://github.com/kolluruss/mudgala-puranam)
2. Navigate to `chapters/` → open the chapter file (e.g. `ch-1.md`)
3. Click the **pencil icon** to open the editor
4. Edit the content — keep the `## ` heading, `అవతారిక`, and `### ` section structure intact
5. Scroll down → write a brief commit message → click **"Commit changes"**
6. Click the **Actions** tab to watch the pipeline — green checkmark means the PDF is updated

### Adding a new chapter

1. In the `chapters/` folder, click **"Add file" → "Create new file"**
2. Name it `ch-N.md` (e.g. `ch-18.md`)
3. Follow the chapter format (heading → అవతారిక → sections with shlokas and commentary)
4. Commit — the pipeline includes it automatically in the next build

### Adding a chapter image

Images are optional. If a file `images/ch-N.png` exists, the PDF pipeline automatically inserts a dedicated image page before that chapter's content.

1. Generate or prepare an image for the chapter
2. Name it `ch-N.png` (e.g. `ch-18.png`)
3. Upload to the `images/` folder via GitHub's **"Add file" → "Upload files"**
4. Commit — the next PDF build will include the image
