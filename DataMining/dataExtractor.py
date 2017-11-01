from bs4 import BeautifulSoup
import urllib2

gSite = "https://www.basketball-reference.com"
gSeasonPage = gSite + "/leagues/NBA_2017_games.html"

def GetScheduleGamesPages(BRSeasonWebPage):
	results = []

	req = urllib2.Request(BRSeasonWebPage)
	resp = urllib2.urlopen(req)
	page = resp.read()

	soup = BeautifulSoup(page)
	schedule_pages = soup.find_all("div", class_="filter")

	links = schedule_pages[0].find_all("a")

	for link in links:
		scheduleLink = gSite + link["href"]
		schedulePage = urllib2.urlopen(scheduleLink)
		soup2 = BeautifulSoup(schedulePage)
		gamePages = soup2.find_all("table", {"id":"schedule"})
		for temp in gamePages[0].find_all("a"):
			if temp.string == "Box Score":
				results.append(temp["href"])
	return results;

print(GetScheduleGamesPages(gSeasonPage))

