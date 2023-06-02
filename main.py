from indexer import Indexer
import os
import sys

def main():
    #TODO 
    #DOC ID
    #COS SIMILARITY
    #HITS + PAGE RANKING
    #2-gram and 3-gram 
    #word position
    #OPEN AI

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
        # if count == 20020:
        #     break
        # count += 1
        json = indexer.load(file)
        print(json["url"],file, indexer.indexed_files)
        tokens = indexer.extract_words(json)
        indexer.index_document(json["url"], tokens)

    #write the remaining index to disk
    indexer.write_to_disk()

    #merge all files together
    indexer.merge_indexes()

    indexer.distribute_index()
    # indexer.createTFIDF()
    indexer.distribute_small_index()
    indexer.index_index()

    #print final report
    indexer.write_report()





if __name__ == "__main__":
    main()
    # indexer = Indexer()
    # indexer.distribute_index()






