# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from fortest.demo import Search_engine

if __name__ == '__main__':
    test = Search_engine()
    idx, graph = test.crawl_web('http://udacity.com/cs101x/urank/index.html')
    print(graph)
    ranks = test.compute_ranks(graph, 0)
    print(ranks)
    res = test.ordered_search(idx, ranks, 'for')
    print(res)
