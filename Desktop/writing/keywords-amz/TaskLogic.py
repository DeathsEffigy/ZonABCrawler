import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# task logic (called from workers)
class TaskLogic(object):
    def __init__(self, target, proxy, type):
        self.target = target
        self.proxy = proxy
        self.type = type
        return
    
    def __call__(self, worker):
        p = self.proxy.select()
        
        print '> %i@%s: Served by %s via %s as %i.' % (time.time(), self.target, worker, p, self.type)
        
        try:
            retkw = []
            retli = []
            ph = urllib2.ProxyHandler({'https': p})
            cht = urllib2.build_opener(ph)
            cht.addheaders = self.proxy.fake_agent()
            contents = cht.open('https://www.amazon.com/dp/' + self.target.encode('utf-8'), timeout=5).read()
            
            soup = BeautifulSoup(contents, 'html.parser')
            
            # add titles
            #retkw.append(soup.find(id='ebooksProductTitle').text.encode('utf-8'))
            retkw.append(soup.find(id=re.compile('producttitle', re.IGNORECASE)).text.encode('utf-8'))
            
            # add authors
            for cont in soup.find_all(class_='contributorNameID'):
                retkw.append(cont.text.encode('utf-8'))
            
            # get also boughts
            id_tag = soup.find(id='purchase-sims-feature')
            id_cj = json.loads(id_tag.contents[1]['data-a-carousel-options'])
            retli = id_cj['ajax']['id_list']
                        
            return [retkw, retli]
        except:
            print '> %i/%s: %s failed via %s as %i.' % (time.time(), self.target, worker, p, self.type)
            return None