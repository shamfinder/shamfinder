import xml.etree.ElementTree as et



tree = et.parse('result_nmap.xml')
root = tree.getroot()

allr = {}

# create dictionary : dic[domain] = {"80":status, "443":status}

for child in root:
    #print("-------")
    for mago in child:
        if mago.tag == "hostnames":
            for k in mago:
                g = k.attrib
                if g["type"] == "user":
                    key = g["name"]

        if mago.tag == "ports":
            dic = {}
            for v in mago:
                x = v.attrib
                dic[x["portid"]]= ""
                for w in v:
                    ss = w.attrib
                    if "state" in list(ss.keys()):
                        dic[x["portid"]] = ss["state"]
            allr[key] = dic


http = 0
https = 0
http_and_https = 0

p80 = []
p443 = []



# Detect open ports
for k in list(allr.keys()):
    if allr[k]["80"] == "open":
        http += 1
        p80.append(k)
    if allr[k]["443"] == "open":
        https += 1
        p443.append(k)
    if allr[k]["80"] == "open" and allr[k]["443"] == "open":
        http_and_https += 1


print("http :"+str(http))
print("https :"+str(https))
print("http and https :"+str(http_and_https))
total = list(set(p80 + p443))
print("total :"+str(len(total)))

