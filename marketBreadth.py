import requests
import re
from bs4 import BeautifulSoup
import time

'''
Basic_Materials
Communication_Services
Consumer_Cyclical
Consumer_Defensive
Energy
Financial_Services
Healthcare
Industrials
Real_Estate
Technology
Utilities
'''
sectors = [
{'name':'mat', 'fullname':'Basic_Materials'},
{'name':'com', 'fullname':'Communication_Services'},
{'name':'cns', 'fullname':'Consumer_Cyclical'},
{'name':'cmd', 'fullname':'Consumer_Defensive'},
{'name':'eng', 'fullname':'Energy'},
{'name':'fin', 'fullname':'Financial_Services'},
{'name':'hlt', 'fullname':'Healthcare'},
{'name':'ind', 'fullname':'Industrials'},
{'name':'res', 'fullname':'Real_Estate'},
{'name':'tec', 'fullname':'Technology'},
{'name':'utl', 'fullname':'Utilities'}]

def stock_filter(stock, algo):

def get_sector_stocks(sector):
	data = []
	offset = 0
	flag = True
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
				'accept-encoding': 'gzip, deflate, br',
				'accept-language': 'en-US,en;q=0.9',
				'accept': '*/*',
				'referer':'https://finance.yahoo.com/sector/ms_%s' % sector,
				'content-type': 'text/plain;charset=UTF-8'
	}
	while(flag):
		url = 'https://finance.yahoo.com/screener/predefined/ms_%s?count=100&offset=%d' % (sector,offset)
		print url
		response = requests.get(url,headers=headers)
		soup = BeautifulSoup(response.text,'html.parser')
		div_table = soup.find('div', attrs={"id" :"fin-scr-res-table"})
		table = div_table.find('table')
		if offset == 0:
			table_head = table.find('thead')
			cols = table_head.find_all('th')
			cols = [ele.text.strip() for ele in cols]
			cols.remove('52 Week Range')
			data.append([ele for ele in cols if ele])
		table_body = table.find('tbody')
		rows = table_body.find_all('tr')
		for row in rows:
			cols = row.find_all('td')
			cols = [ele.text.strip() for ele in cols]
			data.append([ele for ele in cols if ele])
		total_results = int(div_table.find_all('span')[2].text.split(" ")[2])
		print total_results
		offset += 100
		if offset >= total_results:
			flag = False
		time.sleep(10)
	res_df = pd.DataFrame(data[1:], columns = data[0])
	return res_df

def get_all_stocks():
	for sector in sectors:
		res = get_sector_stocks(sector['fullname'])
		res.to_csv("data/%s.csv" % sector['name'], encoding = 'utf-8')


