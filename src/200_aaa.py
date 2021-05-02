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
import csv

###########

files = glob.glob("data/*.json")

map = {}

for file in files:
    with open(file) as f:
        df = json.load(f)
        for obj in df:
            id = obj["objectID"]
            map[id] = obj # obj["page"]

###########

file = "calc3.json"

with open(file) as f:
    calc = json.load(f)

book_ids = ["京大本01", "京大本02", "NDL02", "NDL03", "NDL04"]

for book_id in book_ids:

    rows = []

    row = ["aaa"]
    rows.append(row)

    row = []
    row.append("Vol")
    row.append("Page")
    row.append("1")
    row.append("Score")
    rows.append(row)

    for page in calc:
        row = []

        obj2 = map[page]
        row.append(obj2["vol_str"])

        row.append(page)
        arr = calc[page][book_id]
        for obj in arr:
            page_id = obj["id"]
            row.append(map[page_id]["page"]) # page_id
            row.append(obj["score"])
        rows.append(row)

    with open('aaa/'+book_id+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)