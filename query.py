from nltk.stem import PorterStemmer
import json
from concurrent.futures import ThreadPoolExecutor

def query(timesIndexed, uinput):
    splitinput = uinput.split()
    ps = PorterStemmer()
    userArr = [ps.stem(w) for w in splitinput]

    alphanum = '0123456789abcdefghijklmnopqrstuvwxyz'

    totaltf = {}

    def process_index(index_path, query_terms):
        index = load_index_from_disk(index_path)
        for term in query_terms:
            if term in index:
                documents = index[term]
                for doc, values in documents.items():
                    totaltf.setdefault(doc, 0)
                    totaltf[doc] += values[1]

    # Split query terms into groups for parallel processing
    query_groups = [[] for _ in range(len(alphanum) + 1)]
    for term in userArr:
        if term[0] not in alphanum:
            index = 37
        else:
            index = alphanum.index(term[0]) + 1
        query_groups[index].append(term)

    # Parallel query processing
    with ThreadPoolExecutor() as executor:
        futures = []
        for index, terms in enumerate(query_groups):
            if terms:
                index_path = f"index{index}.json"
                futures.append(executor.submit(process_index, index_path, terms))

    # Wait for all futures to complete
    for future in futures:
        future.result()

    top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:20]
    return top_five

def load_index_from_disk(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
