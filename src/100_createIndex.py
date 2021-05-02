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

with open("nuxt.json") as f:
    df = json.load(f)

facets = {
    "vol_str" : {}
}

index = {}

for objectID in df:
    item = df[objectID]

    if "text" in item:
        description = item["text"].replace("\n", "").strip()
    else:
        description = ""

    if description != "":

        if description not in index:
            index[description] = []

        index[description].append(objectID)

    for key in facets:


        if key in item:
            facet = facets[key]
            values = item[key]

            if type(values) is str:
                values = [values]

            for value in values:

                if value == "":
                    continue

                if value not in facet:
                    facet[value] = []
                facet[value].append(objectID)


opath = "../static/data/docs.json"

with open(opath, 'w') as outfile:
    json.dump(df, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))

with open("../static/data/facets.json", 'w') as outfile:
    json.dump(facets,  outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))

with open("../static/data/index.json", 'w') as outfile:
    json.dump(index,  outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))