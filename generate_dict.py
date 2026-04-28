import csv
import random
import string
import time

def generate_synthetic_data(filename="data/synthetic_searches.csv", target_records=1500000):
    """
    Generates a CSV file with over a million synthetic search terms.
    Word lengths are strictly between 3 and 20 characters.
    """
    print(f"Generating {target_records} records... This may take a moment.")
    start_time = time.time()
    
    alphabet = string.ascii_lowercase
    unique_words = set()
    records = []
    
    # Generate random words until we reach the target
    while len(records) < target_records:
        length = random.randint(3, 20)
        
        # Generate a completely random string of lowercase letters
        new_word = "".join(random.choices(alphabet, k=length))
        
        # Ensure uniqueness to simulate a properly grouped dataset
        if new_word not in unique_words:
            unique_words.add(new_word)
            
            # Assign a random popularity score 
            count = random.randint(1, 100000)
            records.append([new_word, count])
            
            # Print progress every 300,000 words
            if len(records) % 300000 == 0:
                print(f"Generated {len(records)} words...")

    # Write to CSV
    print(f"Saving to {filename}...")
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"]) # Header explicitly requested
        writer.writerows(records)

    end_time = time.time()
    print(f"Done! Created {len(records)} unique words in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    generate_synthetic_data()