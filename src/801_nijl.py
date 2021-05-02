import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib
import requests

config = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/info.json").json()

selections = config["selections"]

config_map = {}

for selection in selections:
    members = selection["members"]

    for member in members:
        label = member["label"]

        for m in member["metadata"]:
            if m["label"] == "vol":
                config_map[m["value"]] = label

data = []

for vol in range(1, 55):
    print(vol)

    index = 1

    koui_url = "https://genji.dl.itc.u-tokyo.ac.jp/data/vol/"+str(vol).zfill(2)+"/curation.json"
    k = requests.get(koui_url).json()

    koui = {}

    selections = k["selections"]

    for selection in selections:
        for member in selection["members"]:
            member_id = member["@id"]
            labels = member["label"].split(" ")
            if labels[0] == "校異源氏物語":
                koui[member_id] = int(labels[1].split("p.")[1])

    path = "/Users/nakamurasatoru/git/d_genji/genji_curation/docs/iiif/nijl_kuronet/"+str(vol).zfill(2)+".json"

    curationUrl = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl_kuronet_taisei_all/"+str(vol).zfill(2)+".json"

    with open(path) as f:
        curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        manifest = selection["within"]["@id"]

        m_data = requests.get(manifest).json()

        canvases = m_data["sequences"][0]["canvases"]

        images = {}

        for canvas in canvases:
            images[canvas["@id"]] = canvas["images"][0]["resource"]["service"]["@id"] + "/full/200,/0/default.jpg"

        label = selection["within"]["label"]

        map = {}

        for member in members:

            member_id = member["@id"]

            member_id_spl = member_id.split("#xywh=")

            canvasId = member_id_spl[0]

            page = int(canvasId.split("canvas/")[1])
            
            hash = hashlib.md5(canvasId.encode('utf-8')).hexdigest()

            if canvasId not in map:
                map[canvasId] = {
                    "objectID" : hash,
                    "attribution" : "国文学研究資料館",
                    "target" : "湖月抄（国文研所蔵）",
                    "vol_str" : '{} {}'.format(str(vol).zfill(2), config_map[vol]),
                    "vol" : vol,
                    "label": [],
                    "image" : images[canvasId],
                    "work" : label,
                    "page" : page,
                    "pos" : index,
                    "curation" : curationUrl,
                    "manifest" : manifest,
                    "canvas" : canvasId,
                    "koui" : [],
                    "type" : "コマ"
                }

                index += 1

            map[canvasId]["label"].append(member["label"])

            if member_id in koui:
                map[canvasId]["koui"].append(koui[member_id])

        for canvas in map:

            obj = map[canvas]
            obj["text"] = "\n".join(obj["label"])

            data.append(obj)

    # break

opath = "data/nijl.json"

with open(opath, 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
