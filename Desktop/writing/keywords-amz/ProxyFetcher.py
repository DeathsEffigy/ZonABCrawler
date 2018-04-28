import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

def get_list(proxy, do_test = True):
    print '> Fetching list...'
    # prepare list
    stream = requests.get('https://free-proxy-list.net')
    soup = BeautifulSoup(stream.text, 'html.parser')
    table = soup.find(id='proxylisttable')
    list = []
    trs = table.find_all('tr')
    for tr in trs:
        if (tr.contents[6].text != 'yes'):
            continue
        if (tr.contents[4].text == 'transparent'):
            continue
        ts = tr.contents[7].text
        if 'seconds' not in ts:
            ts = int(re.sub('[^0-9]', '', ts))
            if ts > 10:
                continue
        list.append('%s:%s' % (tr.contents[0].text, tr.contents[1].text))
    
    print '> Weeding out proxies...'
    # test list
    if do_test is True:
        for p in list:
            ph = urllib2.ProxyHandler({'https': p})
            cht = urllib2.build_opener(ph)
            cht.addheaders = proxy.fake_agent()
            try:
                contents = cht.open('https://free-proxy-list.net', timeout=3).read()
                # no timeout = pass
            except:
                # timeout = fail
                list.remove(p)
    return list