# ============================================================================
# IST — Paper build pipeline
#
#   markdown  →  pandoc  →  .tex  →  xelatex (2 passes)  →  PDF
#
# Requirements (verified on this machine):
#   - pandoc portable : C:\Users\AmosA\pandoc\pandoc-3.6.4\pandoc.exe
#   - MiKTeX / XeLaTeX: C:\Users\AmosA\AppData\Local\Programs\MiKTeX\miktex\bin\x64
#   - Must use XeLaTeX, NOT pdflatex (docs contain literal Unicode φ)
#
# Usage:
#   powershell -File publication\build_paper.ps1 [-Source main\ist_v7_0_topology_substrate.md]
#
# Outputs (in publication/):
#   - <stem>.tex     LaTeX source (Overleaf-compatible)
#   - <stem>.pdf     rendered PDF
# ============================================================================
param(
    [string]$Source = "main\ist_v8_0_topology_substrate.md"
)

$ErrorActionPreference = "Stop"
$root  = Split-Path -Parent $PSScriptRoot
$stem  = [System.IO.Path]::GetFileNameWithoutExtension($Source)
$out   = Join-Path $root "publication"
$srcAbs = Join-Path $root $Source

$pandoc   = "C:\Users\AmosA\pandoc\pandoc-3.6.4\pandoc.exe"
$miktex   = "C:\Users\AmosA\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
$env:Path = "$miktex;$env:Path"

if (-not (Test-Path $srcAbs)) { throw "Source not found: $srcAbs" }
if (-not (Test-Path $pandoc)) { throw "Pandoc not found: $pandoc" }
if (-not (Test-Path (Join-Path $miktex "xelatex.exe"))) { throw "xelatex not found" }

Write-Host "[1/3] pandoc: markdown -> LaTeX"
& $pandoc $srcAbs `
    --from=markdown-yaml_metadata_block `
    --resource-path="$root" `
    -o (Join-Path $out "$stem.tex") `
    --standalone --toc `
    --shift-heading-level-by=-1 `
    -V geometry:letterpaper `
    -V geometry:margin=0.75in `
    -V fontsize=11pt `
    -H (Join-Path $out "preamble.tex") `
    --metadata title="Information Substrate Theory (IST): Topology as a Substrate for Emergent Physics" `
    --metadata author="Dr. Mary Theadoor -- The Nown Research Group" `
    --metadata date="Version 8.0 - August 2026"
if ($LASTEXITCODE -ne 0) { throw "pandoc failed (exit $LASTEXITCODE)" }

Write-Host "[2/3] xelatex pass 1"
& xelatex -interaction=nonstopmode -halt-on-error -output-directory="$out" (Join-Path $out "$stem.tex")
if ($LASTEXITCODE -ne 0) { throw "xelatex pass 1 failed (exit $LASTEXITCODE)" }

Write-Host "[3/3] xelatex pass 2 (resolve cross-references)"
& xelatex -interaction=nonstopmode -halt-on-error -output-directory="$out" (Join-Path $out "$stem.tex")
if ($LASTEXITCODE -ne 0) { throw "xelatex pass 2 failed (exit $LASTEXITCODE)" }

$pdf = Join-Path $out "$stem.pdf"
Write-Host "Done. PDF: $pdf"
Write-Host "Pages: $((Get-ChildItem $pdf).Length) bytes"
