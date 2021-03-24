#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pagerankwithNX.py    
@Author  :   wangyawen
@Modify Time :  2021/3/23 下午12:25
@Version    :   1.0
"""
import argparse
import time
import networkx as nx
import os
import json

data_path = "./data"
graph_path = os.path.join(data_path, "url_graph_file")


def buildGFromFile(G):
    with open(graph_path) as f:
        for line in f.readlines():
            l = list(map(eval, line.split()))
            if len(l) <= 1:
                continue
            start = l[0]
            ends = l[1:]
            for end in ends:
                G.add_edge(start, end)
    return G


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-rate', type=float, default=0.15,
                        help='walk out rate, the probability of a man opening a new web')
    parser.add_argument('-num_iter', type=int, default=1e3, help='max iterations of pageRank')
    parser.add_argument('-eps', type=float, default=1e-10, help='stop condition, if loss < eps then stop iteration')
    parser.add_argument('-type', type=str, default='scipy',
                        help='pagerank algorithm type. naive for pagerank(), numpy for pagerank_numpy(), scipy for pagerank_scipy(), google for google_matrix()')
    arg = parser.parse_args()
    print("pagerank begins!")

    begintime = time.time()
    G = nx.DiGraph()
    G = buildGFromFile(G)
    print("building Graph elapsed time: ", time.time() - begintime)
    if arg.type == 'naive':
        beginTime = time.time()
        PageRankResult = nx.pagerank(G, alpha=1 - arg.rate, max_iter=int(arg.num_iter), tol=arg.eps)
        print("PageRank elapsed time: ", time.time() - beginTime)
    elif arg.type == 'numpy':
        beginTime = time.time()
        PageRankResult = nx.pagerank_numpy(G, alpha=1 - arg.rate, max_iter=int(arg.num_iter), tol=arg.eps)
        print("pagerank_numpy elapsed time: ", time.time() - beginTime)
    elif arg.type == 'scipy':
        beginTime = time.time()
        PageRankResult = nx.pagerank_scipy(G, alpha=1 - arg.rate)
        print("PageRank_scipy elapsed time: ", time.time() - beginTime)
    elif arg.type == 'google':
        beginTime = time.time()
        PageRankResult = nx.google_matrix(G, alpha=1 - arg.rate)
        print("Google Matrix elapsed time: ", time.time() - beginTime)

    pr_res = json.dumps(PageRankResult)

    f = open('rank_save.tsv', 'w')
    f.write(pr_res)
    f.close()
