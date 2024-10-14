
# Autocomplete Search - System Design

## 1. Use Case Description
Implement an efficient autocomplete search feature for their internal web application, used by the front office, scouts, and coaching staff. The system is designed to allow users to search for players, teams, and leagues, and it must handle a small load of no more than 100 simultaneous users. The goal is to provide fast, real-time search suggestions while optimizing data storage, indexing, and query efficiency. This system uses a Redis-based Trie for autocomplete suggestions, processes logs for optimization using Apache Spark, and stores detailed information in PostgreSQL.

## 2. Goals
The primary goals of this project are:
- **Low Latency**: Autocomplete results must appear as the user types, so latency should be minimized. The target response time should be under 100 ms for each query.
- **Scalability**: Although the application only serves around 100 users, it should efficiently handle any potential increase in data size (e.g., player stats, historical data).
- **Relevancy**: The search results must be relevant and contextual. For example, if a scout types "LeB," the system should rank "LeBron James" over others based on usage patterns or player popularity.


## 3. Technologies Required
### React (Frontend)
- **Role**: Provides a responsive, fast, and interactive UI for users to input their search queries.
- **Why React?**: React offers efficient rendering and state management, making it ideal for building a fast, interactive search interface. Its virtual DOM provides better performance compared to other frameworks like Angular.

### Node.js (Backend)
- **Role**: Acts as the central server that handles API requests from the frontend and communicates with both Redis and PostgreSQL for data retrieval and processing.
- **Why Node.js?**: Node.js is lightweight and highly efficient for handling I/O-bound tasks, making it suitable for real-time applications with multiple asynchronous operations.

### Redis (In-memory Cache using Trie Data Structure)
- **Role**: Stores frequently used search terms in the form of Trie structures for fast prefix matching and autocomplete suggestions.
- **Why Redis?**: Redis offers blazing-fast read/write speeds and is ideal for caching. The Trie data structure stored in Redis allows for highly efficient autocomplete functionality by enabling prefix-based search.

### PostgreSQL (Relational Database)
- **Role**: Stores the detailed player, team, and league data, which is queried if Redis does not have a relevant cached result.
- **Why PostgreSQL?**: PostgreSQL provides ACID compliance and advanced indexing mechanisms like B-Trees, which ensure that queries are efficient and data is reliable.

### Apache Logs (Logging User Interactions)
- **Role**: Tracks all user interactions, including the search queries they perform, which are logged for analysis.
- **Why Apache Logs?**: Apache logs provide detailed tracking of user activity, which is essential for understanding search patterns and improving autocomplete accuracy.

### Apache Spark (Batch Processing of Logs)
- **Role**: Periodically processes the logs to identify frequently searched terms and updates the Trie in Redis for optimized autocomplete performance.
- **Why Apache Spark?**: Spark is highly efficient for batch processing large datasets and is ideal for analyzing logs to detect frequent search patterns. It ensures that the Trie in Redis is always updated with the latest trends from real-world usage.

## 4. System Design
The autocomplete system is built on a multi-tier architecture to ensure efficiency, scalability, and maintainability.

### Key Components:
- **Frontend (React)**: Users input search queries into the web interface, and these queries are sent to the backend.
- **Backend (Node.js)**: Receives search queries, checks Redis for cached Trie data, and interacts with PostgreSQL if the data is not cached.
- **Redis (Caching Layer)**: Contains Trie data structures for fast prefix-based search. The cached data includes frequently searched terms.
- **PostgreSQL (Persistent Data Storage)**: Stores detailed information about players, teams, and leagues, and provides data for uncommon queries not found in Redis.
- **Apache Logs**: Captures search requests and logs them for further analysis.
- **Apache Spark**: Periodically processes Apache logs to generate new Trie structures based on frequently searched terms. These Tries are then stored back into Redis for faster future searches.

## 5. Workflow
### User Input:
1. Debouncing: As the user types a search query (e.g., "Le"), the React frontend implements a debouncing mechanism. Instead of sending an API request for every keystroke, it waits for a short period (e.g., 300 milliseconds) after the user stops typing before sending the request. This reduces the number of API calls made to the backend and helps improve overall performance and efficiency.
2. The user types a search query (e.g., "Le") in the search bar. After a brief pause, the debounced function triggers, sending the query to the Node.js backend via an API request (`GET /autocomplete?q=le`).

### Trie Lookup in Redis:
1. The backend checks Redis for a cached Trie structure that matches the query prefix (e.g., `/autocomplete?q=le`).
2. If a match is found in Redis: The system retrieves the relevant autocomplete suggestions and sends them back to the user.
3. If no match is found: The backend queries PostgreSQL for the detailed player, team, or league data.

### PostgreSQL Query:
1. PostgreSQL retrieves the requested data, which is then sent to the user and cached in Redis as a Trie for faster future access.

### Log Capture:
1. Each search query is logged in Apache logs for further processing.

### Apache Spark Log Processing:
1. Periodically, Apache Spark processes the logs to identify frequently searched terms.
2. It constructs Trie structures based on these popular terms and stores them in Redis for faster future autocomplete.

### Trie Update in Redis:
1. The new Trie generated by Spark is saved in Redis, ensuring that the most frequent search queries are readily available for autocomplete.

## 6. Architecture
The system consists of multiple interconnected components, each playing a distinct role in the overall flow. Below is a high-level architecture breakdown:

### 1. User Interaction:
- Users interact with the web application, typing search queries.
- The search queries are sent to the backend via an API request from the React frontend.

### 2. Backend Processing:
- **Redis Lookup**: The backend first checks Redis for a cached Trie. If found, it returns the autocomplete results immediately.
- **PostgreSQL Query**: If no matching Trie is found in Redis, the backend queries PostgreSQL for detailed player/team data.

### 3. Log Capture and Processing:
- **Apache Logs**: Every search interaction is logged.
- **Apache Spark**: Apache Spark periodically processes the logs, analyzing search patterns to identify frequently searched terms.
- **Redis Trie Update**: The output of Spark's log processing is used to update the Trie in Redis, ensuring frequently searched terms are cached for fast access.

### Key Benefits of the Optimized System:
- **Fast Query Responses**: Trie structures in Redis enable fast prefix matching, providing users with immediate autocomplete suggestions.
- **Efficient Data Access**: By caching frequently searched terms in Redis and keeping detailed data in PostgreSQL, the system balances speed and data integrity.
- **Adaptability**: Regular log processing with Apache Spark ensures that the system is always up-to-date with the latest user search trends, enhancing the accuracy of autocomplete suggestions.
- **Scalability**: The architecture is designed to scale efficiently by leveraging Redis and batching Apache logs for Trie updates, ensuring that performance remains high as the amount of data grows.


## 6. Conclusion: 
This optimized architecture leverages the strength of Redis for fast in-memory lookups, a trie data structure for efficient prefix matching, and Apache Spark for offline processing and updating. Together with React on the frontend and PostgreSQL for persistent storage, the system is designed to handle autocomplete functionality at scale with low latency, high efficiency, and great user experience.
