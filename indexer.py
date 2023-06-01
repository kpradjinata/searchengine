import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import math
import sys


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
            
            #calculate tfidf here
            tf = self.index[tokens[i]][doc_id][0]
            idf = math.log(self.documents/(1+len(self.index[tokens[i]])))
            tfidf = tf * idf
            
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

                # Get the important tags
                important_tags = soup.find_all(['h1', 'strong', 'b'])
                for tag in important_tags:
                    if '<h1' in str(tag):
                        words = tag.get_text().split()
                        tokens += (words * 9)
                    elif '<h2' in str(tag):
                        words = tag.get_text().split()
                        tokens += (words * 4)
                    elif 'h3' in str(tag):
                        words = tag.get_text().split()
                        tokens += (words * 3)
                    elif 'strong' in str(tag):
                        words = tag.get_text().split()
                        tokens += (words * 2)
                    elif 'b' in str(tag):
                        words = tag.get_text().split()
                        tokens += (words)
                # print("ASDHAISDUHASIUDHAISUDHA")

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
                idf = math.log(self.documents/(1+len(index[term])))
                index[term][posting][1] = index[term][posting][1]*idf

            index[term] = dict(sorted(index[term].items(),key=lambda x:x[1][1],reverse = True)[:20])


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


    def distribute_small_index(self):
        file_path = f"index_final.json"
        merged_file = open(file_path, 'r')
        index = json.load(merged_file)

        #sort the index alphabetically, keeping the dic
        index = dict(sorted(index.items(), key=lambda x: x[0]))
        max_size = 300

        size_of_each_file = len(index)/max_size

        #split the index into 400 parts
        #each part is a dictionary

        self.index = {}
        alpha_index = 0
        self.times_indexed = 0

        for term, postings in index.items():
            #calculate tfidf
            for posting, features in postings.items():
                #make sure its self.documents
                idf = math.log(self.documents/(1+len(index[term])))
                index[term][posting][1] = index[term][posting][1]*idf
            #sort the postings by tfidf, save top 20
            index[term] = dict(sorted(index[term].items(),key=lambda x:x[1][1],reverse = True)[:20])

            #split the index into 400 parts
            #each part is a dictionary
            if len(self.index) < size_of_each_file:
                self.index[term] = index[term]
            else:
                #offload
                self.write_to_disk()
                self.index[term] = index[term]
        self.write_to_disk()

    def index_index(self):
        #index the index
        #index is a dictionary
        #key is the term
        #value is the dictionary of docid and tfidf
        #index_index is a dictionary
        #key is the term
        #value is a position of the term within the index
        max_size = 300
        index_index = {}
        filepath = "index_index.json"
        for i in range(1, max_size+1):
            file_path = f"index{i}.json"
            with open(file_path, 'r') as f:
                index = json.load(f)
                for term, postings in index.items():
                    if term not in index_index:
                        index_index[term] = i

        with open(filepath, "w") as f:
            json.dump(index_index, f)

    
    def printindex(self):
        #print the master index
        print(self.index)
