from indexer import Indexer


def main():
    indexer = Indexer()
    json = indexer.load("searchengine/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json")

    tokens = indexer.extract_words(json)

    indexer.index_document(json["url"], tokens)

    print(indexer.index)



if __name__ == "__main__":
    main()