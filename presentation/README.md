# Presentation materials

Everything you need for the 5-minute final presentation, in the order you should read it.

| # | File | What's inside |
|---|---|---|
| 1 | [`01_APPROACH_REVIEW.md`](./01_APPROACH_REVIEW.md) | Honest review of your approach: what's strong, what to defend, small polish items |
| 2 | [`Autocomplete_Presentation.pptx`](./Autocomplete_Presentation.pptx) | **Editable PowerPoint deck** — open in PowerPoint / Google Slides / Keynote |
| 3 | [`Autocomplete_Presentation.pdf`](./Autocomplete_Presentation.pdf) | Read-only PDF backup of the same deck |
| 4 | [`02_SLIDES.md`](./02_SLIDES.md) | Marp markdown source for the deck (used to regenerate the PPTX/PDF if needed) |
| 5 | [`03_SPEAKER_SCRIPT.md`](./03_SPEAKER_SCRIPT.md) | Word-for-word script split between Adam and Julia, with timing per slide and Q&A answers |

## Editing the slides

The recommended path is to **open `Autocomplete_Presentation.pptx` directly** in PowerPoint, Google Slides, or Keynote and edit there.

> **Tip — fonts & code blocks.** The deck uses the default theme font. Code blocks are rendered as monospaced text inside a colored box. If a code block looks off after editing, set its font to "Consolas" or "Menlo" at 18 pt and apply a light-grey fill.

## Re-generating the slides from the markdown source

If you change `02_SLIDES.md` and want fresh PPTX / PDF files:

```bash
cd /workspace
npx @marp-team/marp-cli@latest presentation/02_SLIDES.md --pptx --no-stdin -o presentation/Autocomplete_Presentation.pptx
npx @marp-team/marp-cli@latest presentation/02_SLIDES.md --pdf  --no-stdin -o presentation/Autocomplete_Presentation.pdf
```

Marp also runs as a VS Code extension (*"Marp for VS Code"*) — you get a live preview and an export button.

## Demo run-of-show

Before standing up:

```bash
cd /workspace
python main.py
# wait for "Welcome to the Autocomplete System!"
# leave the prompt blinking — DO NOT close the terminal
```

During slide 8, type these three prefixes in order: `pro` → `kat` → `zzzqq`.

That's it. Good luck.
