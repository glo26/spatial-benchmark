# SpatialEval Paper - arXiv Submission

This folder contains the LaTeX source files for the SpatialEval paper targeting NeurIPS 2026 Datasets & Benchmarks Track.

## Files

- `spatialeval.tex` - Main LaTeX source file
- `references.bib` - BibTeX bibliography file
- `neurips_2023.sty` - NeurIPS style file
- `figures/` - Paper figures

## Compilation

To compile the paper:

```bash
cd arxiv
pdflatex spatialeval.tex
bibtex spatialeval
pdflatex spatialeval.tex
pdflatex spatialeval.tex
```

## Version

**Draft v1** - February 2026
