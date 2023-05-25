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

    # retrun html lables of tokens
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
        
        #accept xml error maybe
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

    def distribute_index(self):
        file_path = f"index_final.json"
        merged_file = open(file_path, 'r')
        index = json.load(merged_file)

        #sort the index alphabetically, keeping the dic
        index = dict(sorted(index.items(), key=lambda x: x[0]))

        #split the index into 26 parts based on the first letter of the term
        #each part is a dictionary

        self.index = {}
        alphanum = '0123456789abcdefghijklmnopqrstuvwxyz'
        alpha_index = 0
        self.times_indexed = 0

        for term, postings in index.items():
            for posting, features in postings.items():
                idf = math.log(50000/(1+len(index[term])))
                index[term][posting][1] = index[term][posting][1]*idf



            if alpha_index == 36:
                self.index[term] = index[term]
            elif term[0] == alphanum[alpha_index]:
                self.index[term] = index[term]
            else:
                #offload, need to fix sorting
                # self.index = dict(sorted(self.index.items(), key=lambda x: x[1]))
                self.write_to_disk()
                self.index[term] = index[term]
                if alpha_index != 36:
                    alpha_index += 1
        # self.index = dict(sorted(self.index.items(), key=lambda x: x[1]))
        self.write_to_disk()





    
    def printindex(self):
        #print the master index
        print(self.index)