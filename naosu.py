import json


with open("confusables_v12-1_in_draft.json","r") as cv:
    data = json.load(cv)


for k in list(data.keys()):
    for x in data[k]:
        x["decimal"] = x["demical"]
        del x["demical"]



fw = open("confusables2.json","w")

json.dump(data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))        
