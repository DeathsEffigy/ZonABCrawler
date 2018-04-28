import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# worker dummy class
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
    
    def run(self):
        while True:
            task = self.task_queue.get()
            
            if task is None:
                self.task_queue.task_done()
                break
            
            res = task(self.name)
            self.task_queue.task_done()
            self.result_queue.put(res)
        
        return