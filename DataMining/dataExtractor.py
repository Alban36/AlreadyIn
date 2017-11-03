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

	soup = BeautifulSoup(page,"lxml")
	schedule_pages = soup.find_all("div", class_="filter")

	links = schedule_pages[0].find_all("a")

	for link in links:
		scheduleLink = gSite + link["href"]
		schedulePage = urllib2.urlopen(scheduleLink)
		soup2 = BeautifulSoup(schedulePage,"lxml")
		gamePages = soup2.find_all("table", {"id":"schedule"})
		for temp in gamePages[0].find_all("a"):
			if temp.string == "Box Score":
				results.append(gSite + temp["href"])
	print("DONE.")
	return results;

#Insert a new team into the DB if not existing
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

#Insert a new player into the DB if not existing
def InsertPlayer(playerName, conn):
	inserted = False
	cur = conn.cursor()

	cur.execute("SELECT id FROM players WHERE name = :playername", {"playername":playerName})
	if cur.fetchone() == None:
		cur.execute("INSERT INTO teams (name) VALUES ('"+teamName+"')")
		conn.commit()
		inserted = True
	return inserted;

#Insert a new game into the DB if not existing
def InsertGame(gameStruct):
	inserted = False
	conn = sqlite3.connect(gDB)
	cur = conn.cursor()

	cur.execute("SELECT id FROM games WHERE name = :teamname", {"teamname":teamName})
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

	soup = BeautifulSoup(page,"lxml")
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
	awayTeam = None
	homeTeam = None
	date = None

	print("Extracting game record for page "+BRGameWebPage+" ...")
	req = urllib2.Request(BRGameWebPage)
	resp = urllib2.urlopen(req)
	page = resp.read()

	if not page:
		print("Error : webpage "+BRGameWebPage+" is empty. Data cannot be extracted.")	
		return;

	#extract game information (home team, away team and date)
	soup = BeautifulSoup(page,"lxml")

	description = soup.find_all("meta", {"name":"Description"})
	if description != None:
		#here extract from description the home team, the away team and the date
		text = description[0]["content"]
		fp = text.find(" (");
		vs = text.find("vs. ");
		lp = text.rfind(" (");
		lt = text.rfind("- ");	

		#Description data here
		awayTeam = text[12:fp]
		homeTeam = text[vs+4:lp]
		date = StrToDate(text[lt+2:])

		print("Away: "+awayTeam+" - Home: "+homeTeam)
		print(date)
	else:
		print("Error: could not find game description")
	
	#extract game record
	statsTables = soup.find_all("tbody")
	
	#extract away team stats
	awayStatsTable = statsTables[0]
	
	statsLines = awayStatsTable.find_all("tr")
	for statsLine in statsLines:
		if statsLine.has_attr("class") == False:
			playerName = statsLine.find_all("a")[0].text
			mp = statsLine.find_all("td", {"data-stat":"mp"})[0].text
			fg = statsLine.find_all("td", {"data-stat":"fg"})[0].text
			fga = statsLine.find_all("td", {"data-stat":"fga"})[0].text
			fg3 = statsLine.find_all("td", {"data-stat":"fg3"})[0].text
			fg3a = statsLine.find_all("td", {"data-stat":"fg3a"})[0].text
			ft = statsLine.find_all("td", {"data-stat":"ft"})[0].text
			fta = statsLine.find_all("td", {"data-stat":"fta"})[0].text
			orb = statsLine.find_all("td", {"data-stat":"orb"})[0].text
			drb = statsLine.find_all("td", {"data-stat":"drb"})[0].text
			ast = statsLine.find_all("td", {"data-stat":"ast"})[0].text
			stl = statsLine.find_all("td", {"data-stat":"stl"})[0].text
			blk = statsLine.find_all("td", {"data-stat":"blk"})[0].text
			tov = statsLine.find_all("td", {"data-stat":"tov"})[0].text
			pf = statsLine.find_all("td", {"data-stat":"pf"})[0].text
			pm = statsLine.find_all("td", {"data-stat":"plus_minus"})[0].text
			
			print(playerName+"|"+mp+"|"+fg+"|"+fga+"|"+fg3+"|"+fg3a+"|"+ft+"|"+fta+"|"+orb+"|"+drb+"|"+ast+"|"+stl+"|"+blk+"|"+tov+"|"+pf+"|"+pm)

	print("\n***************\n")
	#extract home team stats
	homeStatsTable = statsTables[2]
	
	statsLines = homeStatsTable.find_all("tr")
	for statsLine in statsLines:
		if statsLine.has_attr("class") == False:
			playerName = statsLine.find_all("a")[0].text
			mp = statsLine.find_all("td", {"data-stat":"mp"})[0].text
			fg = statsLine.find_all("td", {"data-stat":"fg"})[0].text
			fga = statsLine.find_all("td", {"data-stat":"fga"})[0].text
			fg3 = statsLine.find_all("td", {"data-stat":"fg3"})[0].text
			fg3a = statsLine.find_all("td", {"data-stat":"fg3a"})[0].text
			ft = statsLine.find_all("td", {"data-stat":"ft"})[0].text
			fta = statsLine.find_all("td", {"data-stat":"fta"})[0].text
			orb = statsLine.find_all("td", {"data-stat":"orb"})[0].text
			drb = statsLine.find_all("td", {"data-stat":"drb"})[0].text
			ast = statsLine.find_all("td", {"data-stat":"ast"})[0].text
			stl = statsLine.find_all("td", {"data-stat":"stl"})[0].text
			blk = statsLine.find_all("td", {"data-stat":"blk"})[0].text
			tov = statsLine.find_all("td", {"data-stat":"tov"})[0].text
			pf = statsLine.find_all("td", {"data-stat":"pf"})[0].text
			pm = statsLine.find_all("td", {"data-stat":"plus_minus"})[0].text
			
			print(playerName+"|"+mp+"|"+fg+"|"+fga+"|"+fg3+"|"+fg3a+"|"+ft+"|"+fta+"|"+orb+"|"+drb+"|"+ast+"|"+stl+"|"+blk+"|"+tov+"|"+pf+"|"+pm)

	print("DONE.")
	return;

#Extracting teams if necessary (it shoudln't once done once)
if gExtractTeams==True:
	ExtractTeams(gTeamsPage)

#games_pages_list = GetScheduleGamesPages(gSeasonPage)
#for game_page in games_pages_list:
#	ExtractGameRecord(game_page)
ExtractGameRecord("https://www.basketball-reference.com/boxscores/201610250GSW.html")
