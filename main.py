from indexer import Indexer
import os
import sys

def main():
    #TODO 
    #CHECK ENCODING
    #CHECK ERRORS
    #FIGURE OUT DOCID
    #OUTPUT TO FILE
    #CREATE PDF

    #contains the json files
    directory = 'searchengine/DEV' 
    json_files = []
    # count = 0

    #get all the json files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    
    indexer = Indexer()

    #index all the json files
    for file in json_files:
        # if count ==1000:
        #     break
        # count += 1
        json = indexer.load(file)
        print(json["url"],file, indexer.indexed_files)
        tokens = indexer.extract_words(json)
        indexer.index_document(json["url"], tokens)

    #print the master index
    indexer.merge_indexes()

    print(indexer.documents)
    print(indexer.invalid)
    with open("report.txt","r") as f:
        f.write(f"Documents: {indexer.documents}\n")
        f.write(f"Invalid: {indexer.invalid}\n")
        index = indexer.load("index_final.json")
        # print(sys.getsizeof(index))
        f.write(f"Final Index Size: {sys.getsizeof(index)}\n")

    #get size of final index

    # with open(, 'r') as f:


    # indexer.printindex()
    # print(indexer.failed)

if __name__ == "__main__":
    main()