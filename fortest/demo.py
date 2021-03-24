#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py    
@Author  :   wangyawen
@Modify Time :  2021/3/22 下午11:52
@Version    :   1.0
"""


class Search_engine(object):

    def __init__(self):
        # 倒排索引：词-》URL
        self.index = {}
        self.graph = {}
        # Examples of website content
        self.cache = {
            'http://udacity.com/cs101x/urank/index.html': """<html>
                                                        <body>
                                                        <h1>dave's cooking algorithms</h1>
                                                        <p>
                                                        here are my favorite recipies:
                                                        <ul>
                                                        <li> <a href="http://udacity.com/cs101x/urank/hummus.html">hummus recipe</a>
                                                        <li> <a href="http://udacity.com/cs101x/urank/arsenic.html">world's best hummus</a>
                                                        <li> <a href="http://udacity.com/cs101x/urank/kathleen.html">kathleen's hummus recipe</a>
                                                        </ul>
                                                        for more expert opinions, check out the
                                                        <a href="http://udacity.com/cs101x/urank/nickel.html">nickel chef</a>
                                                        and <a href="http://udacity.com/cs101x/urank/zinc.html">zinc chef</a>.
                                                        </body>
                                                        </html>
                                                        """,

            'http://udacity.com/cs101x/urank/zinc.html': """<html>
                                                        <body>
                                                        <h1>the zinc chef</h1>
                                                        <p>
                                                        i learned everything i know from
                                                        <a href="http://udacity.com/cs101x/urank/nickel.html">the nickel chef</a>.
                                                        </p>
                                                        <p>
                                                        for great hummus, try
                                                        <a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.
                                                        </body>
                                                        </html>
                                                        """,

            'http://udacity.com/cs101x/urank/nickel.html': """<html>
                                                        <body>
                                                        <h1>the nickel chef</h1>
                                                        <p>
                                                        this is the
                                                        <a href="http://udacity.com/cs101x/urank/kathleen.html">
                                                        best hummus recipe!
                                                        </a>
                                                        </body>
                                                        </html>
                                                        """,

            'http://udacity.com/cs101x/urank/kathleen.html': """<html>
                                                        <body>
                                                        <h1>
                                                        kathleen's hummus recipe
                                                        </h1>
                                                        <p>
                                                        <ol>
                                                        <li> open a can of garbonzo beans.
                                                        <li> crush them in a blender.
                                                        <li> add 3 tablesppons of tahini sauce.
                                                        <li> squeeze in one lemon.
                                                        <li> add salt, pepper, and buttercream frosting to taste.
                                                        </ol>
                                                        </body>
                                                        </html>
                                                        """,

            'http://udacity.com/cs101x/urank/arsenic.html': """<html>
                                                        <body>
                                                        <h1>
                                                        the arsenic chef's world famous hummus recipe
                                                        </h1>
                                                        <p>
                                                        <ol>
                                                        <li> kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">nickel chef</a>.
                                                        <li> force her to make hummus for you.
                                                        </ol>
                                                        </body>
                                                        </html>
                                                        """,

            'http://udacity.com/cs101x/urank/hummus.html': """<html>
                                                        <body>
                                                        <h1>
                                                        hummus recipe
                                                        </h1>
                                                        <p>
                                                        <ol>
                                                        <li> go to the store and buy a container of hummus.
                                                        <li> open it.
                                                        </ol>
                                                        </body>
                                                        </html>
                                                        """,
        }

    ## web crawling
    def crawl_web(self, seed):
        tocrawl = [seed]
        crawled = []
        while tocrawl:
            page = tocrawl.pop()
            if page not in crawled:
                # 获取缓存cache数据,根据url获得page内容
                content = self._get_page(page)
                # 将内容加入索引
                self._add_page_to_index(self.index, page, content)
                # 获得该URL界面中的指向网页
                outlinks = self._get_all_links(content)
                # 连接 向tocrawl中添加外链
                self._union(tocrawl, outlinks)
                # 创建图
                self.graph[page] = outlinks
                crawled.append(page)
        return self.index, self.graph

    def _get_page(self, url):
        if url in self.cache:
            return self.cache[url]
        return ""

    def _add_page_to_index(self, index, url, content):
        # content 分割
        words = content.split()
        for word in words:
            # 对每一个词
            if word in index:
                # 如果词在index中，在索引中加上这个url
                index[word].append(url)
            else:
                # 如果索引没有这个词，则创建索引，并加入url
                index[word] = [url]

    def _get_next_target(self, page):
        start_link = page.find('<a href=')
        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote

    def _get_all_links(self, page):
        # 获得该URL界面中的指向网页
        links = []
        while True:
            url, endpos = self._get_next_target(page)
            if url:
                links.append(url)
                page = page[endpos:]
            else:
                break
        return links

    def _union(self, a, b):
        for e in b:
            if e not in a:
                a.append(e)

    ## look up the keyword in index
    def lookup(self, index, keyword):
        if keyword not in index:
            return index[keyword]
        return None

    ## compute page rank using graph
    def compute_ranks(self, graph, k):
        d = 0.8
        numloops = 2
        ranks = {}
        npages = len(graph)
        for page in graph:
            ranks[page] = 1.0 / npages

        for i in range(0, numloops):
            newranks = {}
            for page in graph:
                newrank = (1 - d) / npages
                for node in graph:
                    if page in graph[node]:
                        if not self._is_reciprocal_link(graph, node, page, k):
                            newrank = newrank + d * ranks[node] / len(graph[node])
                newranks[page] = newrank
            ranks = newranks
        return ranks

    def _is_reciprocal_link(self, graph, source, destination, k):
        if k == 0:
            if source == destination:
                return True
            return False
        if source in graph[destination]:
            return True
        for node in graph[destination]:
            if self._is_reciprocal_link(graph, source, node, k - 1):
                return True
        return False

    ## sort ascending
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


## not use
#    def remove_tags(self, string):
#        start, end = 0, 0
#        while True:
#            start = string.find('<')
#            if start == -1:
#                return string.split()
#            end = string.find('>', start)
#            string = string[:start] + ' ' + string[end+1:]

#    def record_user_click(self,index,keyword,url):
#        return
if __name__ == '__main__':
    print('main')
