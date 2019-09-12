import string
import json
import csv
import tldextract
import time
from collections import defaultdict
import idna



# detect homograph idn from this file
file = open("uniq_idn_io_and_zone.txt","r")



# decode idn
target_idn = defaultdict(list)

for i in file:
    a = i.strip().replace(".com","")
    try:
        ddlio = idna.decode(a)
        target_idn[len(ddlio)].append(ddlio)
    except:
        try:
            dlio = a.encode("utf-8")
            ddlio = dlio.decode("idna")
            target_idn[len(ddlio)].append(ddlio)
        except:
            with open("simchar_only/decode_failed_idn.txt","a") as cdic:
                #with open("confusable_only/decode_failed_idn.txt","a") as cdic:
                #with open("simchar_confusable/decode_failed_idn.txt","a") as cdic:
                cdic.write(a+"\n")


file.close()



# extract 10k domains that have ".com"

alexa_target = []
with open("top-1m.csv","r") as al:
    ax = csv.reader(al)
    for i in ax:
        ext = tldextract.extract(i[1])
        if "com" == ext.suffix:
            if ext.domain not in alexa_target:    
                alexa_target.append(ext.domain)

        if len(alexa_target) == 10000:
            break


with open("simchar_only/target_alexa.txt","w") as tal:
    #with open("confusable_only/target_alexa.txt","w") as tal:
    #with open("simchar_confusable/target_alexa.txt","w") as tal:
    for i in alexa_target:
        tal.write(str(i)+"\n")


sim_dic = defaultdict(list)

alp = string.ascii_lowercase+string.digits



# simchar_only
# simchar_confusable

with open("../simchar/simchar.json","r") as sim:
    data = json.load(sim)

for i in alp:
    sim_dic[i] += [ ew["char"] for ew in data[i]["similar_char"] if ew["psnr"] >= 27.96 ]



#confusable_only
#simchar_confusable

'''
with open("confusables_v12-1_in_draft.json","r") as fhe:
    cfff = json.load(fhe)

for i in alp:
    if i in list(cfff.keys()):
        sim_dic[i] += [ okk["char"] for okk in cfff[i] ]
'''


#simchar_confusable
#for i in list(sim_dic.keys()):
    #sim_dic[i] = list(set(sim_dic[i]))


result_dic = defaultdict(list)


# compare reference domain with idn 

def detect_homo(i,k):
    flag = 0
    for x in range(len(i)):

        if i[x] == k[x]:
            continue
        elif k[x] in sim_dic[i[x]]:
            continue
        else:
            flag = 1
            break

    if flag == 0:
        result_dic[i].append(k)



start = time.time()

ccc = 1

for i in alexa_target:

    with open("simchar_only/log_homograph_detect.txt","a") as lll:
        #with open("confusable_only/log_homograph_detect.txt","a") as lll:
        #with open("simchar_confusable/log_homograph_detect.txt","a") as lll:
        lll.write(str(ccc)+" : "+i+"\n")

    #compare reference domain with same string length idn 
    for k in target_idn[len(i)]:
            detect_homo(i,k)
    ccc += 1



spend_time = time.time() - start


with open("simchar_only/result_detect_simchar.json","w") as rh:
    #with open("confusable_only/result_detect_confusable.json","w") as rh:
    #with open("simchar_confusable/result_detect_simchar_confusable.json","w") as rh:
    json.dump(result_dic,rh,ensure_ascii=False,indent = 4)


file = open("simchar_only/total_time.txt","a")
#file = open("confusable_only/total_time.txt","a")
#file = open("simchar_confusable/total_time.txt","a")
file.write("total time is "+str(spend_time)+"\n")
file.flush()
file.close()




