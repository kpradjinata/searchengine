import os
import json
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup


class Indexer:
    def __init__(self):
        self.index = {}
        self.ps = PorterStemmer()

    def index_document(self, doc_id, tokens):
        # Parse the text to extract important words
        #important_words = self._extract_important_words(text)

        # Create the inverted index
        for i in range(len(tokens)):
            if tokens[i] not in self.index:
                self.index[tokens[i]] = {doc_id: 1}
            else:
                if doc_id not in self.index[tokens[i]]:
                    self.index[tokens[i]][doc_id] = 1
                else:
                    self.index[tokens[i]][doc_id] += 1

    def load(self, path):
        # Load the index from a file
        with open(path, "r") as f:
            return json.load(f)

    def extract_words(self, json):
        soup = BeautifulSoup(json["content"], "html.parser")
        # Tokenize the text
        tokens = word_tokenize(soup.get_text())
        # Stem the remaining words
        stemTokens = [self.ps.stem(token.lower()) for token in tokens if token.isalnum()]
        return stemTokens

    
