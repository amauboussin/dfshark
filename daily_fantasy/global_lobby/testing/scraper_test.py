
import re, string, json
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


class Contest():

	def __init__(self, **kwargs):
	    arg_vals = {
	    	'site' : 'No site',
	        'title': 'No Title',
	        'sport' : 'No sport',
	        'size' : 0,
	        'entries' : 0,
	        'buyin' : 0,
	        'payout' : 0,
	        'start' : 0,
	    }
	    arg_vals.update(kwargs)
	    for kw,arg in arg_vals.iteritems():
	        setattr(self, kw, arg)

	def __repr__(self):
		return str(self.__dict__)

	def __str__(self):
		return self.__repr__()

def format_prize_amount(payout):
	payout = string.replace(payout, ',', '')
	payout = string.replace(payout, '$', '')
	return float(payout)

def ftd():

	final = []
	with open('ftd.html', 'r') as rfile:
		html = rfile.read()

	soup = BeautifulSoup(html)
	rows = soup.find_all('tr', class_ = 'lobby_row')

	for row in rows[:3]:

		print row

		contest_args = {
				'site' : 'FanThrowdown',
				'url' : 'https://fanthrowdown.com/game/pickx/' + row['data-league-id'],
				'title': row.find('a', class_ = 'league_info').text,
				'sport' : row['data-sport'],
				'size' : int(row['data-size']),
				'entries' : int(row['data-entries']),
				'buyin' : float(row['data-entry-fee']),
				'payout' : format_prize_amount(row.find('a', class_ = 'payout_modal_btn')['data-total-prizes']),
				'start' : int(row['data-start-time']),
		}

		final.append(Contest(**contest_args))


def fanduel():

	final = []
	with open('fd.html', 'r') as rfile:
		html = rfile.read()
	regex = re.compile('LobbyConnection.initialData = (.*?)LobbyConnection', re.DOTALL)
	json_data = string.strip(regex.search(html).groups()[0])[:-1]
	data = json.loads(json_data)
	contests = data['additions']

	for contest in contests[:4]:
			contest_args = {
				'site' : 'Fanduel',
				'title': contest['title'],
				'sport' : contest['sport'],
				'size' : int(contest['size']),
				'entries' : int(contest['entriesData']),
				'buyin' : int(contest['entryFee']),
				'payout' : int(contest['prizes']),
				'start' : int(contest['startTime']),
			}

			final.append(Contest(**contest_args))
	print final



fanduel()

	# {u'tableSpecId': u'5776', u'entriesDfata': u'2', u'prizeSummary': None, u'startTime': 1388340000, 
	# u'title': u'NFL Salary Cap 60k Sun Dec 29th', u'stack': None, u'cap': u'60000', u'flags': {u'standard': 1}, 
	# u'dateCreated': 1387765982540, u'gameId': u'9305', u'entryFee': 2, u'prizes': 5.4, u'prizeBreakdown': False, 
	# u'entryURL': u'/e/Game/9305?tableId=3610123', u'entryHTML': None, u'startString': u'Sun 1:00&nbsp;pm', 
	# u'uniqueId': u'3610123', u'sport': u'nfl', u'dateUpdated': 1387830398145, u'size': u'3'}
