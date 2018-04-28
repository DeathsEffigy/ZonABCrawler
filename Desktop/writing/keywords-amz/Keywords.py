import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# keyword handler
class Keywords:
    def __init__(self):
        self.list = []
    
    def fix_keyword (self, string):
        string = re.sub('[^a-z0-9 \-\']', '', string, 0, re.IGNORECASE).strip()
        string = re.sub('( \-)+|(\- )+|(\-$)+|(^\-)+', '', string, 0, re.IGNORECASE).strip()
        string = re.sub(' +', ' ', string)
        if (string.count(' ') > 9):
            string = " ".join(string.split(' ', 9)[:9]).strip()
        if (len(string) > 79):
                string = string[0:78].strip()
        if ("kindle" in string or "Kindle" in string or "KINDLE" in string):
            return ''
        return string

    def make_keywords (self, string):
        keywords_t = []
        
        for hit in re.finditer('\(([^,#]+)([,#]+.+)?\)', string, re.IGNORECASE):
            hit_s = hit.group(1)
            string = string.replace(hit.group(0), '')
            hit_s = re.sub('book [#0-9\-]+', '', hit_s, 0, re.IGNORECASE)
            keywords_t.append(self.fix_keyword(hit_s))
        
        for match in string.split(':'):
            for match_n in match.split(' - '):
                keywords_t.append(self.fix_keyword(match_n))
        
        return keywords_t

    def add_keywords (self, obj):
        for kw in obj:
            if kw not in self.list:
                self.list.append(kw)
        return True

    def get(self):
        return self.list