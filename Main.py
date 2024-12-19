import time
import random
from collections import defaultdict
import nltk
import numpy as np
nltk.download('punkt')

# Cache Structure
class TextCache:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.cache = {}
        self.cache_order = []

    def put(self, text_id, text):
        if len(self.cache) >= self.max_size:
            old_text_id = self.cache_order.pop(0)
            del self.cache[old_text_id]

        self.cache[text_id] = text
        self.cache_order.append(text_id)

    def get(self, text_id):
        if text_id in self.cache:
            self.cache_order.remove(text_id)
            self.cache_order.append(text_id)
            return self.cache[text_id]
        else:
            return None


# Cache Algorithms
# LRU (Least Recently Used)
class LRUCache(TextCache):
    def get(self, text_id):
        text = super().get(text_id)
        if text:
            self.cache_order.remove(text_id)
            self.cache_order.append(text_id)
        return text

# FIFO (First In First Out)
class FIFOCache(TextCache):
    def put(self, text_id, text):
        if len(self.cache) >= self.max_size:
            old_text_id = self.cache_order.pop(0)
            del self.cache[old_text_id]
        super().put(text_id, text)

# LFU (Least Frequently Used)
class LFUCache(TextCache):
    def __init__(self, max_size=10):
        super().__init__(max_size)
        self.frequency = {}

    def put(self, text_id, text):
        if len(self.cache) >= self.max_size:
            least_frequent_text_id = min(self.frequency, key=self.frequency.get)
            del self.cache[least_frequent_text_id]
            del self.frequency[least_frequent_text_id]
            self.cache_order.remove(least_frequent_text_id)

        super().put(text_id, text)
        self.frequency[text_id] = 0

    def get(self, text_id):
        text = super().get(text_id)
        if text:
            self.frequency[text_id] += 1
        return text


# Function to simulate cache access
def simulate_access(cache_algorithm, cache_size, num_requests=200):
    # Variables to count cache hits and misses and calculate total time
    cache_hit_count = 0
    cache_miss_count = 0
    total_time = 0

    # Initialize cache with selected algorithm
    cache = cache_algorithm(max_size=cache_size)

    # Mark the start time of the simulation
    start_time = time.time()

    # Loop through the number of requests specified
    for _ in range(num_requests):
        # Generate text IDs for different scenarios
        simple_text_id, poisson_text_id, pct_33_text_id = choose_text()

        # Mark the start time of the current request
        start_req_time = time.time()

        # Variable to store the text ID found in the cache (hit)
        text_id_hit = None

        # Loop through the text IDs, trying to find one in the cache
        for text_id in [simple_text_id, poisson_text_id, pct_33_text_id]:
            text = cache.get(text_id)
            if text is not None:
                cache_hit_count += 1
                text_id_hit = text_id
                break

        # If no text was found in the cache (miss), randomly select one of the IDs and add it to the cache
        if text_id_hit is None:
            cache_miss_count += 1
            time.sleep(0.1)  # Simulate access to the data source
            text_id_hit = random.choice([simple_text_id, poisson_text_id, pct_33_text_id])
            text = f'Text {text_id_hit}'
            cache.put(text_id_hit, text)

        # Mark the end time of the current request
        end_req_time = time.time()

        # Calculate the total time spent on the requests
        total_time += end_req_time - start_req_time

    # Mark the end time of the simulation
    end_time = time.time()

    # Calculate the average time per request
    avg_time_per_request = total_time / num_requests

    # Return the hit and miss counts, and the average time per request
    return cache_hit_count, cache_miss_count, avg_time_per_request


# Function to choose the text ID based on specified criteria
def choose_text():
    simple_text_id = random.randint(1, 100)
    poisson_text_id = np.random.poisson(50)
    if random.random() < 0.33:
        pct_33_text_id = random.randint(30, 40)
    else:
        pct_33_text_id = random.randint(1, 100)
    return simple_text_id, poisson_text_id, pct_33_text_id


# Function to generate the report
def generate_report(cache_algorithms, cache_size):
    report = defaultdict(lambda: defaultdict(dict))
    users = ['User 1', 'User 2', 'User 3']
    for user in users:
        for algo_name, algo_class in cache_algorithms.items():
            cache_hit_count, cache_miss_count, avg_time_per_request = simulate_access(algo_class, cache_size)
            report[user][algo_name]['cache_hit_count'] = cache_hit_count
            report[user][algo_name]['cache_miss_count'] = cache_miss_count
            report[user][algo_name]['avg_time_per_request'] = avg_time_per_request
    return report


# Function to read according to the number
def read_text(text_id):
    try:
        with open(f'output_{text_id}.txt', 'r') as file:
            text = file.read()
            print(text)
    except FileNotFoundError:
        print("Text not found.")


# Main function
def main():

    cache_size = 10
    cache_algorithms = {
        'LRU': LRUCache,
        'FIFO': FIFOCache,
        'LFU': LFUCache
    }

    while True:
        test = input("Enter the number that identifies the desired text (or -1 to enter simulation mode, 0 to exit): ")
        try:
            text_id = int(test)
            if text_id == 0:
                print("Closing the program...")
                break
            elif text_id == -1:
                print("Entering simulation mode...")
                report = generate_report(cache_algorithms, cache_size)
                with open('Simulation_report.txt', 'w') as file:
                    for user, data in report.items():
                        file.write(f"{user}:\n")
                        for algo_name, algo_data in data.items():
                            file.write(f"Cache Algorithm: {algo_name}\n")
                            file.write(f"Cache hit: {algo_data['cache_hit_count']}\n")
                            file.write(f"Cache miss: {algo_data['cache_miss_count']}\n")
                            file.write(f"Average time per request: {algo_data['avg_time_per_request']:.4f} seconds\n\n")
                print("Simulation report successfully generated.")
            else:
                read_text(text_id)
        except ValueError:
            print("Please enter a valid integer number.")


if __name__ == "__main__":
    main()