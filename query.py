
from nltk.stem import PorterStemmer
import json

def query(timesIndexed):
    #user query
    while True:
        uinput = input("Query (x to quit): ")
        if uinput == "x":
            break
        else:
            uinput = uinput.split()

            ps = PorterStemmer()
            userArr = []
            #stem the query
            for w in uinput:
                userArr.append(ps.stem(w))

            #index with the query
            totaltf = {}

            #get all indexes with the query
            for i in range(1,timesIndexed+1):
                with open(f"index{i}.json", "r") as f:
                    index = json.load(f)
                    for q in userArr:
                        if q in index:
                            #hard coded "of"
                            if q!="of":
                                documents = index[q]
                                for doc, values in documents.items():
                                    if doc not in totaltf:
                                        totaltf[doc] = values[0]
                                    else:
                                        totaltf[doc] += values[0]


            #top 5 urls
            top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:5]
            print(top_five)


                
     
query(1)
