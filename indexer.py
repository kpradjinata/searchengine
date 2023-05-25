import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import math


class Indexer:
    def __init__(self):
        self.index = {}
        self.ps = PorterStemmer()
        self.indexed_files = 0
        #keep as 9973
        self.MAXSIZE = 9973
        self.times_indexed = 0
        self.documents = 0
        self.invalid = 0

    def index_document(self, doc_id, tokens):
        # Create the inverted index
        for i in range(len(tokens)):
            if tokens[i] not in self.index:
                self.index[tokens[i]] = {doc_id: [1]}
            else:
                if doc_id not in self.index[tokens[i]]:
                    self.index[tokens[i]][doc_id] = [1]
                else:
                    # print(self.index[tokens[i]][doc_id][0])
                    self.index[tokens[i]][doc_id][0] += 1
            
            #tf
            tf = self.index[tokens[i]][doc_id][0]/len(tokens)
            idf = math.log(self.documents/(1+len(self.index[tokens[i]])))
            tfidf = tf*idf
            
            #value of values is a list of size 2 containing the tf
            if len(self.index[tokens[i]][doc_id]) == 1:
                #change to tfidf later
                self.index[tokens[i]][doc_id].append(tf)
            #update current tf value
            else:
                #change to tfidf later
                self.index[tokens[i]][doc_id][1] = tf


                    
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
                self.documents += 1 
                return stemTokens
            else:
                self.invalid += 1
                return []
        
        except RecursionError:
            self.invalid+=1
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
                    for doc_id, values in postings.items():
                        if doc_id not in final_index[term]:
                            final_index[term][doc_id] = values

        # Write the final index to disk
        with open("index_final.json", 'w') as f:
            json.dump(final_index, f)


    def write_report(self):
        with open("report.txt","w") as f:
            f.write(f"Documents Indexed: {self.documents}\n")
            f.write(f"Invalid Documents: {self.invalid}\n")
            index = self.load("index_final.json")
            f.write(f"Final Index Size KB: {int(sys.getsizeof(index)/1024)}\n")
            f.write(f"Unique Tokens: {len(index)}\n")
            f.write(f"TOTAL INDEX: \n\n{index}")
    
    # def add_idf(self):
    #     # get idf for all partial indexes
    #     for i in range(1, self.times_indexed+1):
    #         file_path = f"index{i}.json"
    #         with open(file_path, 'r') as f:
    #             index = json.load(f)
    #             for term, postings in index.items():
    #                 #get idf for each term
    #                 idf = math.log(self.documents/(1+len(postings)))

    #     #add idf to the final index
    #     idf = math.log(49000/(1+len()))



    
    def printindex(self):
        #print the master index
        print(self.index)
