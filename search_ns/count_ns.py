import json


with open("ns_record.json","r") as nrj:
    ns = json.load(nrj)



exist_ns = []

for k in ns:
    for i in list(k.keys()):
        if "Answer" in list(k[i].keys()):
            exist_ns.append(i)

print("domains that have ns record : "+str(len(exist_ns)))
