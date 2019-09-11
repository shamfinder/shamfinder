import json
import numpy as np
import time




file = open("u12_similar_char_list.json","r")


dic_data = json.load(file)

sim_dic = dic_data.copy()

# Delete characters with black pixels less than 10 pixels 

for i in list(dic_data.keys()):
    if dic_data[i]["black_point"] < 10:
        del sim_dic[i]
    else:
        del_index = []
        for k in range(len(dic_data[i]["similar_char"])):
            if dic_data[i]["similar_char"][k]["black_point"] < 10:
                del_index.append(k)

        if len(del_index) != 0:
            sim_list = np.delete(sim_dic[i]["similar_char"],del_index).tolist()
            sim_dic[i]["similar_char"] = []
            sim_dic[i]["similar_char"].extend(sim_list)
            if len(sim_dic[i]["similar_char"]) == 0:
                del sim_dic[i]



fw = open("simchar.json","w")

json.dump(sim_dic, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



