import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib
import requests

data = []

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
                koui[member_id] = labels[1].split("p.")[1].zfill(4)
            

    path = "/Users/nakamurasatoru/git/d_genji/genji_curation/docs/iiif/kuronet/"+str(vol).zfill(2)+".json"

    curationUrl = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/021_taisei_all/"+str(vol).zfill(2)+".json"

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
            images[canvas["@id"]] = canvas["thumbnail"]["@id"]

        label = selection["within"]["label"]

        map = {}

        for member in members:

            member_id = member["@id"]

            member_id_spl = member_id.split("#xywh=")

            canvasId = member_id_spl[0]

            page = int(canvasId.split("canvas/p")[1])
            
            hash = hashlib.md5(canvasId.encode('utf-8')).hexdigest()

            if canvasId not in map:
                map[canvasId] = {
                    "objectID" : hash,
                    "attribution" : "東京大学",
                    "target" : "東大本",
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

opath = "data/utokyo.json"

with open(opath, 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
