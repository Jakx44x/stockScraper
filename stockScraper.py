from bs4 import BeautifulSoup
import requests
import pandas as pd


def Main():
	'''executes the main body of the code'''
	url = getURL()
	tags = parseData(url)
	stockData = getStocks(tags)
	formatReturns(stockData)

def getURL():
	#I will replace this with an input statement later
	stock = input("Stock: ")
	url = requests.get(f'https://finance.yahoo.com/quote/{stock}/history?p={stock}').text
	

	return url


def parseData(url):
	'''will parse the data in the url to get specified data. In this case
	that is stock prices at particular dates'''
	#parses the raw html into a more readable format
	soup = BeautifulSoup(url, 'lxml')

	#finds the tag(s) titled <tbody within the html> and returns all tags 
	#in <tbody>
	tbody = soup.find("tbody")
	
	#grabs ALL tags titled td (table data) within <tbody tag>
	tags = tbody.find_all("td")
	


	return tags

def getStocks(tags):
	'''will take the data in tags, and grab the stock prices'''
	yahooMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Dec']
	stockData = {}
	tempReturns = []

	rawData = []
	#puts all the stock returns into a list of the data
	for i in tags:
		#makes sure the dividend payments aren't in raw return data
		if i.text.find("Dividend") > -1:
			continue
		rawData.append(i.text)
	
	print(rawData)
	key = 'a'
	#goes through each element in the rawData list and puts them in a ditcitonary
	for i in rawData:
		#finds the specific months in the rawData
		if i[0:3] in yahooMonths:
			#once you find a new date, that ends the data in the last date, so you need to update that one
			stockData.update({key:tempReturns})
			#now that you have the new date, you need to update the key after you update the dict
			key = i
			#you also need to reset the tempReturns for the new Date
			tempReturns = []
			#you don't want to add the new Date to the returns list, so we continue to move to the next item
			continue
		tempReturns.append(i)
	#deletes the temporary key value so we don't see it in our data	
	del stockData['a']	
	return stockData
	
	
def formatReturns(stockData):
	#turns the dictionary:"stockData" into a pandas dataframe, where the keys
	#are the row indexes, and the columns as specified
	stockDataDF = pd.DataFrame.from_dict(stockData, orient='index', columns=["Open", "High", "Low", "Close", "Adj. Close", "Volume"])
	
	print(stockDataDF)


if __name__ == '__main__':
	Main()