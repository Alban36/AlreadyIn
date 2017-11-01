from bs4 import BeautifulSoup
import urllib2

site = "https://www.basketball-reference.com"

seasonPage = site + "/leagues/NBA_2017_games.html"

req = urllib2.Request(seasonPage)
resp = urllib2.urlopen(req)
page = resp.read()

soup = BeautifulSoup(page)
schedule_pages = soup.find_all("div", class_="filter")

links = schedule_pages[0].find_all("a")

for link in links:
	scheduleLink = site + link["href"]
	print("***")
	print(scheduleLink+"\n")
	schedulePage = urllib2.urlopen(scheduleLink)
	soup2 = BeautifulSoup(schedulePage)
	gamePages = soup2.find_all("table", {"id":"schedule"})
	
	for temp in gamePages[0].find_all("a"):
		if temp.string == "Box Score":
			print(site + temp["href"])
	print("\n")

