# -*- coding: utf-8 -*-

import time
import os
import sys
import urllib2, urllib
import json
import ssl
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

cnt = 1
#it seems it's infeasible to downnload files using https protocol
class searchGoogle:
    def searchKey(self, keyword):
        url=('https://www.googleapis.com/customsearch/v1?'
            'key=AIzaSyAHHLD-Xo2gPwcqtpeNL02fa5U_GpjW0nM'
            '&cx=012622939647794549308:mu1irvr0kzs'
            '&q=%s&num=10') % urllib.quote(keyword) 
        print url
        
        try:
            ###it doens't work to set proxy in this way,using xx_net
            ###I don't know why
#            proxy = urllib2.ProxyHandler({'http': '127.0.0.1'})
#            proxy2 = urllib2.ProxyHandler({'https': '127.0.0.1'})
#            opener = urllib2.build_opener(proxy, proxy2)
#            urllib2.install_opener(opener)
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            request = urllib2.Request(url, None)
            request.set_proxy('127.0.0.1:8087', 'http')
            response = urllib2.urlopen(request, context=gcontext)
            results = json.load(response)
            items = results['items']
            for item in items:
                if item.get('mime') == 'application/pdf':
                    link = item['link']
                    if link.startswith('https'):
                        link = link[:4]+link[5:]
                    idx = link.find('ieee.org')
                    if idx != -1:
                        idx = idx + len('ieee.org')
                        link = link[:idx] + '.sci-hub.cc' + link[idx:]
                        
                    if link.find('ieee.org'):
                        r = urllib2.urlopen(link, timeout=60).read()
                        idx1 = r.find('<iframe src = "') + len('<iframe src = "')
                        idx2 = r.find('" id = "pdf"></iframe>')
                        link = r[idx1:idx2]
                    print link
                    r = requests.get(link, stream=True)
                    with open(str(cnt)+keyword+".pdf", 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):  
                            if chunk: # filter out keep-alive new chunks  
                                f.write(chunk)  
                                f.flush() 
                    break
                    #urllib.urlretrieve(link, keyword+"2.pdf", context=gcontext)
            return results
        except Exception, e:
            print e
        else:
            print 'search keyword: %s finished', keyword

sg = searchGoogle()
keywords = open('papers.txt', 'r')
keyword = keywords.readline()
while(keyword):
    keyword = keyword.strip('\n')
    if os.path.exists(str(cnt)+keyword+".pdf"):
        cnt += 1
        keyword = keywords.readline()
        continue
    sg.searchKey(keyword)
    cnt += 1
keywords.close()

