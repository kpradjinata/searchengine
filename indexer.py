import os
import json
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class Indexer:
    def __init__(self):
        self.index = defaultdict(list)
        self.ps = PorterStemmer()

    def index_document(self, doc_id, text):
        # Parse the text to extract important words
        important_words = self._extract_important_words(text)

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stop words and stem the remaining words
        terms = [self.ps.stem(token.lower()) for token in tokens if token.isalnum()]

        # Create the inverted index
        for i, term in enumerate(terms):
            self.index[term].append((doc_id, i, term in important_words))

    def save(self, path):
        # Save the index to a file
        with open(path, "w") as f:
            json.dump(self.index, f)

    def load(self, path):
        # Load the index from a file
        with open(path, "r") as f:
            self.index = json.load(f)

    def _extract_important_words(self, text):
        # Extract important words from the text
        important_words = set()

        # Extract words in bold
        important_words.update(re.findall(r"<b>(.*?)</b>", text))

        # Extract words in headings
        important_words.update(re.findall(r"<h\d>(.*?)</h\d>", text))

        # Extract words in titles
        if "<title>" in text:
            title_start = text.index("<title>") + len("<title>")
            title_end = text.index("</title>")
            title = text[title_start:title_end]
            important_words.update(word_tokenize(title))

        return important_words
