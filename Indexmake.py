#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   Indexmake.py    
"""
import tarfile
import os
import json
from bs4 import BeautifulSoup

from SearchEnginePR import SearchEngine

data_path = "./data"
html_path = os.path.join(data_path, "WebbSpamCorpus")

index = {}


def read_data(in_index, po_index):
    # tarf = tarfile.open(html_path)
    filenames = os.listdir(html_path)
    print(len(filenames))
    count = 0
    for file in filenames:
        file = os.path.join(html_path, file)
        count += 1
        if count % 1000 == 0:
            print(count)
        if count == 189001:
            break
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            url = f.readline()
            start = url.find("http://")
            url = url[start:-5]
            if url not in po_index:
                continue
            idx = po_index[url]
            try:
                content = f.read()
            except:
                continue
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string if soup.title is not None else ""
            if title is not None:
                for t in title.split():
                    if t is None:
                        continue
                    if t in index:
                        index[t].append(idx)
                    else:
                        index[t] = [idx]
            words = soup.find_all("a")
            for w in words:
                word = w.string
                if word is None or word == "":
                    continue
                for t in word.split():
                    if t is None:
                        continue
                    if t in index:
                        index[t].append(idx)
                    else:
                        index[t] = [idx]
    res = json.dumps(index)
    f = open("index.tsv", 'w')
    f.write(res)
    f.close()
    return index


if __name__ == '__main__':
    se = SearchEngine()
    se.index_build()
    read_data(se.in_index, se.po_index)
