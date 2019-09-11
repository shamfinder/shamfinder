import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont
from skimage.measure import compare_ssim,compare_psnr
import codecs
import time
import json
from multiprocessing import Pool
import os
import warnings

warnings.filterwarnings('ignore')


# embed one word in white image(50*50)

def create_str_img(demi):
    moji = chr(int(demi))
    size = 50, 50, 3
    white_img = np.zeros(size,dtype=np.uint8)
    white_img.fill(255)
    img_pil = Image.fromarray(white_img)
    draw = ImageDraw.Draw(img_pil)
    if int(demi) <= int("FFFF",16):
        font = ImageFont.truetype("unifont-12.0.01.ttf",16)
    else:
        font = ImageFont.truetype("unifont_upper-12.0.01.ttf",16)
    draw.text((25-8,25-8),moji,fill=(0,0,0),font=font)
    img = np.array(img_pil)
    return img






base_param=[]
start_read = time.time()

# This file shows codepoints(demical) that have unifont and they are contained draft
file = open("uf12_exist_draft_u12.txt","r")


# create dictionary (key:word ,value:image)
kk={}
for i in file:
    a = i.strip()
    base_param.append(a)
    image2 = create_str_img(a)
    kk[a] = image2
file.close()
end_read = time.time() - start_read


file = open("time_measure.txt","a")
file.write("store image time : "+str(end_read)+"\n")
file.flush()
file.close()


# round off
def round(x,d=2):
    p=10**d
    return (x*p*2+1)//2/p


# count black pixels 
def black_point_count(t_img):
    counter = 0
    zero = [255,255,255]
    for ii in t_img:
        for gg in ii:
            if (gg != zero).all():
                counter += 1
    return counter





# compare character images with brute force

def psnr_multi(i):

    img_list = []
    bp = chr(int(i))
    base_image = create_str_img(int(i))
    ba = hex(int(i))
    basepoint = str(ba).replace("0x","")
    basepoint = basepoint.zfill(4)
    basepoint = "U+" + basepoint
    base_black_point = black_point_count(base_image)

    # compare one image with all images
    for h in kk.keys():
        img = kk[h]

        # calculate PSNR
        value = compare_psnr(base_image,img)

        if value != float('inf'):
            value = round(value)
        if h != i:
            if value >= 23.7 or value == float('inf'):
                taisyo_black_point = black_point_count(img)
                pair=[]
                pair.append(h)
                pair.append(value)
                pair.append(taisyo_black_point)
                img_list.append(pair)

    # If there is an image similar to base image, output the file
    if len(img_list) > 0:
        result_str = ""
        for ik in img_list:
            cp = hex(int(ik[0]))
            codepoint = str(cp).replace("0x","")
            codepoint = codepoint.zfill(4)
            codepoint = "U+" + codepoint
            result_str = result_str+str(bp)+":"+str(chr(int(ik[0])))+":"+str(i)+":"+basepoint+":"+str(ik[0])+":"+codepoint+":"+str(ik[1])+":"+str(base_black_point)+":"+str(ik[2])+"\n"
        process_id = str(os.getpid())
        file = open("uf12_result_psnr/psnr_"+process_id+".txt","a") 
        file.write(result_str)
        file.flush()
        file.close()
    else:
        process_id = str(os.getpid())
        file = open("uf12_result_psnr/psnr_"+process_id+".txt","a")
        file.write(str(bp)+":"+str(i)+":"+basepoint+":not similar\n")
        file.flush()
        file.close()


start = time.time()

# run using 15 processes
with Pool(15) as p:
    p.map(psnr_multi,base_param)
end = time.time() - start

file = open("time_measure.txt","a")
file.write("compare time : "+ str(end)+"\n")
file.flush()
file.close()

