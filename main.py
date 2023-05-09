from indexer import Indexer
import os

def main():

    directory = 'searchengine/DEV' 
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    



    indexer = Indexer()

    for file in json_files:


        json = indexer.load(file)

        tokens = indexer.extract_words(json)

        indexer.index_document(json["url"], tokens)


    indexer.printindex()

if __name__ == "__main__":
    main()