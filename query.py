
from nltk.stem import PorterStemmer
import json


def query(timesIndexed, uinput):
    splitinput = uinput.split()
    ps = PorterStemmer()
    userArr = [ps.stem(w) for w in splitinput]

    totaltf = {}

    # Load index index file once
    with open("index_index.json", "r") as f:
        index_index = json.load(f)

    # Get relevant indexes
    relevant_indexes = [index_index[q] for q in userArr if q in index_index]

    # Use a set for faster document lookup
    relevant_documents = set()

    # Get relevant documents
    for index in relevant_indexes:
        with open(f"index{index}.json", "r") as f:
            index_data = json.load(f)
        for q in userArr:
            if q in index_data:
                relevant_documents.update(index_data[q].keys())

    # Calculate total term frequency for relevant documents
    for doc in relevant_documents:
        totaltf[doc] = sum(
            index_data[q][doc][1]
            for index in relevant_indexes
            for q in userArr
            if q in index_data and doc in index_data[q]
        )

    top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:20]
    return top_five                