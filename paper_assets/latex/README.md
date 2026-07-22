# LaTeX inclusion helpers

## Tables

Auto-copied `.tex` fragments live in `latex/tables/`.
Requires `booktabs` in the manuscript preamble.

Example:

```latex
\input{../localgovbench/paper_assets/latex/tables/T01_corpus_composition.tex}
```

Adjust the relative path to your manuscript tree.

## Figures

After running figure scripts, include PNGs, e.g.:

```latex
\includegraphics[width=\linewidth]{../localgovbench/paper_assets/figures/F01_corpus_record_counts/F01_corpus_record_counts.png}
```

Use captions from each figure's `caption.md`.
