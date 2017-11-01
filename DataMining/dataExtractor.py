from bs4 import BeautifulSoup
import urllib2
import sqlite3

gSite = "https://www.basketball-reference.com"
gSeasonPage = gSite + "/leagues/NBA_2017_games.html"
gTeamsPage = gSite + "/teams/"

gDB = "../DataStorage/db/data.db"

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

def InsertTeam(teamName):
	inserted = False
	conn = sqlite3.connect(gDB)
	cur = conn.cursor()

	cur.execute("SELECT id FROM teams WHERE name = :teamname", {"teamname":teamName})
	if cur.fetchone() == None:
		cur.execute("INSERT INTO teams (name) VALUES ('"+teamName+"')")
		conn.commit()
		inserted = True
	conn.close()
	return inserted;

def ExtractTeams(BRTeamsWebPage):
	req = urllib2.Request(BRTeamsWebPage)
	resp = urllib2.urlopen(req)
	page = resp.read()

	soup = BeautifulSoup(page)
	activeTeams = soup.find_all("table", {"id":"teams_active"})
	currentTeams = activeTeams[0].find_all("tr", class_="full_table")
	for team in currentTeams:
		#insert into db
		if InsertTeam(team.find_all("a")[0].string) == True:
			print("Team '"+team.find_all("a")[0].string+"' inserted successfully to the database.")
		else:
			print("Team '"+team.find_all("a")[0].string+"' was NOT inserted to the database. It is already inside it.")
	return;

def ExtractGameRecord(BRGameWebPage):
	req = urllib2.Request(BRSeasonWebPage)
	resp = urllib2.urlopen(req)
	page = resp.read()

	soup = BeautifulSoup(page)

	
	
	return;

ExtractTeams(gTeamsPage)
#print(GetScheduleGamesPages(gSeasonPage))

