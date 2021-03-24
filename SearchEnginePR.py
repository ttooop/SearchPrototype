#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   SearchEnginePR.py    
@Version    :   1.0
"""
import sys
import os
import numpy as np
import json
from scipy import sparse
import time
from bs4 import BeautifulSoup

data_path = "./data"
graph_path = os.path.join(data_path, "url_graph_file")
url_id_path = os.path.join(data_path, "url_id_mapping")
index_path = "./index.tsv"
html_path = os.path.join(data_path, "WebbSpamCorpus")

index = {}


def read_data(in_index, po_index):
    filenames = os.listdir(html_path)
    print(len(filenames))
    count = 0
    for file in filenames:
        file = os.path.join(html_path, file)
        count += 1
        if count % 1000 == 0:
            print(count)
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


class SearchEngine(object):
    def __init__(self):
        self.index = {}
        # id url
        self.in_index = {}
        # url id
        self.po_index = {}
        self.ranks = {}

    def index_build(self):
        with open(url_id_path, "r") as f:
            for line in f.readlines():
                l = line.split()
                id = int(l[0])
                url = l[1]
                self.in_index[id] = url
                self.po_index[url] = id
        # print("finish in and po index")
        if os.path.exists(index_path):
            file = open(index_path, 'r')
            js = file.read()
            self.index = json.loads(js)
            file.close()
        else:
            self.index = read_data(self.in_index, self.po_index)

    def data_initial(self):
        row = []
        col = []
        edges = 0
        with open(graph_path, 'r') as f:
            for line in f.readlines():
                l = list(map(eval, line.split()))
                if len(l) <= 1:
                    continue
                start = l[0]
                ends = l[1:]
                for end in ends:
                    edges += 1
                    row.append(start)
                    col.append(end)
        NODES = 263446
        EDGES = edges
        print(str(NODES), str(EDGES))
        return (sparse.csr_matrix(([True] * EDGES, (row, col)), shape=(NODES, NODES)))

    def PageRank(self, rate=0.85, epsilon=10 ** -10, max_iter=1e3):
        self.G = self.data_initial()
        n, _ = self.G.shape
        deg_out_rate = self.G.sum(axis=0).T / rate
        ranks = np.ones((n, 1)) / n
        count = 0
        flag = True
        while flag and count < max_iter:
            count += 1
            with np.errstate(divide='ignore'):
                newRank = self.G.dot((ranks / deg_out_rate))
            newRank += (1 - newRank.sum()) / n
            if np.linalg.norm(ranks - newRank, ord=1) <= epsilon:
                flag = False
            ranks = newRank
        for i in range(n):
            self.ranks[i] = ranks[i][0, 0]
        return (self.ranks, count)

    def search(self, keyword, rank):
        dic = {}
        res = []
        if keyword is None or keyword == "":
            return []
        for key in keyword.split():
            if key not in self.index:
                continue
            for e in self.index[key]:
                if str(e) in rank:
                    dic[rank[str(e)]] = self.in_index[e]
        key = self._quicksort((list(dic.keys())))
        for i in key:
            res.append(dic[i])
        return res

    def _quicksort(self, l):
        if len(l) <= 1:
            return l
        pivot = l[int(len(l) / 2)]
        smaller = []
        bigger = []
        equal = []
        for e in l:
            if e < pivot:
                smaller.append(e)
            elif e == pivot:
                equal.append(e)
            else:
                bigger.append(e)
        return self._quicksort(bigger) + equal + self._quicksort(smaller)


if __name__ == '__main__':
    print("welcome to my search engine!")
    print("Starting initial Search Engine......")
    se = SearchEngine()
    print("Finished initialization.")
    print("Starting building index from htmls......")
    se.index_build()
    print("Finished building index.")
    print("Starting calculate PageRank......")
    rank_path = "./rank.tsv"
    rank = {}
    if os.path.exists(rank_path):
        file = open(rank_path, 'r')
        js = file.read()
        rank = json.loads(js)
        # print(rank)
        file.close()
    else:
        startTime = time.time()
        rank, count = se.PageRank()
        print("pagerank iter elapsed time: ", time.time() - startTime)
        print("iterations:{0}".format(count))
        pr_res = json.dumps(rank)

        f = open(rank_path, 'w')
        f.write(pr_res)
        f.close()
    print("Finished calculate PageRank")
    keyword = input("Please input your search word: ")
    print("======Start searching======")
    res = se.search(keyword, rank)
    print("Search result is: ")
    print(res)
