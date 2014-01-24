from multiprocessing import Process, Queue
from time import sleep, time
from scrapers import *


def main():
	results_queue = Queue()
	scrapers = [DraftKingsScraper(results_queue), FTDScraper(results_queue), FanduelScraper(results_queue)]
	jobs = [Process(target= s.scrape, args=()) for s in scrapers ]
	for job in jobs: job.start()
	for job in jobs: job.join(60)
	contests = []
	for s in scrapers:
		while True:
			item = results_queue.get()
			if item is None: #break on sentinel
				break
			contests.append(item)
	write_contests(contests)
	#print '\n'.join(str(contests))
	
def write_contests(contests):
	wfile = open('contests.txt', 'w')
	for c in contests:
		wfile.write(str(c) + '\n')
	wfile.close()

def main2():
	results_queue = Queue()
	scrapers = [DraftKingsScraper(results_queue), FTDScraper(results_queue), FanduelScraper(results_queue)]
	for s in scrapers:
		s.scrape()
	contests = []
	for s in scrapers:
		while True:
			item = results_queue.get()
			if item is None: #break on sentinel
				break
			contests.append(item)
	print len(contests)
	write_contests(contests)

def test_scraper(scraper):
	scraper.scrape()
	contests = []
	while True:
		item = results_queue.get()
		if item is None: #break on sentinel
			break
		contests.append(item)

	print len(contests)
	print str(contests)


if __name__ == '__main__':
	results_queue = Queue()
	s = FanduelScraper(results_queue)
	t0 = time()
	#main()
	test_scraper(s)
	t1 = time()
	print 'Took %f' %(t1-t0)



