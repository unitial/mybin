#!/usr/bin/python

import httplib
import urllib
from BeautifulSoup import BeautifulSoup
import re
import time
import sys
import os.path

def gen_fetch(title):
    pubTitle = ""
    pdfURL = ""

    params = urllib.urlencode({'q': title, 'num': 1})
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    url = "/scholar"+"?"+params
    conn = httplib.HTTPConnection("scholar.google.com")
    conn.request("GET", url, "", headers)
    resp = conn.getresponse()

    if resp.status==200:
        html = resp.read().decode('ascii', 'ignore')
        soup = BeautifulSoup(html)
        for record in soup('div', {'class': 'gs_r'}):
            topPart = record.first('h3')
            for part in topPart.a.contents:
                pubTitle += str(part.string)
            if pubTitle == None:
                continue

            pdfPart = record.first('span', {'class': 'gs_ggs gs_fl'})
            if pdfPart != None and re.search('\[PDF\]', str(pdfPart)) != None:
                pdfURL = pdfPart.a['href']

    print "#", title
    if pubTitle != "" and pdfURL != "":
        pubTitle = pubTitle.replace(':', ' - ')
        print "wget --no-check-certificate -O \"" + pubTitle + ".pdf\"", "\"" + pdfURL + "\""
    else:
        print "# not found."

if __name__ == '__main__':
    if os.path.isfile(sys.argv[1]) is False:
        gen_fetch(sys.argv[1])
    else:
        f = open(sys.argv[1])
        line = f.readline()
        line = line.replace('\n', '')
        while line != '':
            gen_fetch(line)
            line = f.readline()
            line = line.replace('\n', '')
