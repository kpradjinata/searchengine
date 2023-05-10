import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup


class Indexer:
    def __init__(self):
        self.index = {}
        self.ps = PorterStemmer()
        self.failed = 0
        self.encodes = []

    def index_document(self, doc_id, tokens):
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

        #load the HTML
        if (json["encoding"] == "utf-8" or json["encoding"] == "ascii") and bool(BeautifulSoup(json["content"], "html.parser").find()):
            soup = BeautifulSoup(json["content"], "html.parser")
            #fix broken HTML
            soup.prettify()
        else:
            self.failed += 1
            self.encodes.append(json["encoding"])
            return []



        # Tokenize the text
        tokens = word_tokenize(soup.get_text())

        # Stem the remaining words
        stemTokens = [self.ps.stem(token.lower()) for token in tokens if token.isalnum()]

        return stemTokens
    
    def printindex(self):
        #print the master index
        print(self.index)
    
