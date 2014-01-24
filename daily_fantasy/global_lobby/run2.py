from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from scrapers2 import *


scrapers = [DraftKingsScraper(), FTDScraper(), FanduelScraper()]

pool = ThreadPool(3)
pool.map(lambda s : s.scrape(), scrapers )
pool.close()
pool.join()


for s in scrapers:
	for c in s.contests[:5]:
		print c
