# Autocomplete Search System

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-live_demo_ready-success.svg)

This project demonstrates a highly optimized system designed to solve a real-world engineering problem: **Suggesting the top 5 most likely search completions from a dataset of millions of records in under 50ms.** This project was built to showcase architectural decision-making, algorithm chaining, and Big $O$ optimization.

## 🎯 The Problem
As a user types into a search bar, the system must suggest completions on the fly. Scanning a database of millions of historical search terms character-by-character for every keystroke is computationally unfeasible. The system requires a high-speed filtering mechanism combined with an efficient ranking algorithm.

## 🧠 Algorithmic Chain & Architecture

The solution chains two distinct algorithms, clearly separating the filtering phase from the ranking phase.

### Algorithm A: Prefix Filtering (Trie)
* **Role:** Reduces the massive dataset into a small subset of valid candidates based on the user's input.
* **Data Structure:** Hash-Map based Trie (Prefix Tree).
* **Time Complexity:** $O(L)$ where $L$ is the length of the typed prefix. Lookup time is constant regardless of database size.
* **Output:** Returns the specific `TrieNode` representing the end of the user's prefix.

### Algorithm B: Ranking & Selection (DFS + Min-Heap)
* **Role:** Extracts all possible word completions from the sub-tree and strictly keeps the top 5 most popular results.
* **Data Structure:** Depth-First Search (DFS) paired with a Min-Heap (`heapq`).
* **Time Complexity:** $O(N \log K)$ where $N$ is the number of valid completions in the sub-tree, and $K = 5$. Since $K$ is small and constant, insertion effectively approaches $O(1)$.
* **Input:** Receives the `TrieNode` from Algorithm A.

## ⚠️ System Bottleneck
While Time Complexity is highly optimized, the primary bottleneck is **Space Complexity / RAM**. A standard Trie stores a dictionary of references at every node, resulting in $O(W \cdot L)$ space complexity (where $W$ is total words and $L$ is average length). In a production environment with billions of records, a compressed Radix Tree would be required to mitigate memory exhaustion.

## 📂 Project Structure

```text
├── data/
│   └── synthetic_searches.csv   # Dataset containing up to 1.5M (by default, may be more or less) historical syntethic searches
│   └── unigram_freq.csv         # Dataset from [kaggle](https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download&select=unigram_freq.csv) containing 333.333 english words with counts.
├── generate_data.py             # Script to generate random synthetic datasets
├── trie_engine.py               # Module containing Trie implementation (Algorithm A)
├── heap_ranker.py               # Module containing DFS & Min-Heap logic (Algorithm B)
├── main.py                      # Main entry point for the Live Demo
└── README.md
```

## 🚀 How to Run the Live Demo

**1. Generate the dataset:**
Generate a synthetic dataset of 1.5 million records (takes about 10 seconds):

    `python generate_data.py`

*(Make sure to move the generated `synthetic_searches.csv` into the `data/` folder).*

**2. Run the interactive demo:**

    `python main.py`

Type any prefix (e.g., `pro`, `kat`, `kwdadn`) into the terminal to see the top 5 suggestions and the execution time in milliseconds.

## 🤝 Contributors
* **Adam Jaworski:** Data Ingestion & Prefix Filtering
* **Julia Winiarz:** Depth-First Search & Min-Heap Ranking