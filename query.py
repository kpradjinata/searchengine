
from nltk.stem import PorterStemmer
import json


def query(timesIndexed,uinput):
    #user query


            # splitinput = []
            # first = second = -1
            
            # #check if quotes exist in query
            # if uinput.count('"') == 2:
            #     for i in range(len(uinput)):
            #         if uinput[i] == '"':
            #             if first == -1:
            #                 first = i
            #             else:
            #                 second = i
                
            #     splitinput.append(uinput[first+1:second])

            #     splitinput += uinput[0:first].split()

            #     splitinput += uinput[second+1:].split()


            # else:
            #     splitinput = uinput.split()


    splitinput = uinput.split()
    # print(splitinput)
    ps = PorterStemmer()
    userArr = []
    #stem the query
    for w in splitinput:
        userArr.append(ps.stem(w))

    alphanum = '0123456789abcdefghijklmnopqrstuvwxyz'


    

    #index with the query
    totaltf = {}

    #get all indexes
    for q in userArr:
        if q[0] not in alphanum:
            index = 37
        else:
            index = alphanum.index(q[0])
            index += 1

        with open(f"index{index}.json", "r") as f:
            index = json.load(f)
        if q in index:
            #hard coded "of"
            if q!="of":
                documents = index[q]
                # documents = dict(list(index[q].items())[:20])
                for doc, values in documents.items():
                    if doc not in totaltf:
                        totaltf[doc] = values[1]
                    else:
                        totaltf[doc] += values[1]


    top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:20]
    print(totaltf)
    print(top_five)
    return top_five

query(1,"machine")
                
     
