# Generator source

Every SVG, JSON, CSS and Markdown file in this package, plus the standalone PDF, is generated from `tokens.py` by these scripts.
Change a value in `tokens.py`, re-run, and every artefact updates together.

```
pip install pillow playwright && playwright install chromium
python build_foundations.py && python build_components.py && python build_screens.py \
  && python build_deck.py && python build_docs.py && python build_impl.py && python build_pdf.py
```
Paths at the top of each script (`OUT` / `ROOT`) point to the output folder; font paths in `svgkit.py` point to the bundled `fonts/`.
