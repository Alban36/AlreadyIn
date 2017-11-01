from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re
from datetime import datetime

gSite = "https://www.basketball-reference.com"
gSeasonPage = gSite + "/leagues/NBA_2017_games.html"
gTeamsPage = gSite + "/teams/"

gDB = "../DataStorage/db/data.db"

gExtractTeams = False;

#Retrieve the web pages containing the games records of the entire season schedule
def GetScheduleGamesPages(BRSeasonWebPage):
	print("Extracting games pages links ...")
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
				results.append(gSite + temp["href"])
	print("DONE.")
	return results;

#Insert a new team into the DB
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

#Read the list of the team from the teams page of BR and insert them if necessary into the DB
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

#Convert a word date to date type
def StrToDate(value):
	tokens = re.findall(r"[\w']+",value)

	month = tokens[0];
	if month.lower() == "january":
		month = "01"
	elif month.lower() == "february": 
		month = "02"
	elif month.lower() == "march": 
		month = "03"
	elif month.lower() == "april": 
		month = "04"
	elif month.lower() == "may": 
		month = "05"
	elif month.lower() == "june": 
		month = "06"
	elif month.lower() == "july": 
		month = "07"
	elif month.lower() == "august": 
		month = "08"
	elif month.lower() == "september": 
		month = "09"
	elif month.lower() == "october": 
		month = "10"
	elif month.lower() == "november": 
		month = "11"
	elif month.lower() == "december": 
		month = "12"

	return datetime.strptime(tokens[2]+' '+tokens[1]+' '+month,'%Y %d %m');

#Extract the games data and games records and store them in the db
def ExtractGameRecord(BRGameWebPage):
	awayTeam = ""
	homeTeam = ""
	date = ""

	print("Extracting game record for page "+BRGameWebPage+" ...")
	req = urllib2.Request(BRGameWebPage)
	resp = urllib2.urlopen(req)
	page = resp.read()

	if not page:
		print("Error : webpage "+BRGameWebPage+" is empty. Data cannot be extracted.")	
		return;

	soup = BeautifulSoup(page)

	description = soup.find_all("meta", {"name":"Description"})
	if description != None:
		#here extract from description the home team, the away team and the date
		print(description[0]["content"])
		text = description[0]["content"]
		fp = text.find(" (");
		vs = text.find("vs. ");
		lp = text.rfind(" (");
		lt = text.rfind("- ");	

		awayTeam = text[12:fp]
		homeTeam = text[vs+4:lp]
		date = text[lt+2:]

		print(awayTeam)
		print(homeTeam)	
		print(date)
	else:
		print("Error: could not find game description")
	print("DONE.")
	return;

#Extracting teams if necessary (it shoudln't once done once)
if gExtractTeams==True:
	ExtractTeams(gTeamsPage)

date = StrToDate("October 1, 2016")

print(date)
#games_pages_list = GetScheduleGamesPages(gSeasonPage)
#for game_page in games_pages_list:
#	ExtractGameRecord(game_page)

