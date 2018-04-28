import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# management of proxies and cycling
class ProxyManager:
    def __init__(self):
        self.list = []
        self.iterator = 0
    
    def add(self, string):
        if string not in self.list:
            self.list.append(string)
    
    def add_all(self, obj):
        for string in obj:
            self.add(string)
    
    def reset(self):
        self.iterator = 0
    
    def cycle(self):
        self.iterator += 1
    
    def select_cycle(self):
        if (self.iterator >= len(self.list)):
            self.reset()
        self.cycle()
        return self.list[(self.iterator - 1)]
    
    def select(self):
        return self.list[random.randrange(0, len(self.list))]
    
    def remove(self, string):
        self.list.remove(string)
    
    def fake_agent(self):
        browsers = ['Safari', 'Chrome', 'Edge']
        browser = browsers[random.randrange(0, len(browsers))]
        version = ''
        
        if browser == 'Safari':
            version = '%i.%i' % (random.randrange(1, 11), random.randrange(0, 9))
        elif browser == 'Chrome':
            version = '%i.%i.%i.%i' % (random.randrange(1, 65), random.randrange(0, 9), random.randrange(0, 5160), random.randrange(0, 512))
        elif browser == 'Edge':
            version = '%i.%i.%i.%i' % (random.randrange(1, 41), random.randrange(0, 20000), random.randrange(0, 15), random.randrange(0, 9))
        
        return [('User-agent', '%s/%s' % (browser, version))]