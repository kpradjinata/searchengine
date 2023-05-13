import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup


class Indexer:
    def __init__(self):
        self.index = {}
        self.ps = PorterStemmer()
        self.indexed_files = 0
        self.MAXSIZE = 50
        self.times_indexed = 0

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
        self.indexed_files += 1

        # Write to disk if the index is too large
        if self.indexed_files >= self.MAXSIZE:
            self.write_to_disk()


    def write_to_disk(self):
        # Write the inverted index to a file
        self.times_indexed += 1
        with open(f"index{self.times_indexed}.json", "w") as f:
            json.dump(self.index, f)
        self.indexed_files = 0
        self.index = {}


    def load(self, path):
        # Load the index from a file
        with open(path, "r") as f:
            return json.load(f)

    def extract_words(self, json):

        #load the HTML
        try:
            #maybe keep if statement check if we need encoding
            # json["encoding"] == "utf-8" or json["encoding"] == "ascii") and 
            if bool(BeautifulSoup(json["content"], "html.parser").find()):
                soup = BeautifulSoup(json["content"], "html.parser")
                #fix broken HTML
                soup.prettify()
                # Tokenize the text
                tokens = word_tokenize(soup.get_text())

                # Stem the remaining words
                stemTokens = [self.ps.stem(token.lower()) for token in tokens if token.isalnum()]
                return stemTokens
            else:
                return []
        
        #accept xml error maybe
        except RecursionError:
            return []
        
    def merge_indexes(self):
        # Merge all index files on disk to obtain the final inverted index
        final_index = {}
        for i in range(1, self.times_indexed+1):
            file_path = f"index{i}.json"
            with open(file_path, 'r') as f:
                index = json.load(f)
                for term, postings in index.items():
                    if term not in final_index:
                        final_index[term] = {}
                    for doc_id, frequency in postings.items():
                        if doc_id not in final_index[term]:
                            final_index[term][doc_id] = frequency
                        else:
                            final_index[term][doc_id] += frequency
                

                

        # Write the final index to disk
        with open("index_final.json", 'w') as f:
            json.dump(final_index, f)



       
    
    def printindex(self):
        #print the master index
        print(self.index)
    
