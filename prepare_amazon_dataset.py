from datasets import load_dataset
import csv
from collections import defaultdict

# Default output path and target unique query count for the prepared dataset
OUTPUT_PATH = "data/amazon_dataset_1000000.csv"
TARGET_UNIQUE = 1000000


def main():
    print("Loading AmazonQAC (streaming mode)...")

    dataset = load_dataset("amazon/AmazonQAC", split="train", streaming=True)

    counter = defaultdict(int)

    print("Processing dataset...")

    for i, row in enumerate(dataset):
        query = row["final_search_term"]
        popularity = row["popularity"]

        if not query:
            continue
        if query not in counter:
            if len(counter) >= TARGET_UNIQUE:
                break

        counter[query] += popularity

        query = query.strip().lower()

        if len(counter) >= TARGET_UNIQUE:
            print(f"Reached {TARGET_UNIQUE} unique queries")
            break

        if i % 100000 == 0:
            print(f"Processed {i} rows...")

    print("Saving to CSV...")

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])

        for word, count in counter.items():
            writer.writerow([word, count])

    print(f"Done! Saved {len(counter)} unique queries to {OUTPUT_PATH}")
    return


if __name__ == "__main__":
    main()
