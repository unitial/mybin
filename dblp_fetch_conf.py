#!/usr/bin/python

import httplib
import urllib
import sys
from BeautifulSoup import BeautifulSoup

# http://www.informatik.uni-trier.de/~ley/db/conf/uss/index.html
# <html><body>
#   <ul>
#     <li><a name="SongCCWZ11" href="../../indices/a-tree/s/Song:Xiang.html">Xiang Song</a>,
#         <a href="../../indices/a-tree/c/Chen:Haibo.html">Haibo Chen</a>,
#         <a href="../../indices/a-tree/c/Chen:Rong.html">Rong Chen</a>,
#         <a href="../../indices/a-tree/w/Wang:Yuanxuan.html">Yuanxuan Wang</a>,
#         <a href="../../indices/a-tree/z/Zang:Binyu.html">Binyu Zang</a>:
#         <br>
#         <b>A case for scaling applications to many-core with OS clustering.</b>61-76
#         <br>
#         <a ...>...</a>
#         <a ...>...</a>
#         <a ...>...</a>
#         <a ...>...</a>
#         <a ...>...</a>
#         <a ...>...</a>
#     </li>
#     <li>...</li>
#   </ul>
# </html></body>

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " conf year"
        print "  conf: osdi sosp ccs eurosys sp(s&p) uss(usenix security sym) "
        print "  e.g. " + sys.argv[0] + " eurosys 2011"
        sys.exit(1)

    conf = sys.argv[1]
    year = sys.argv[2]
    url = "/~ley/db/conf/" + conf + "/" + conf + year + ".html"
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    conn = httplib.HTTPConnection("www.informatik.uni-trier.de")
    conn.request("GET", url, "", headers)
    resp = conn.getresponse()

    if resp.status == 200:
        html = resp.read().decode('ascii', 'ignore')
        soup = BeautifulSoup(html)
        for record in soup('li'):
            print str(record.b.contents[0]).replace('\n', '')
    else:
        print resp.status
