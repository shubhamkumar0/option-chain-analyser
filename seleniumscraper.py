import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import statistics
import math
import mechanicalsoup
import os.path
from datetime import timedelta, date, datetime


def preProcess(ticker, daysAhead):
	closePrices=[]
	with open('{}.csv'.format(ticker)) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for line in csv_reader:
			if line[4] != "":
				closePrices.append(line[4].replace(',', ''))
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
	yrs_back = 10
	tOneYearback=tNow-((31536000)*yrs_back)
	url="https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(ticker, tOneYearback, tNow)

	browser.get(url)
	time.sleep(1)

	elem = browser.find_element_by_tag_name("body")

	no_of_pagedowns=99
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
	# if file already exists then remove it
	if os.path.isfile(f"{ticker}.csv"):
		os.remove(f"{ticker}.csv")
	# create new file
	with open(f"{ticker}.csv", 'w', newline='') as out_file:
		# Each 3 table has headers as following
		writer = csv.DictWriter(out_file, headings)
		# write the header
		writer.writeheader()
		for row in table_data:
			if row:
				writer.writerow(row)

def price():
	EndDate = date.today() + timedelta(days=7)
	print(EndDate)
	url = "https://web.sensibull.com/option-chain?expiry={0}&tradingsymbol=NIFTY".format(EndDate)
	browser.get(url)
	time.sleep(1)

	elem = browser.find_element_by_tag_name("body")

	no_of_pagedowns=2
	while no_of_pagedowns:
		elem.send_keys(Keys.PAGE_DOWN)
		time.sleep(0.2)
		no_of_pagedowns-=1


	# Get number of rows In table.
	raw_html_page=browser.page_source
	soup= BeautifulSoup(raw_html_page,"html.parser")
	data = {}

	table = soup.find("table", attrs={"id": "optionChainTable-indices"})
	# headings = []
	# head = table.thead.find_all("tr")
	# print(head[0])
	# for span in head[0].find_all("span"):
	# 	headings.append(span.text)
	print("-------------------------------------------------------------------------------------")
	print("-------------------------------------------------------------------------------------")
	print("-------------------------------------------------------------------------------------")

	# table_data = []
	for tr in table.tbody.find_all("tr"):
		# t_row={}
		for a in tr.find_all("a", attrs={"href": "javascript:;", "class": "bold"}):
			print(a)
	# browser.close()

def evaluation(ticker, nDays):
	dates=[]
	closePrices=[]
	with open('{}.csv'.format(ticker)) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for line in csv_reader:
			if line[4] != "" and line[0] != "" and line[0] != "Date":
				dt=datetime.strptime(line[0], '%b %d, %Y')
				dates.append(dt)
				closePrices.append(line[4].replace(',', ''))

	# find the last thursday(target) then keep data till the thursday before it(cutoff) and then make preds
	# if close on the target is in the range- store true in an array and if not false
	# at the end we will check how many true and false are there.
	i=0
	thursdays = []
	for dt in dates:
		if dt.weekday()==3:#Its Thursday
			thursdays.append(i)
		i=i+1
	firstDev=[]
	secondDev=[]
	for idx in range(len(thursdays)-1):
		target = closePrices[thursdays[idx]]
		if len(closePrices[thursdays[idx+1]:])>1:
			l1,l2 = rnge(closePrices[thursdays[idx+1]:], float(target))
			firstDev.append(l1)
			secondDev.append(l2)

	print("1: {}".format(sum(firstDev)/len(firstDev)*100))
	print("2: {}".format(sum(secondDev)/len(secondDev)*100))

def rnge(closePrices, target):
	dailyReturns=[]
	for i in range(len(closePrices)-1):
		dailyReturns.append(math.log(float(closePrices[i+1])/float(closePrices[i])))
	# print(len(closePrices))
	avgVolatility=(sum(dailyReturns)/len(dailyReturns))*5
	stdDevVolatility=statistics.pstdev(dailyReturns)*math.sqrt(5)

	firstRangeMin=avgVolatility-stdDevVolatility
	firstRangeMax=avgVolatility+stdDevVolatility

	scndRangeMin=avgVolatility-(2*stdDevVolatility)
	scndRangeMax=avgVolatility+(2*stdDevVolatility)

	rng1_min = float(closePrices[0])*math.exp(firstRangeMin)
	rng1_max = float(closePrices[0])*math.exp(firstRangeMax)
	if target>rng1_min and target<rng1_max:
		l1=True
	else:
		l1=False

	rng2_min = float(closePrices[0])*math.exp(scndRangeMin)
	rng2_max = float(closePrices[0])*math.exp(scndRangeMax)
	if target>rng2_min and target<rng2_max:
		l2=True
	else:
		l2=False

	return (l1,l2)

browser = webdriver.Firefox(executable_path=r'C:\Users\shubh\Downloads\option-chain-analyser-master\geckodriver.exe')
ticker = str(input('Enter ticker name as given on yahoo finance i.e. CIPLA.NS: '))
nDays = str(input('Enter how many days ahead you want to predict: '))
scrape(ticker)
preProcess(ticker, int(nDays))
# evaluation("%5ENSEI", int(nDays))
# price()
