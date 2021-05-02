import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib
import requests
import Levenshtein
import json

data = []

files = glob.glob("data/*.json")

map = {}

for file in files:

    with open(file) as f:
        al = json.load(f)

    for obj in al:
        id = obj["objectID"]
        text = obj["text"]
        attribution = obj["attribution"]
        vol = obj["vol"]

        if attribution not in map:
            map[attribution] = {}

        if vol not in map[attribution]:
            map[attribution][vol] = {}

        map[attribution][vol][id] = text

result = {}

for attribution in map:

    vols = map[attribution]

    print(attribution)

    for vol in vols:

        print(vol)

        obj = vols[vol]

        for id in obj:

            print(id)

            result[id] = {}

            text = obj[id]

            for attribution2 in map:
                if attribution == attribution2:
                    continue



                vols2 = map[attribution2]

                for vol2 in vols2:
                    if vol != vol2:
                        continue

                    obj2 = vols2[vol2]

                    for id2 in obj2:
                        
                        text2 = obj2[id2]
                        
                        # ratio = 1 - Levenshtein.distance(text, text2) / max(len(text), len(text2)) * 1.00
                        ratio = Levenshtein.ratio(text, text2)

                        result[id][id2] = ratio

        # break

all = {}

for id in result:
    print(id, result[id])

    obj = result[id]

    arr = []

    score_sorted = sorted(obj.items(), key=lambda x:x[1], reverse=True)

    max = 20

    if len(score_sorted) < max:
        max = len(score_sorted)

    for i in range(0, max):

        obj2 = score_sorted[i]

        
        arr.append({
            "id" : obj2[0],
            "score" : obj2[1]
        })
        
        # arr.append(obj2[0])

    all[id] = arr

    

opath = "calc.json"

with open(opath, 'w') as outfile:
    json.dump(all, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))