from nltk.stem import PorterStemmer
import json

def query(timesIndexed):
    uinput = input("Query: ")
    uinput = uinput.split()

    ps = PorterStemmer()
    userArr = []
    for w in uinput:
        userArr.append(ps.stem(w))

    totaltf = {}

    #get all indexes
    for i in range(1,timesIndexed-1):
        with open(f"index{i}.json", "r") as f:
            index = json.load(f)
            for q in userArr:
                if q in index:
                    #hard coded "of"
                    if q!="of":
                        documents = index[q]

                        for doc, values in documents.items():
                            if doc not in totaltf:
                                totaltf[doc] = values[1]
                            else:
                                totaltf[doc] += values[1]

                                
    top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:5]
    print(top_five)


                
            

query(14)