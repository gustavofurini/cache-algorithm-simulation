# Cache-Algorithm-Simulation

This Python application simulates different cache algorithms to optimize text loading times for a reading application with limited memory. The objective is to minimize the time spent loading files from a slow, forensically secure disk system. The system can store a maximum of 10 texts in memory at any given time, and the application supports three cache algorithms: Least Recently Used (LRU), First In First Out (FIFO), and Least Frequently Used (LFU). The program simulates user requests for texts, tracks cache hits and misses, and measures the time taken for each request.

The program generates text files based on the description provided, by downloading public domain books (like from Project Gutenberg) and dividing them into smaller texts. Each of these generated texts is used in the simulation.

## Project Structure

### 1. **TextCache Class**  
   This is the base class that defines the structure for storing and retrieving texts from memory. It handles adding new texts to the cache and managing the cache order.

### 2. **Cache Algorithm Classes**  
   - **LRUCache**: Implements the Least Recently Used (LRU) cache algorithm, which evicts the least recently accessed item when the cache exceeds its capacity.
   - **FIFOCache**: Implements the First In First Out (FIFO) cache algorithm, which evicts the oldest item in the cache when it exceeds its capacity.
   - **LFUCache**: Implements the Least Frequently Used (LFU) cache algorithm, which evicts the least frequently accessed item.

### 3. **Simulation and Metrics**  
   The program simulates the process of accessing the texts, measuring the time taken for each request and tracking the number of cache hits and misses for each algorithm. The results are stored and output as a simulation report.

### 4. **Main Application**  
   The user interface allows the user to interact with the program by inputting text IDs, viewing text content, and entering simulation mode for cache algorithm testing.

## How It Works

- **Text Storage**: The program generates 100 different text files, each with more than 1000 words, from public domain books such as those available on Project Gutenberg. The texts are divided into smaller sections and saved as `.txt` files.
- **Cache Management**: The program supports three cache algorithms (LRU, FIFO, and LFU) to manage the memory efficiently and minimize the loading times for texts.
- **Cache Access**: The program simulates user access to these text files, and if a file is not in memory, it is loaded from disk (simulated by generating or retrieving the text). The program tracks cache hits and misses.
- **Simulation Mode**: When the user enters simulation mode, the program performs tests using 3 simulated users. Each user performs 200 file requests with random selection methods and tracks cache performance metrics such as cache hits, misses, and the time taken for each request.
- **Reporting**: After running the simulation, a report is generated, showing the performance of each algorithm, the average time per request, and the number of cache hits and misses.

## Clone the repository:
   ```bash
   git clone https://github.com/ThomasFrentzel/Cache-Algorithm-Simulation
   ```

