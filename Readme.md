# PageRank模拟谷歌搜索引擎
## 介绍
数据使用的是Webb Spam数据集，download from https://www.cc.gatech.edu/projects/doi/WebbSpamCorpus.html

We need three file: `url_graph_file`/`url_id_mapping`/`WebbSpamCorpus.tgz`，下载下的数据放到`./data`下

数据集介绍：
包括263446个url结点

`url_graph_file`: 包括URL的ID的连接信息，由该数据来构建图，计算pagerank值

`url_id_mapping`：包括url和ID的对应关系

`WebbSpamCorpus.tgz`：包括URL的html文件，通过该数据来构建倒排索引


实现功能包括：
1. 根据`url_graph_file`构建图、计算pagerank值，图结点由20k+ 普通的pagerank算法跑不动，使用稀疏矩阵和调用networkx两种方法计算pagerank值，存储到rank.tsv中
2. 根据`WebbSpamCorpus.tgz`构建倒排索引
3. 根据倒排索引、pagerank值，来实现搜索排序和结果返回

项目结构：
```
-- data
    url_graph_file
    url_id_mapping
    WebbSpamCorpus.tgz
Indexmake.py
SearchEnginePR.py
rank.tsv
index.tsv
```

```
-- fortest
    demo.py
    main.py
    # 以上实现search engine的demo，只能使用小量的数据实现
    pagerankwithNX.py
    rank_save.tsv
    # 调用networkx中的pagerank计算方法，能够对大数据量进行计算，速度也很快，生成结果存储在rank_save.tsv
    SearchEngine.py
```
## Setup
The Search Engine is implemented in `SearchEnginePR.py`

run 
```
python3 SearchEnginePR.py
```
Running result is：(you should input your search word in `Please input your search word: `    ` uts Australia`)
```
welcome to my search engine!
Starting initial Search Engine......
Finished initialization.
Starting building index from htmls......
Finished building index.
Starting calculate PageRank......
Finished calculate PageRank
Please input your search word: uts Australia
uts Australia
======Start searching======
Search result is: 
['http://www.concierge.com/deals/cruise/', 'http://www.playgroundsoftheworld.com/xstream/email/potw.asp', 'http://whitepaper.sdmagazine.com/cmpsdmagazine/MainServlet?ksAction=Home', 'http://flyer.com/', 'http://www.naturopath.com/', 'http://reservations.johannesburg.com/nexres/start-pages/travelpage.cgi?src=10011275', 'http://www.concierge.com/cntraveler/whereareyou/', 'http://www.searchenginejournal.com/index.php?p=1036', 'http://www.antwerp.com/', 'http://news.ft.com/cms/4bb9612a-d254-11d8-b661-00000e2511c8.html', 'http://alumni.net/', 'http://www.energyreview.net/default.asp', 'http://www.knowledgestorm.com/search/sponsor/results/INTUITIVEMANUFACTURING/1537/50286/1/index.jsp?showReturnToResultsLinkForFS=Y', 'http://www.savethechildren.net/alliance/index.html', 'http://www.diversityworking.com/communityChannels/africanAmerican/newaccount.php', 'http://www.letmestayforaday.com/report/?idH8', 'http://www.aol.com.ar/principal/', 'http://www.insurancenewsnet.com/fpr.asp', 'http://www.onthesnow.com/ski/', 'http://www.redstart.com/', 'http://www.exactseek.com/', 'http://thin.hearsay.com/', 'http://www.concierge.com/deals/', 'http://www.nsisoftware.com/leading-the-way/press-releases/', 'http://www.searchenginejournal.com/index.php?p=235', 'http://www.hearsay.com/', 'http://www.playgroundsoftheworld.com/xstream/email/far_wide_australia.asp', 'http://www.pleasantholidays.com/PleasantHolidaysWeb/SpecialsOverviewDisplay.do', 'http://www.easyroommate.com/index.cfm?ac=easyrent', 'http://ecardica.com/', 'http://www.august.com/', 'http://away.com/about_us/privacy.adp', 'http://news.scotsman.com/international.cfm?id=283942004', 'http://www.galtglobalreview.com/business/asian_roundup17.html', 'http://www.knowledgestorm.com/search/company/Sockeye%20Solutions/UserNewsletterOctober2003/Sockeye%20Solutions', 'http://www.itbusinessedge.com/', 'http://www.verisign.com/verisign-worldwide/index.html', 'http://www.concierge.com/', 'http://www.how2vacation.com/deals/gotimeevents_110.aspx', 'http://www.sans.org/top20/', 'http://www.poise.com/', 'http://www.spare.com/', 'http://rhodesia.com/', 'http://www.shop.com', 'http://www.institutionalinvestor.com/', 'http://www.citrix.com/lang/English/training.asp', 'http://www.ecardica.com/', 'http://www.gozingsurveys.com/survey_site/index.asp', 'http://www.calais.com/', 'http://www.nwa.com/alliance/', 'http://www.sitepoint.com/newsletter/archives.php', 'http://www.palm.com', 'http://www.playgroundsoftheworld.com/xstream/email/australia.asp', 'http://www.how2vacation.com/deals/39760003590503.aspx', 'http://www.wine.com/wineshop/product_detail.asp?PProduct_ID=PDXCASOUTHCORP4PK&Nu=p_family_name', 'http://www.pleasantholidays.com/PleasantHolidaysWeb/MainDestinationDisplayView.do?storeid=0&langid=-1&key_MainDestinationOID=code__.__MEX', 'http://notre.com/', 'http://www.azerbaijan.com/', 'http://news.com.com/', 'http://www.webshots.com/', 'http://www.miningnews.net/StoryView.asp?StoryID=16904', 'http://www.knowledgestorm.com/MainServlet?ksAction=privacy', 'http://www.prague.com/', 'http://www.knowledgestorm.com/MainServlet?ksAction=legal', 'http://techrepublic.com.com/', 'http://www.schizophrenia.com/']
```
## data
you have to tar data file: data/WebbSpamCorpus.tgz first.

```tar -zxvf ./data/WebbSpamCorpus.tgz```

## generate rank
This model is to generate rank file based on `data/url_graph_file`.

Main method is in `SearchEnginePR/PageRank()`.

And we save `rank.tsv` to save rank dict, so that you dont have to execute it everytime.

## generate index
This model is to generate index file based on content in each url-html files.

Main method is in `Indexmake.py/read_data()`

And we save `index.tsv` to save index dict, so that you dont have to execute is everytime.


