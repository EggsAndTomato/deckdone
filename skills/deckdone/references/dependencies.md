# Dependencies

## Required

| Dependency | Type | Purpose |
|-----------|------|---------|
| pptx skill | Skill | Core PPTX generation (`html2pptx`, `thumbnail`) |
| pptxgenjs | npm global | PowerPoint generation library |
| playwright | npm global | HTML rendering for `html2pptx` |
| sharp | npm global | SVG→PNG icon/gradient rasterization |

## Optional (graceful degradation)

| Dependency | Type | Degradation if missing |
|-----------|------|----------------------|
| pdf skill | Skill | Ask user to paste text |
| docx skill | Skill | Ask user to paste text |
| xlsx skill | Skill | Ask user to provide CSV/text |
| theme-factory skill | Skill | Use built-in `references/style-presets.md` |
| deckdone-style skill | Skill | Use built-in `references/style-presets.md`, no icons or illustrations |
| react-icons | npm global | Use text-based icons or pre-rendered images |

## Python (Optional)

| Dependency | Type | Degradation if missing |
|-----------|------|----------------------|
| pypdf | pip | Image-type PDFs cannot be processed by extract-pdf.py |
| pypdfium2 | pip | Image-type PDFs cannot be rendered to PNG |
| pdfplumber | pip | Complex PDF layouts may extract text with lower fidelity |

If these packages are unavailable, image-type PDFs fall back to asking the user to paste text content.

## Dependency Detection

Check for optional dependencies at the point of use, not at startup:

- **Step 2 (Material Collection):** Before extracting from a file, check whether the relevant skill (pdf / docx / xlsx) is available. If unavailable, ask the user to paste the content as text.
- **Step 6 (Visual Style):** Check for the theme-factory skill to surface additional presets. If unavailable, rely solely on `references/style-presets.md`. Check for deckdone-style skill for enhanced presets and decoration rules.
- **Step 9 (Test Generation):** Check for sharp (npm global) before attempting SVG→PNG rasterization. If unavailable, use text-based icons or pre-rendered placeholder images. If deckdone-style is available, run `fetch-icon.py` and `fetch-illustration.py` for icons and illustrations.

See the repository root `SETUP.md` for installation instructions for all dependencies.
