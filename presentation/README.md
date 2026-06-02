# Presentation materials

Everything you need for the 5-minute final presentation, in the order you should read it.

| # | File | What's inside |
|---|---|---|
| 1 | [`01_APPROACH_REVIEW.md`](./01_APPROACH_REVIEW.md) | Honest review of your approach: what's strong, what to defend, small polish items |
| 2 | [`02_SLIDES.md`](./02_SLIDES.md) | 8 slides + 3 backup slides, in [Marp](https://marp.app/) markdown — opens straight in VS Code, exports to PDF / PPTX |
| 3 | [`03_SPEAKER_SCRIPT.md`](./03_SPEAKER_SCRIPT.md) | Word-for-word script split between Adam and Julia, with timing per slide and Q&A answers |

## Rendering the slides

The slides are written in **Marp** markdown. Three easy ways to view / export:

**Option A — VS Code** *(easiest)*
1. Install the extension *"Marp for VS Code"*.
2. Open `02_SLIDES.md`.
3. Click the *Marp preview* icon in the top-right of the editor.
4. To export: command palette → *"Marp: Export slide deck"* → pick PDF or PPTX.

**Option B — CLI**
```bash
npx @marp-team/marp-cli@latest 02_SLIDES.md -o slides.pdf
npx @marp-team/marp-cli@latest 02_SLIDES.md -o slides.pptx
```

**Option C — copy into Google Slides**
The deck is plain markdown headings + tables. If Marp is unavailable, copy each `---`-separated section into a Google Slides slide manually. Estimated time: 15 minutes.

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
