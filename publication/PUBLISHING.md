# Publication Workflow

## Generated Files

- `publication/synthesis_paper.html` — standalone HTML with water.css styling. Open in any browser, Print → Save as PDF for a review-ready document.
- `publication/synthesis_paper.tex` — LaTeX source, ready for Overleaf or local TeX compilation (needs a TeX distribution like MiKTeX or TeX Live).
- `publication/synthesis_paper.md` — source markdown (symlinked from `main/synthesis_paper.md`).

## Tools Installed

- **Pandoc 3.6.4** (portable) at `C:\Users\AmosA\pandoc\pandoc-3.6.4\pandoc.exe`
- **weasyprint** installed via pip but non-functional on this Windows machine (missing GTK runtime)
- **LaTeX (pdflatex) not available** — needs MiKTeX portable or TeX Live install

## How to Generate PDF

### Option A: Browser (fastest, works now)
1. Open `publication/synthesis_paper.html` in Chrome/Edge
2. Ctrl+P → Save as PDF
3. Margins: 1 inch, ✓ Background graphics

### Option B: Overleaf (for proper LaTeX typesetting)
1. Upload `publication/synthesis_paper.tex` to overleaf.com
2. Compile → Download PDF

### Option C: Install TeX Live / MiKTeX
1. Download MiKTeX portable: https://miktex.org/download
2. Extract to `C:\Users\AmosA\miktex`
3. Run: `pandoc synthesis_paper.md -o synthesis_paper.pdf --pdf-engine=pdflatex`

## Regenerating

```bash
pandoc main/synthesis_paper.md -o publication/synthesis_paper.tex --standalone --number-sections --toc
pandoc main/synthesis_paper.md -o publication/synthesis_paper.html --standalone --toc --metadata title="The phi-Attractor" --css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.css
```
