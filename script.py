import requests
from bs4 import BeautifulSoup
import csv
import statistics
import math
import time

def scrape(ticker):
	tNow = int(time.time())
	tOneYearback=tNow-31536000
	url="https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(ticker, tOneYearback, tNow)
	page = requests.get(url).text
	
	soup= BeautifulSoup(page,"html.parser")
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


	# Step 4: Export the data to csv
	with open(f"{ticker}.csv", 'w') as out_file:
		# Each 3 table has headers as following
		writer = csv.DictWriter(out_file, headings)
		# write the header
		writer.writeheader()
		for row in table_data:
			if row:
				writer.writerow(row)

def preProcess(ticker, daysAhead):
	closePrices=[]
	with open('{}.csv'.format(ticker)) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for line in csv_reader:
			if line[8] != "":
				closePrices.append(line[8])
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
	print("First std dev range : {0} to {1}".format(float(closePrices[len(closePrices)-1])*math.exp(firstRangeMin), float(closePrices[len(closePrices)-1])*math.exp(firstRangeMax)))
	print("Second std dev range : {0} to {1}".format(float(closePrices[len(closePrices)-1])*math.exp(scndRangeMin), float(closePrices[len(closePrices)-1])*math.exp(scndRangeMax)))

tickerInput = str(input('Enter ticker name as given on yahoo finance i.e. CIPLA.NS: '))
nDays = str(input('Enter how many days ahead you want to predict: '))

# print()
# scrape(tickerInput)
preProcess(tickerInput, int(nDays))