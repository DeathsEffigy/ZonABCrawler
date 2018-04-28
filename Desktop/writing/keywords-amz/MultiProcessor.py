import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# management of processes
class MultiProcessor:
    def __init__(self):
        self.jobs = []
        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()
    
    def prep(self, proxy, type, targets, workers = 0):
        self._proxy = proxy
        self._workers = workers
        self._type = type
        self._targets = targets
    
    def execute(self):
        # get workers going
        if (self._workers == 0):
            self._workers = multiprocessing.cpu_count() * 2
        self.workers = [ Worker.Worker(self.tasks, self.results) for i in xrange(self._workers) ]
        for w in self.workers:
            w.start()
        
        # enqueue jobs
        for t in self._targets:
            self.tasks.put(TaskLogic.TaskLogic(t, self._proxy, self._type))
        
        # add poison pills to stack
        for i in xrange(self._workers):
            self.tasks.put(None)
        
        # wait for tasks to finish
        self.tasks.join()
        
        return True
    
    def get(self):
        # get results
        c = len(self._targets)
        r = []
        while c:
            r.append(self.results.get())
            c -= 1
        return r