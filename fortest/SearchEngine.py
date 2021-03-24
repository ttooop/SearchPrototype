#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   SearchEngine.py    
@Version    :   1.0
"""
import sys
import os
import numpy as np
import json

data_path = "./data"
graph_path = os.path.join(data_path, "url_graph_file")
G_path = os.path.join(data_path, "graph.csv")
M_path = os.path.join(data_path, "map.csv")


class SearchEngine(object):
    def __init__(self):
        self.G = np.zeros((263446, 263446), np.float32)
        self.M = np.zeros((263446, 263446), np.float32)
        self.N = 263446
        self.index = {}
        self.ranks = []
        self.graph = self.init_graph()

    def init_graph(self):
        graph = {}
        print("Starting building link graph......")
        with open(graph_path, 'r') as f:
            line = f.readlines()
            for l in line:
                l_ = list(map(eval, l.split()))
                key = l_[0]
                value = l_[1:]
                graph[key] = value
                for j in value:
                    self.G[key][j] = 1
            print("Initial graph successfully")
        if not os.path.exists(G_path):
            np.savetxt(G_path, self.G, delimiter=',', fmt='%d')
        return graph

    def GtoM(self):
        for i in range(self.N):
            D_i = sum(self.G[i])
            if D_i == 0:
                continue
            for j in range(self.N):
                self.M[j][i] = self.G[i][j] / D_i

    def PageRank(self, T=10, eps=1e-6, beta=0.8):
        if os.path.exists(M_path):
            self.M = np.loadtxt(open(M_path, "rb"), delimiter=",", skiprows=0)
            print(self.M.shape)
        else:
            self.M = self.G / self.G.sum(axis=0)
            np.savetxt(M_path, self.M, delimiter=',')
        # self.GtoM()
        R = np.ones(self.N) / self.N
        R.astype(np.float32)
        teleport = np.ones(self.N) / self.N
        teleport.astype(np.float32)
        print("Starting calculate rank....")
        for time in range(T):
            print("loop " + str(time))
            R_new = beta * np.dot(self.M, R) + (1 - beta) * teleport
            if np.linalg.norm(R_new - R) < eps:
                break
            R = R_new.copy()
        print("Finished calculating ")
        np.savetxt('rank_save.tsv', R, newline='\t', delimiter='\t')

    def compute_ranks(self, k):
        d = 0.8
        numloops = 5
        ranks = {}
        npages = len(self.graph)
        for page in self.graph:
            ranks[page] = 1.0 / npages

        print("Starting calculate rank....")
        for i in range(0, numloops):
            print("loop " + str(i))
            newranks = {}
            for page in self.graph:
                newrank = (1 - d) / npages
                for node in self.graph:
                    if page in self.graph[node]:
                        if not self._is_reciprocal_link(node, page, k):
                            newrank = newrank + d * ranks[node] / len(self.graph[node])
                newranks[page] = newrank
            ranks = newranks

        print("Finished calculating ")
        self.ranks = ranks
        np.savetxt('rank_save.tsv', ranks, newline='\t', delimiter='\t')
        return ranks

    def _is_reciprocal_link(self, source, destination, k):
        if k == 0:
            if source == destination:
                return True
            return False
        if source in self.graph[destination]:
            return True
        for node in self.graph[destination]:
            if self._is_reciprocal_link(source, node, k - 1):
                return True
        return False

    def ordered_search(self, index, ranks, keyword):
        dic = {}
        res = []
        for e in index[keyword]:
            if e in ranks:
                dic[ranks[e]] = e
        key = self._quicksort(list(dic.keys()))
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
    se = SearchEngine()
    # rank = se.compute_ranks(0)
    rank = se.PageRank()
