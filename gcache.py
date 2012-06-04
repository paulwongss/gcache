#!/usr/bin/python
# Original script by: http://www.guyrutenberg.com/2008/10/02/retrieving-googles-cache-for-a-whole-website/
# Ported to Python 3.x by Luka Pušić <luka@pusic.si> http://360percents.com
#
import urllib.request
import re
import socket
import os
import random
import time
socket.setdefaulttimeout(30)
#adjust the site here
search_term="your search query here" #!!change this to your query!!
def main():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'}
    url = "http://www.google.com/search?q="+search_term
    regex_cache = re.compile(r'<a href="([^"]*)"[^>]*>Cached</a>')
    regex_next = re.compile('<a href="([^"]*)"[^>]*><span[^>]*>[^<]*</span><span[^>]*>Next</span></a>')
 
    #this is the directory we will save files to
    try:
        os.mkdir('files')
    except:
        pass
    counter = 195
    pagenum = 18
    more = True
    while(more):
        pagenum += 1
        print("PAGE"+str(pagenum)+": "+url)
        req = urllib.request.Request(url, None, headers)
        page = urllib.request.urlopen(req).read().decode("utf-8")
        matches = regex_cache.findall(page)
        for match in matches:
            match = 'http:'+match
            counter+=1
            tmp_req = urllib.request.Request(match.replace('&amp;','&'), None, headers)
            tmp_page = urllib.request.urlopen(tmp_req).read()
            print(counter,": "+match)
            f = open('files/'+str(counter)+'.html','wb')
            f.write(tmp_page)
            f.close()
            #comment out the code below if you expect to crawl less than 50 pages
            random_interval=random.randrange(1,10,1)
            print("sleeping for: " + str(random_interval) + " seconds")
            time.sleep(random_interval)
        #now check if there is more pages
        match = regex_next.search(page)
        if match == None:
            more = False
        else:
            url = "http://www.google.com"+match.group(1).replace('&amp;','&')
 
if __name__=="__main__":
    main()
 
# vim: ai ts=4 sts=4 et sw=4
