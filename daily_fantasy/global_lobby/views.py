
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render_to_response, render, HttpResponse
from multiprocessing import Process, Queue
from django.db.models import Max
import simplejson

from django.core import serializers
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from scrapers2 import *
from time import sleep, time, mktime

def home (request):
    return render(request, 'index.html', {})

def raw_data(request):
    id = Contest.objects.all().aggregate(Max('scrape_id'))['scrape_id__max']
    contests = Contest.objects.filter(scrape_id = id)
    json = serializers.serialize("json", contests)
    return HttpResponse(json, mimetype="application/json")


def print_contests(request):
    scrapers = [DraftKingsScraper(), FTDScraper(), FanduelScraper()]
    pool = ThreadPool(len(scrapers))
    pool.map(lambda s : s.scrape(0), scrapers )
    pool.close()
    pool.join()

    contests = [contest for scraper in scrapers for contest in scraper.contests]

    return render(request, 'simple_home.html', {'contests' : contests})


def refresh_database(request):
    id = Contest.objects.all().aggregate(Max('scrape_id'))['scrape_id__max'] + 1
    scrapers = [DraftKingsScraper(), FTDScraper(), FanduelScraper()]
    pool = ThreadPool(3)
    pool.map(lambda s : s.scrape(id), scrapers )
    pool.close()
    pool.join()

    for s in scrapers:
        s.update_db()

    return render(request, 'simple_message.html', {'message' : 'Refreshed database'})


def test_scraper():
    results_queue = Queue()
    scraper = FanduelScraper()
    scraper.scrape()
    contests = []
    while True:
        item = results_queue.get()
        if item is None: #break on sentinel
            break
        contests.append(item)

    print len(contests)
    print str(contests)

    return render_to_response('simple_message.html', {'message' : 'testing'})