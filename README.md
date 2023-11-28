# Search Engine Project

This project is a simple search engine that indexes and searches through a collection of documents. It includes a Flask web application for user interaction.

## Flask Web Application

The web application is built using Flask and provides a simple interface for users to input queries and retrieve relevant search results.

### Usage

1. Run the Flask application by executing the following command:

    ```bash
    python app.py
    ```

2. Access the application by navigating to [http://localhost:8000](http://localhost:8000) in your web browser.

3. Enter your search query and click the "Search" button to get the top results.

## Indexer

The indexer component is responsible for processing and indexing documents. It includes functionality for tokenization, stemming, and building an inverted index.

### Indexing Process

1. The `Indexer` class initializes an inverted index, a Porter Stemmer, and sets some configuration parameters.

2. The `index_document` method processes a document by tokenizing it, updating the inverted index, and calculating TF-IDF values.

3. The indexer writes the inverted index to disk when the index size reaches a specified threshold.

4. The `merge_indexes` method merges all the partial indexes into a final inverted index.

5. The `distribute_index` method distributes the final index into multiple parts based on the starting letter of terms.

6. The `write_report` method generates a report on the indexing process, including the number of indexed documents, invalid documents, final index size, and unique tokens.

### Usage

Run the indexing process by executing the following command:

```bash
python indexer.py
```
This will process a collection of JSON documents and build the inverted index.

### Query Processing
The query processing component includes a query function located in query.py. This function takes a user query, tokenizes and stems it, retrieves relevant documents, and ranks them based on TF-IDF values.

### Dependencies
- Flask
- NLTK
- BeautifulSoup
Install the required dependencies using the following command:

```bash
pip install Flask nltk beautifulsoup4
```
### Acknowledgments
This project was developed as part of a search engine experiment. Special thanks to the contributors and libraries used in the development process.

