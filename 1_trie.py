import csv
import time

class TrieNode:
    """
    Represents a single node (letter) in the Trie.
    """
    def __init__(self):
        # Hash map (dictionary) for O(1) lookup of child nodes
        self.children = {}
        # Flag to mark if a word ends at this specific node
        self.is_end = False
        # The frequency/popularity score of the word (0 if not an end node)
        self.score = 0
        # Storing the full word here makes it easier for Person 2 to collect results
        self.word = ""

class Trie:
    """
    The main Trie data structure.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, score: int):
        """
        Inserts a word and its score into the Trie.
        Time Complexity: O(L) where L is the length of the word.
        """
        node = self.root
        for char in word:
            # If the character path doesn't exist, create a new node
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move down the tree
            node = node.children[char]
        
        # We reached the end of the word. Mark it and save the data.
        # This elegantly handles nested words (e.g., "kos" and "kosodrzewina")
        node.is_end = True
        node.score = score
        node.word = word

    def find_prefix_node(self, prefix: str) -> TrieNode:
        """
        Travels down the Trie following the prefix.
        Returns the node where the prefix ends, or None if not found.
        Time Complexity: O(P) where P is the length of the prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None # Prefix does not exist in our database
            node = node.children[char]
        
        return node # This is the "handoff" point for Person 2

def preprocess_input(user_input: str) -> str:
    """
    Cleans the raw user input to handle edge cases.
    - Removes leading/trailing whitespaces
    - Converts to lowercase
    """
    if not user_input:
        return ""
    return user_input.strip().lower()

def load_data_into_trie(csv_filepath: str) -> Trie:
    """
    Reads the CSV file and populates the Trie.
    Expects a CSV with 'word' and 'count' columns.
    """
    trie = Trie()
    loaded_count = 0
    
    print("Loading data into Trie... This might take a few seconds.")
    start_time = time.time()
    
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = str(row['word'])
                
                # Skip empty data rows
                if not word or word == "nan": 
                    continue
                
                # Clean the word just in case the dataset has dirty entries
                clean_word = preprocess_input(word)
                score = int(row['count'])
                
                trie.insert(clean_word, score)
                loaded_count += 1
                
    except FileNotFoundError:
        print(f"Error: The file '{csv_filepath}' was not found.")
        print("Please download it from Kaggle and place it in the project folder.")
        return trie

    end_time = time.time()
    print(f"Successfully loaded {loaded_count} words in {end_time - start_time:.2f} seconds.\n")
    return trie

# ==========================================
# TEST BLOCK (For Person 1 to verify logic)
# ==========================================
if __name__ == "__main__":
    # 1. Initialize and load data (make sure unigram_freq.csv is in the folder)
    # If you don't have the file yet, you can test with a dummy CSV or comment this out
    #my_trie = load_data_into_trie("data/unigram_freq.csv")
    my_trie = load_data_into_trie("data/synthetic_searches.csv")
    # 2. Simulate user input
    raw_user_input = "  Pro  " # Testing edge cases (spaces and uppercase)
    clean_prefix = preprocess_input(raw_user_input)
    print(f"User typed: '{raw_user_input}' -> Cleaned to: '{clean_prefix}'")
    
    # 3. Execute Algorithm A
    start_search = time.time()
    prefix_node = my_trie.find_prefix_node(clean_prefix)
    end_search = time.time()
    
    # 4. Verify results
    search_time_ms = (end_search - start_search) * 1000
    if prefix_node:
        print(f"Prefix found! Handing over the node to Person 2.")
        print(f"Algorithm A execution time: {search_time_ms:.5f} ms")
        print(f"Node dictionary contains keys (next possible letters): {list(prefix_node.children.keys())[:10]}...")
    else:
        print("Prefix not found in the database.")