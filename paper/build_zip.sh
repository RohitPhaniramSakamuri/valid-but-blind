#!/usr/bin/env bash
# Builds a flat Overleaf-ready zip and compiles it from a clean folder as a check. Usage: build_zip.sh <scratch dir>
set -e
T="$1/ziptest"; rm -rf "$T"; mkdir -p "$T"
cp main.tex references.bib llncs.cls splncs04.bst "$T"/; cp -r figures "$T"/
(cd "$T"; pdflatex -interaction=nonstopmode main.tex >/dev/null; bibtex main >/dev/null; pdflatex -interaction=nonstopmode main.tex >/dev/null; pdflatex -interaction=nonstopmode main.tex > final.log; grep -cE '^!' main.log || true; grep -E 'Warning: (Citation|Reference)|undefined' main.log | head; pdfinfo main.pdf | grep Pages)
cp "$T/main.pdf" manuscript_preview.pdf; cp "$T/main.bbl" main.bbl
rm -f springer_overleaf.zip
zip -qr springer_overleaf.zip main.tex main.bbl references.bib llncs.cls splncs04.bst figures
unzip -l springer_overleaf.zip | tail -10
