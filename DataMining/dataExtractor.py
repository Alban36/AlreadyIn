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
def InsertGame(pGameStruct):
	lInserted = False
	lConn = sqlite3.connect(gDB)
	lCur = lConn.cursor()

	lCur.execute("SELECT id FROM games WHERE date = :date AND home_team=:hometeam AND visitor_team=:awayteam", [{"date":pGameStruct['Date']}, {"hometeam":pGameStruct['HomeTeam']}, {"awayteam":pGameStruct['AwayTeam']}])
	if lCur.fetchone() == None:
		#cur.execute("INSERT INTO teams (name) VALUES ('"+teamName+"')")
		#conn.commit()
		lInserted = True
	lConn.close()
	return lInserted;


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
	lGameStruct = {};

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
		lGameStruct['AwayTeam'] = text[12:fp]
		lGameStruct['HomeTeam'] = text[vs+4:lp]
		lGameStruct['Date'] = StrToDate(text[lt+2:])
	else:
		print("Error: could not find game description")
	
	#extract game record
	statsTables = soup.find_all("tbody")
	
	#extract away team stats
	awayStatsTable = statsTables[0]
	
	lGameStruct['Record']=[]
	statsLines = awayStatsTable.find_all("tr")
	for statsLine in statsLines:
		if statsLine.has_attr("class") == False:
                        lStatsLineStruct = {}
                        lStatsLineStruct['Player'] = statsLine.find_all("a")[0].text
			lStatsLineStruct['MP'] = statsLine.find_all("td", {"data-stat":"mp"})[0].text
			lStatsLineStruct['FG'] = statsLine.find_all("td", {"data-stat":"fg"})[0].text
			lStatsLineStruct['FGA'] = statsLine.find_all("td", {"data-stat":"fga"})[0].text
			lStatsLineStruct['FG3'] = statsLine.find_all("td", {"data-stat":"fg3"})[0].text
			lStatsLineStruct['FG3A'] = statsLine.find_all("td", {"data-stat":"fg3a"})[0].text
			lStatsLineStruct['FT'] = statsLine.find_all("td", {"data-stat":"ft"})[0].text
			lStatsLineStruct['FTA'] = statsLine.find_all("td", {"data-stat":"fta"})[0].text
			lStatsLineStruct['ORB'] = statsLine.find_all("td", {"data-stat":"orb"})[0].text
			lStatsLineStruct['DRB'] = statsLine.find_all("td", {"data-stat":"drb"})[0].text
			lStatsLineStruct['AST'] = statsLine.find_all("td", {"data-stat":"ast"})[0].text
			lStatsLineStruct['STL'] = statsLine.find_all("td", {"data-stat":"stl"})[0].text
			lStatsLineStruct['BLK'] = statsLine.find_all("td", {"data-stat":"blk"})[0].text
			lStatsLineStruct['TOV'] = statsLine.find_all("td", {"data-stat":"tov"})[0].text
			lStatsLineStruct['PF'] = statsLine.find_all("td", {"data-stat":"pf"})[0].text
			lStatsLineStruct['PM'] = statsLine.find_all("td", {"data-stat":"plus_minus"})[0].text
			lGameStruct['Record'].append(lStatsLineStruct)
	#extract home team stats
	homeStatsTable = statsTables[2]
	
	statsLines = homeStatsTable.find_all("tr")
	for statsLine in statsLines:
		if statsLine.has_attr("class") == False:
			lStatsLineStruct = {}
                        lStatsLineStruct['Player'] = statsLine.find_all("a")[0].text
			lStatsLineStruct['MP'] = statsLine.find_all("td", {"data-stat":"mp"})[0].text
			lStatsLineStruct['FG'] = statsLine.find_all("td", {"data-stat":"fg"})[0].text
			lStatsLineStruct['FGA'] = statsLine.find_all("td", {"data-stat":"fga"})[0].text
			lStatsLineStruct['FG3'] = statsLine.find_all("td", {"data-stat":"fg3"})[0].text
			lStatsLineStruct['FG3A'] = statsLine.find_all("td", {"data-stat":"fg3a"})[0].text
			lStatsLineStruct['FT'] = statsLine.find_all("td", {"data-stat":"ft"})[0].text
			lStatsLineStruct['FTA'] = statsLine.find_all("td", {"data-stat":"fta"})[0].text
			lStatsLineStruct['ORB'] = statsLine.find_all("td", {"data-stat":"orb"})[0].text
			lStatsLineStruct['DRB'] = statsLine.find_all("td", {"data-stat":"drb"})[0].text
			lStatsLineStruct['AST'] = statsLine.find_all("td", {"data-stat":"ast"})[0].text
			lStatsLineStruct['STL'] = statsLine.find_all("td", {"data-stat":"stl"})[0].text
			lStatsLineStruct['BLK'] = statsLine.find_all("td", {"data-stat":"blk"})[0].text
			lStatsLineStruct['TOV'] = statsLine.find_all("td", {"data-stat":"tov"})[0].text
			lStatsLineStruct['PF'] = statsLine.find_all("td", {"data-stat":"pf"})[0].text
			lStatsLineStruct['PM'] = statsLine.find_all("td", {"data-stat":"plus_minus"})[0].text
			lGameStruct['Record'].append(lStatsLineStruct)
        print(lGameStruct)
        #Insert data in DB if not existing
        if InsertGame(lGameStruct):
            print("Game inserted in the DB")
        else:
            print("Game already existing in the DB")
	print("DONE.")
	return;

#Extracting teams if necessary (it shoudln't once done once)
if gExtractTeams==True:
	ExtractTeams(gTeamsPage)

#games_pages_list = GetScheduleGamesPages(gSeasonPage)
#for game_page in games_pages_list:
#	ExtractGameRecord(game_page)
ExtractGameRecord("https://www.basketball-reference.com/boxscores/201610250GSW.html")

#game struct exemple
lGameStruct = {
	'Date':datetime.now(),
	'HomeTeam':'Atlanta Hawks',
	'AwayTeam':'Boston Celtics',
	'Record':[
		{
			'Player':'Toto',
			'sp':48*60,
			'fg':10,
			'fga':20,
			'fg3':0,
			'fg3a':2,
			'ft':2,
			'fta':2,
			'orb':0,
			'drb':4,
			'ast':3,
			'stl':1,
			'tov':1,
			'blk':0,
			'pf':4,
			'pm':6
		},
		{
			'Player':'Tata',
			'sp':12*60,
			'fg':1,
			'fga':9,
			'fg3':0,
			'fg3a':1,
			'ft':2,
			'fta':2,
			'orb':0,
			'drb':2,
			'ast':1,
			'stl':0,
			'tov':2,
			'blk':0,
			'pf':2,
			'pm':-3
		}]}
