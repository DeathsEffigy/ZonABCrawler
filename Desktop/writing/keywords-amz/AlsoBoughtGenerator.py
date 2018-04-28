import urllib2, urllib, re, time, sys, os, os.path, math, random, json, multiprocessing, requests
from bs4 import BeautifulSoup
import Keywords, MultiProcessor, ProxyManager, ProxyFetcher, TaskLogic, Worker

# main
if __name__ == '__main__':
    # change keywords_path, nothing else
    keywords_path = "/Users/fabianschneider/Desktop/writing/keywords-amz/legacy/"
    
    # logic go
    kw = Keywords.Keywords()
    
    # fetch current proxies
    ttt = time.time()
    print '\n\n\n> Preparing proxies...'
    proxy = ProxyManager.ProxyManager()
    list = ProxyFetcher.get_list(proxy)
    proxy.add_all(list)
    ttte = time.time()
    print '> > Completed. %i proxies available (took %is).\n\n\n' % (len(proxy.list), (ttte - ttt))
    
    # bases
    baseline = raw_input("What's the baseline product?\n=> ")
    depth = int(raw_input("How deep do you wanna crawl? Rec. 1-2\n=> "))
    amount = int(raw_input("How many crawlers do you wanna enslave? Rec. 8ish\nIf you don't know what you're doing, please enter 0 to let the code figure it out.\n=> "))
    time_start = time.time()
    print 'Alright cool. Getting to work.\n\n\n'
    
    # baseline crawl
    print '> Baseline crawl.'
    cht = urllib2.build_opener()
    cht.addheaders = proxy.fake_agent()
    amz_stream = cht.open('https://amazon.com/dp/' + baseline.encode('utf-8')).read()
    amz_soup = BeautifulSoup(amz_stream, 'html.parser')
    
    tag = amz_soup.find(id='purchase-sims-feature')
    cj = json.loads(tag.contents[1]['data-a-carousel-options'])
    targets = cj['ajax']['id_list']
    print '> > Completed.'
    
    # get all crawl
    x = 0
    while x < depth:
        print '\n\n\n> Going in for recursion no. %i.' % x
        mp = MultiProcessor.MultiProcessor()
        mp.prep(proxy, 1, targets, amount)
        mp.execute()
        r = mp.get()
        
        # evaluate
        ln = []
        for res in r:
            if res is None:
                continue
            for k in res[0]:
                kw.add_keywords(kw.make_keywords(k))
            for it in res[1]:
                if it not in ln:
                    ln.append(it)
        if (len(ln) < 1):
            break
        targets = ln
        x += 1
    
    time_finish = time.time()
    time_taken = time_finish - time_start
    
    print '> > All done.'
    print '> > Took me a whopping %f seconds to fetch %i keywords.' % (time_taken, len(kw.list))
    
    print '\n\n\n> Saving...'
    fi = keywords_path + str(baseline) + '_' + str(depth) + '_master.txt'
    f = open(fi, 'w+')
    for k in kw.list:
        f.write(k + "\r\n")
    f.close()
    
    if (len(kw.list) > 999):
        fl = keywords_path + str(baseline) + '_' + str(depth)
        tot = float(len(kw.list))
        max = float(999)
        n_files = math.ceil(tot / max)
        current_k = 0
        current_l = 0
        for k in kw.list:
            if (current_k > 999):
                current_k = 0
                current_l += 1
            if (os.path.isfile(fl + '_' + str(current_l) + '.txt')):
                f = open(fl + '_' + str(current_l) + '.txt', 'a')
            else:
                f = open(fl + '_' + str(current_l) + '.txt', 'w+')
            f.write(k + "\r\n")
            f.close()
            current_k += 1
    print("> > Saved. Have fun.")