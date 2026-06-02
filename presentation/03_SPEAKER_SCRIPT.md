# Speaker Script — Autocomplete Search System
**Adam Jaworski** & **Julia Winiarz** · 5 min presentation + 2 min Q&A

> **How to read this script.** Each block has a target time, the slide it pairs with, and a verbatim line you can read or paraphrase. The role tag (**[ADAM]** / **[JULIA]**) tells you who speaks. **Don't read the parentheticals out loud** — those are stage directions.
>
> **Total budget: 300 seconds.** We've allocated 285 s of speaking + 15 s of natural pauses and slide transitions. If you talk faster, that's a win — you'll have more demo time.

---

## Slide 1 · Title (≈ 10 s)

**[ADAM]** *(confident, 5 s)*
> "Hi, I'm Adam, and I'll cover the data ingestion and the prefix-filtering algorithm."

**[JULIA]** *(5 s)*
> "And I'm Julia — I'll cover the ranking algorithm, the data-structure trade-offs, and the bottleneck."

*(advance to slide 2)*

---

## Slide 2 · Problem Statement · 0:00 – 0:30 (30 s) — **[ADAM]**

> "As a user types into a search bar, our system has to suggest the **top five most likely completions in under fifty milliseconds**, drawing from a database of **millions** of historical search terms ranked by popularity.
>
> The naïve approach — scanning the full list on every keystroke — is **O of N** per keystroke. With a million records that's around a hundred milliseconds, and a single search query is typically five to fifteen keystrokes, so we'd blow the budget five to fifteen times over.
>
> Our goal is to push the per-keystroke cost from depending on **N**, the database size, to depending only on **L**, the prefix length."

*(advance to slide 3)*

---

## Slide 3 · Data Input & Edge Cases · 0:30 – 1:30 (60 s) — **[ADAM]**

> *(15 s)* "The input is a CSV with two columns — `word` and `count`. We tested with three hundred and thirty-three thousand real English unigrams from Kaggle, and a synthetic dataset of one and a half million records. At runtime the input is the raw UTF-8 string the user is typing."

> *(15 s)* "The expected output is the **top five word-score pairs**, ordered by descending popularity, all of which begin with what the user typed."

> *(30 s)* "We handle six classes of dirty data. **One:** trailing whitespace — stripped. **Two:** mixed casing — lowercased. **Three:** empty input — we return immediately, no traversal. **Four:** prefixes not in the database, like `zzzqq` — the trie walk returns `None` and we hand back an empty list. **Five:** blank or `nan` rows in the CSV — skipped on load. **Six:** missing CSV file — caught with a friendly error.
>
> The extreme-scale case worth flagging is a **one-letter prefix** like `a`, where the candidate subtree has tens of thousands of words. We handle that in the next algorithm with a pruning trick — Julia will pick that up."

*(advance to slide 4 — handoff)*

---

## Slide 4 · The Algorithmic Chain · 1:30 – 1:45 (15 s) — **[ADAM]**

> "Two algorithms in series. **Algorithm A**, the trie, takes the cleaned prefix and returns a single `TrieNode`. **Algorithm B**, depth-first search plus a min-heap, takes that node and returns the top five completions.
>
> The hand-off between us is exactly one Python object — that node."

*(advance to slide 5)*

---

## Slide 5 · Algorithm A — Trie · 1:45 – 2:30 (45 s) — **[ADAM]**

> *(20 s)* "A trie is a tree where each edge is a character. To find a prefix, we walk one character at a time, hopping through a hash-map of children. Lookup time depends only on the **prefix length**, not on the database size — doubling the dataset does **not** slow down a query."

> *(15 s)* "Asymptotics: insert is **theta of L**, find-prefix is **theta of L**, where L is the prefix length. Building the full trie is **O of W times L** — but that happens once at startup. Memory is also **O of W times L** in the worst case, because every node stores a dictionary of children."

> *(10 s)* "One detail that becomes important in a moment: every trie node also caches the **maximum popularity score** of any word in its subtree. We update it at insert time. Julia, over to you."

*(advance to slide 6 — hand mic to Julia)*

---

## Slide 6 · Algorithm B — DFS + Min-Heap · 2:30 – 3:30 (60 s) — **[JULIA]**

> *(20 s)* "I receive Adam's node — that subtree contains every word that starts with the prefix. I run a depth-first search, but with two production tweaks. **First**, I sort children by their cached `max_score` and visit the highest first — that's a best-first heuristic. **Second**, I keep a **min-heap of size five**, so I always know the score of my current fifth-best."

> *(20 s)* "The trick is the line: *if the heap is full and the current node's max-score is less than or equal to the heap's minimum, return immediately.* That entire subtree can't possibly produce a top-five answer, so we skip it. For the prefix `a` — which has roughly thirty thousand candidate words — we end up visiting only a tiny fraction."

> *(20 s)* "Asymptotics: worst-case DFS over the subtree is **O of N log K**, where N is the number of completions and K is five. With the pruning, the **expected** cost drops to roughly **O of K times L** — we essentially walk down the few highest-scoring paths and stop. Heap operations are **O of log five**, which is a constant. Heap memory is **O of K**, also constant."

*(advance to slide 7)*

---

## Slide 7 · Architectural Justification · 3:30 – 4:30 (60 s) — **[JULIA]**

> *(25 s)* "Two design choices we want to defend.
>
> **Why hash-map children instead of a balanced BST?** A BST gives us ordered traversal in **log c** time, where c is the alphabet. But we **never** need alphabetical traversal — we want *highest-score-first*, and we already get that for free from the cached `max_score`. So a BST would cost log time for a feature we don't use. The hash-map gives us **O of one** child lookup."

> *(15 s)* "**Why a min-heap instead of a sorted list?** For K equal to five the difference is small, but the heap generalises: if we ever bumped K to fifty or five hundred, sorted-list insertion is **O of K** and heap insertion stays at **O of log K**. The heap is the right general answer."

> *(20 s)* "**Primary bottleneck: memory, not time.** A query already finishes in under one millisecond on three hundred thousand words — fifty times under budget. The cost we *can't* hide is RAM: **O of W times L** for the trie. At billion-record scale you'd need a **Radix tree**, which compresses chains of single-child nodes and cuts memory five to ten times. As a secondary bottleneck, at extreme keystroke throughput, the per-character hash-map dispatch becomes the hot loop — that's fixable with a packed array of children for ASCII, or a DAWG."

*(advance to slide 8 — hand mic to Adam for demo)*

---

## Slide 8 · Live Demo · 4:30 – 5:00 (30 s) — **[ADAM]** (driving keyboard) + **[JULIA]** (narrating)

**SETUP, BEFORE YOU STAND UP:** have `python main.py` already running, trie pre-loaded, cursor blinking at the prompt. Don't waste the 30 s on the 2-second CSV load.

**[ADAM]** *(typing `pro` and pressing Enter, 5 s)*
> "Live system. I type `pro`…"

**[JULIA]** *(reading the result, 7 s)*
> "…top five: products, product, program, project, profile. **Zero point one milliseconds.**"

**[ADAM]** *(typing `kat`, 5 s)*
> "Different prefix — `kat`."

**[JULIA]** *(7 s)*
> "Kate, Katrina, Katie, Kathy, Kathleen. **Zero point zero three milliseconds.** And the missing-prefix case — `zzzqq` — returns nothing in a microsecond."

**[ADAM] / [JULIA] — together close, 6 s**
> "Two algorithms, one hand-off, one cached field — fifty times under the latency budget. Thank you, we're happy to take questions."

*(stop; pause for Q&A)*

---

# Q&A — Anticipated Questions & Crisp Answers

> Pick **one speaker** per question — whoever's domain it is. If the questioner doesn't aim it, **Adam** takes infrastructure / data questions, **Julia** takes algorithm / complexity questions.

### Q1 · "Why not just sort the candidate list?"
**[JULIA]** "Sorting all N candidates is **O of N log N**. We don't need a full ordering — we need only the top five. A min-heap of size five gives us **O of N log five**, which is essentially **O of N**, and with `max_score` pruning we don't even visit all N nodes. So we save both a `log N` factor and most of the constant."

### Q2 · "Doesn't sorting children at every DFS node hurt your asymptotics?"
**[JULIA]** "The number of children is bounded by the alphabet — twenty-six for ASCII — so it's **c log c**, a constant ≤ a hundred and twenty. We pay it because best-first traversal makes the `max_score` pruning fire after one or two branches instead of last."

### Q3 · "What if two words have the same popularity score?"
**[JULIA]** "The min-heap breaks ties by the second tuple element, which is the word string — so it's deterministic and lexicographic. We could plug in any tiebreaker — recency, click-through rate — without changing the algorithm."

### Q4 · "Memory usage on a billion records?"
**[ADAM]** "Roughly a billion times average prefix length — call it ten billion node references, which would not fit in RAM. We'd switch to a **Radix tree**: it merges chains of single-child nodes into one edge with a string label. On English text that compresses around five to ten times. For multi-language deployments you'd shard by first character or use a DAWG."

### Q5 · "Why Python? Wouldn't C++ be faster?"
**[ADAM]** "Python is what the assignment evaluates and the latency budget is fifty milliseconds — we're at zero point one. We have a five-hundred-times margin. C++ would buy us throughput, not latency — relevant only if we served millions of QPS, which is a different problem."

### Q6 · "How do you handle typos / fuzzy matching?"
**[JULIA]** "Not in scope today — pure trie can't do fuzzy. The standard extension is a **Levenshtein automaton** layered on top of the trie, which tolerates `k` edits in **O of L times k** per node. Compatible with our pipeline: replace `find_prefix_node` with a fuzzy walk, keep the heap stage unchanged."

### Q7 · "Why does the empty prefix finish in under a millisecond if it has to scan everything?"
**[JULIA]** "It doesn't actually scan everything. The root's children are visited in `max_score` order, and once the heap fills with the five most popular words on the planet, every other subtree fails the pruning check on its very first comparison. We touch maybe a few dozen nodes."

### Q8 · "What's the worst case you actually hit?"
**[JULIA]** "A prefix where many subtrees have similar `max_score` — the pruning becomes weaker. We can construct a synthetic adversary, but on real English data we never measured a query above one millisecond on three hundred thousand words."

### Q9 · "Could you do this with a SQL `LIKE 'pro%'`?"
**[ADAM]** "With an index on the prefix, yes — but database round-trips dominate. A B-tree index on a million rows is roughly **O of log N** for the prefix scan, then we'd still need to rank. Our trie keeps everything in memory and the whole pipeline is one process call. For a search-bar UX, in-process is the right answer."

---

## Pre-flight checklist (5 minutes before going up)

1. **Open the terminal**, `cd` into the repo, run `python main.py` and **let it finish loading** so the prompt is blinking when you start.
2. Have **three prefixes** queued in your head: `pro`, `kat`, `zzzqq`. Don't improvise live.
3. **Enlarge the terminal font** — examiners will be reading from a distance.
4. Confirm both presenters know **whose slide each one is** (this script).
5. Decide a **graceful exit signal** — e.g. Adam taps the table after his last line on slide 8, Julia delivers the close.
6. Bring the **slide deck on a USB stick AND on Google Drive** — projectors are unreliable.

## Speaking-time budget summary

| Slide | Topic | Speaker | Time |
|---|---|---|---|
| 1 | Title | A + J | 10 s |
| 2 | Problem | A | 30 s |
| 3 | Data & edge cases | A | 60 s |
| 4 | Chain diagram | A | 15 s |
| 5 | Algorithm A — Trie | A | 45 s |
| 6 | Algorithm B — DFS+Heap | J | 60 s |
| 7 | Justification & bottleneck | J | 60 s |
| 8 | Live demo | A + J | 30 s |
| **Total** | | | **310 s** |

> 310 s is intentionally 10 s over the strict 5-minute limit so that, when the inevitable slow-down happens (laptop unlock, projector wake-up, a sentence rephrased), you still land at or under 300 s. **Practice once with a stopwatch.** If you finish in 4:40 in rehearsal, you'll finish in 4:55 live.
