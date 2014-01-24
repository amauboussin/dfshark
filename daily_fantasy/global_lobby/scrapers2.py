
from bs4 import BeautifulSoup
import mechanize, cookielib
import urllib2, re, json, string, types
import passwords

from models import Contest

from datetime import datetime

# class Contest():
#
# 	def __init__(self, **kwargs):
# 	    arg_vals = {
# 	    	'site' : 'No site',
# 	        'title': 'No Title',
# 	        'sport' : 'No sport',
# 	        'size' : 0,
# 	        'entries' : 0,
# 	        'buyin' : 0,
# 	        'payout' : 0,
# 	        'start' : 0,
# 	    }
# 	    arg_vals.update(kwargs)
# 	    for kw,arg in arg_vals.iteritems():
# 	        setattr(self, kw, arg)
#
# 	def __repr__(self):
# 		return str(self.__dict__)
#
# 	def __str__(self):
# 		return self.__repr__()

class Scraper(object):

	def __init__(self, browser_needed = True):
		self.contests = []
		if browser_needed:
			self.browser = mechanize.Browser()
			self.browser.set_handle_robots(False)
			self.cj = cookielib.LWPCookieJar()
			self.browser.set_cookiejar(self.cj)
			self.browser.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]

	def get_html(self, url):
		response = self.browser.open(url)
		return response.read()

	def update_db(self):
		Contest.objects.bulk_create(self.contests)

class FTDScraper(Scraper):
	def __init__(self):
		super(FTDScraper, self).__init__()
		self.cj.load('/Users/Andrew/Desktop/fs/daily_fantasy/daily_fantasy/static/ftd_cookie.txt', ignore_discard=False, ignore_expires=False)
		self.url = 'https://fanthrowdown.com/lobby'


	def format_prize_amount(self, payout):
		payout = string.replace(payout, ',', '')
		payout = string.replace(payout, '$', '')
		return float(payout)

	def scrape(self, scrape_id):

		response = self.browser.open(self.url)
		html = response.read()
		soup = BeautifulSoup(html)
		rows = soup.find_all('tr', class_ = 'lobby_row')

		for row in rows[:-1]:

			contest_args = {
					'site' : 'FanThrowdown',
					'url' : 'https://fanthrowdown.com/league/player_select/' + row['data-league-id'],
					'title': row.find('a', class_ = 'league_info').text,
					'sport' : row['data-sport'],
					'size' : int(row['data-size']),
					'entries' : int(row['data-entries']),
					'buyin' : float(row['data-entry-fee']),
					'payout' : self.format_prize_amount(row.find('a', class_ = 'payout_modal_btn')['data-total-prizes']),
					'start' : datetime.fromtimestamp(int(row['data-start-time'])),
					'scrape_id' : scrape_id,

			}

			self.contests.append(Contest(**contest_args))



	def login(self):
		self.browser.open('https://fanthrowdown.com/login')

		self.browser.form = list(self.browser.forms())[0]
		for control in self.browser.form.controls:
			if control.name == 'username_email':
				control.value = passwords.email
			elif control.name == 'password':
				control.value = passwords.ftd_password

		response = self.browser.submit()

		wfile = open('ftd.html', 'w')
		wfile.write(response.read())
		wfile.close()

		self.cj.save('/Users/Andrew/Desktop/fs/daily_fantasy/daily_fantasy/static/ftd_cookie.txt', ignore_discard=False, ignore_expires=False)


class FanduelScraper(Scraper):

	def __init__(self):
		super(FanduelScraper, self).__init__()
		self.cj.load('/Users/Andrew/Desktop/fs/daily_fantasy/daily_fantasy/static/fd_cookie.txt', ignore_discard=False, ignore_expires=False)
		self.url = 'https://www.fanduel.com/p/Home'


	def get_entries(self,entriesData):
		if isinstance( entriesData, types.StringTypes) or isinstance(entriesData, int):
			return int(entriesData)
		else: return len(entriesData)


	def scrape(self, scrape_id):
		#check cookie expiration here
		html = self.browser.open(self.url).read()

		regex = re.compile('LobbyConnection.initialData = (.*?)LobbyConnection', re.DOTALL)
		json_data = string.strip(regex.search(html).groups()[0])[:-1]
		data = json.loads(json_data)
		contests = data['additions']
		for contest in contests:
			contest_args = {
				'site' : 'Fanduel',
				'url' : 'https://fanduel.com' + contest['entryURL'],
				'title': contest['title'],
				'sport' : contest['sport'],
				'size' : int(contest['size']),
				'entries' : self.get_entries(contest['entriesData']),
				'buyin' : float(contest['entryFee']),
				'payout' : float(contest['prizes']),
				'start' : datetime.fromtimestamp(int(contest['startTime'])),
				'scrape_id' : scrape_id,
			}

			self.contests.append(Contest(**contest_args))


	def login(self):
		self.browser.open('https://www.fanduel.com/p/login')
		self.browser.form = list(self.browser.forms())[0]
		for control in self.browser.form.controls:
			if control.id == 'email':
				control.value = passwords.email
			elif control.id == 'password':
				control.value = passwords.fanduel_password

		response = self.browser.submit()

		wfile = open('fd.html', 'w')
		wfile.write(response.read())
		wfile.close()

		self.cj.save('/Users/Andrew/Desktop/fs/daily_fantasy/daily_fantasy/static/fd_cookie.txt', ignore_discard=False, ignore_expires=False)

class DraftKingsScraper(Scraper):

	def __init__(self):
		super(DraftKingsScraper, self).__init__(browser_needed = False)


	def find_between(self, s, first, last):
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]


	def scrape(self, scrape_id):
		json_data = urllib2.urlopen('https://www.draftkings.com/contest/index').read()
		contests = json.loads(json_data)
		guranteed = [c for c in contests if (c['attr'].has_key('IsGuaranteed') and c['attr']['IsGuaranteed'] == 'true') ]
		for contest in guranteed[:-1]:

			contest_args = {
				'site' : 'DraftKings',
				'url' : 'https://www.draftkings.com/contest/draftteam/%s' % (contest['id']),
				'title': contest['n'],
				'sport' : 'todo',
				'size' : int(contest['m']),
				'entries' : int(contest['nt']),
				'buyin' : int(contest['a']),
				'payout' : int(contest['po']),
				'start' : datetime.fromtimestamp(int(self.find_between(contest['sd'], '(', ')'))/1000),
				'scrape_id' : scrape_id,
			}

			self.contests.append(Contest(**contest_args))












