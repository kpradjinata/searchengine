from indexer import Indexer
import os

def main():
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
        # if count == 40:
        #     break
        # count+=1
        json = indexer.load(file)
        tokens = indexer.extract_words(json)
        indexer.index_document(json["url"], tokens)
        print(json["url"],file)

    #print the master index
    indexer.printindex()
    print(indexer.failed)

if __name__ == "__main__":
    main()