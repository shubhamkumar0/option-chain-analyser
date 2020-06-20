import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import statistics
import math
import mechanicalsoup


def preProcess(ticker, daysAhead):
	closePrices=[]
	with open('{}.csv'.format(ticker)) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for line in csv_reader:
			if line[4] != "":
				closePrices.append(line[4])
	closePrices= closePrices[1:]
	dailyReturns=[]
	for i in range(len(closePrices)-1):
		dailyReturns.append(math.log(float(closePrices[i+1])/float(closePrices[i])))

	avgVolatility=(sum(dailyReturns)/len(dailyReturns))*daysAhead
	stdDevVolatility=statistics.pstdev(dailyReturns)*math.sqrt(daysAhead)

	firstRangeMin=avgVolatility-stdDevVolatility
	firstRangeMax=avgVolatility+stdDevVolatility

	scndRangeMin=avgVolatility-(2*stdDevVolatility)
	scndRangeMax=avgVolatility+(2*stdDevVolatility)

	print("First std dev range : {0} to {1}".format(float(closePrices[0])*math.exp(firstRangeMin), float(closePrices[0])*math.exp(firstRangeMax)))
	print("Second std dev range : {0} to {1}".format(float(closePrices[0])*math.exp(scndRangeMin), float(closePrices[0])*math.exp(scndRangeMax)))




def scrape(ticker):
	tNow = int(time.time())
	tOneYearback=tNow-31536000
	url="https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(ticker, tOneYearback, tNow)

	browser.get(url)
	time.sleep(1)

	elem = browser.find_element_by_tag_name("body")

	no_of_pagedowns=20
	while no_of_pagedowns:
		elem.send_keys(Keys.PAGE_DOWN)
		time.sleep(0.2)
		no_of_pagedowns-=1


	# Get number of rows In table.
	raw_html_page=browser.page_source
	soup= BeautifulSoup(raw_html_page,"html.parser")
	data = {}

	table = soup.find("table", attrs={"class": "W(100%) M(0)"})
	headings = []
	head = table.thead.find_all("tr")
	for span in head[0].find_all("span"):
		headings.append(span.text)


	table_data = []
	for tr in table.tbody.find_all("tr"):
		t_row={}
		for span, th in zip(tr.find_all("span"), headings):
			t_row[th] = span.text
		table_data.append(t_row)

	browser.close()

	# Step 4: Export the data to csv
	with open(f"{ticker}.csv", 'w') as out_file:
		# Each 3 table has headers as following
		writer = csv.DictWriter(out_file, headings)
		# write the header
		writer.writeheader()
		for row in table_data:
			if row:
				writer.writerow(row)

def price():
	browser.follow_link("https://zerodha.com/margin-calculator/SPAN/")
	browser.select_form(id="form-span")
	browser["exchange"]="NFO"
	browser["product"]="Options"
	browser["product"]="Options"
	browser["product"]="Options"
	browser["scrip"]="BAJFINANCE 25-JUN-20"
	browser["option_type"]="Puts"
	browser["strike_price"]="2000"
	browser["lot_size"]="250"
	search_response = browser.submit()
	print(search_response)


browser = webdriver.Firefox(executable_path='/home/kakashi/Downloads/geckodriver')
ticker = str(input('Enter ticker name as given on yahoo finance i.e. CIPLA.NS: '))
nDays = str(input('Enter how many days ahead you want to predict: '))
scrape(ticker)
preProcess(ticker, int(nDays))
price()
