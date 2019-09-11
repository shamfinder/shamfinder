import json


with open("passive_dns_result.json","r") as pdr:
    data = json.load(pdr)

# key: domain, value: access
rec_count = {}

for i in data:
    for k in list(i.keys()):

        access_num = 0
        rec_count[k] = 0
        
        for a in i[k]:
            if a["rrtype"] == "A":
                access_num += a["count"]
        rec_count[k] = access_num


# sort & show 
import idna

for k, v in sorted(rec_count.items(), key=lambda x: -x[1]):
    print(str(idna.decode(k)) + ": " + str(v))
    
