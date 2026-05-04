from trie_engine import load_data_into_trie, preprocess_input
from heap_ranker import get_top_5_completions
import time


def main():
    # default to the smaller dataset for faster testing, but can switch to the larger one if needed
    trie_database = load_data_into_trie("data/amazon_dataset_1000000.csv")

    if not trie_database.root.children:
        print("Trie database is empty. Please check the data loading step.")
        return

    print("Welcome to the Autocomplete System!")

    while True:
        user_input = input(
            "Type a search term prefix and press Enter to get suggestions or 'quit' to exit.\n>"
        )
        if user_input.lower() == "quit":
            print("Exiting the Autocomplete System. Goodbye!")
            break

        start_time = time.time()

        # Algorithm A
        clean_prefix = preprocess_input(user_input)
        if not clean_prefix:
            print("Please enter a valid prefix (at least 3 characters).")
            continue
        prefix_node = trie_database.find_prefix_node(clean_prefix)

        # Algorithm B
        top_5_suggestions = get_top_5_completions(prefix_node)

        end_time = time.time()
        exe_time = end_time - start_time

        if top_5_suggestions:
            print(f"Top suggestions for '{clean_prefix}':")
            for rank, (query, score) in enumerate(top_5_suggestions, start=1):
                print(f"{rank}. {query} (score: {score})")
        else:
            print(f"No suggestions found for '{clean_prefix}'.")

        print(f"Search completed in {exe_time:.4f} seconds.\n")


if __name__ == "__main__":
    main()
