from indexer import Indexer
import os

def main():
    #TODO DISK
    #CHECK ENCODING
    #CHECK ERRORS
    #FIGURE OUT DOCID
    #OUTPUT TO FILE
    #CREATE PDF

    #contains the json files
    directory = 'searchengine/DEV' 
    json_files = []
    count = 0

    #get all the json files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    
    indexer = Indexer()

    #index all the json files
    for file in json_files:
        if count ==100:
            break
        count += 1
        json = indexer.load(file)
        print(json["url"],file, indexer.indexed_files)
        tokens = indexer.extract_words(json)
        indexer.index_document(json["url"], tokens)

    #print the master index
    indexer.merge_indexes()
    # indexer.printindex()
    # print(indexer.failed)

if __name__ == "__main__":
    main()