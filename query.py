from nltk.stem import PorterStemmer
import json

def query(timesIndexed, uinput):
    # uinput = input("Query: ")
    uinput = uinput.split()

    ps = PorterStemmer()
    userArr = []
    for w in uinput:
        userArr.append(ps.stem(w))
    alphanum = '0123456789abcdefghijklmnopqrstuvwxyz'
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
                for doc, values in documents.items():
                    if doc not in totaltf:
                        totaltf[doc] = values[1]
                    else:
                        totaltf[doc] += values[1]


    top_five = sorted(totaltf.items(), key=lambda x: x[1], reverse=True)[:5]
    print(top_five)
    return top_five


# uinput = input("Query: ")               
            
# query(62, uinput)