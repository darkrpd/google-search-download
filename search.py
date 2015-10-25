'''
Created on Oct 25, 2015

@author: teaddict
'''
#!/usr/bin/python3
import json
import urllib.request, urllib.parse 
import os, datetime
import sys

downloadList = []

def search(searchfor):
    query = urllib.parse.urlencode({'q': searchfor})
    #this query brings only first 8 results -> API max give 8 results
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&rsz=large' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    data = results['responseData']
    pages = int(data['cursor']['estimatedResultCount'])
    print('Total results: %d' % pages)
    getAllUrls(data)
    pages = int(pages / 8)
    for i in range(pages):
        query = urllib.parse.urlencode({'q': searchfor})
        #we got the first page and now we begin with second page 9 , 10 , 11 etc.
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&%s&start=%d' % (query, (i*8)+1)
        search_response = urllib.request.urlopen(url)
        search_results = search_response.read().decode("utf8")
        results = json.loads(search_results)
        data = results['responseData']
        getAllUrls(data)
    #at the end download all
    downloadAll()
def getAllUrls(data):
    hits = data['results']
    for h in hits: 
        downloadList.append(h['url'])
def downloadAll():
    # I create a driectory with timestamp so i download all files into this directory
    mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(mydir)
    for i in range(len(downloadList)):
        fileName = str(downloadList[i]).split('/')[-1]
        print("downloaded filename: " + fileName + " url: " + downloadList[i])
        urllib.request.urlretrieve(downloadList[i], mydir +"/" + fileName)    
    
    print("all downloaded!!!")
    
search("site:"+sys.argv[1])