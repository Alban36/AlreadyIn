from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import re
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datetime import datetime
from time import sleep

gSite = "http://stats.nba.com/game/"
gStartGame = "0021600001"
gEndGame = "0021601230"

gDB = "../DataStorage/db/data.db"

gExtractTeams = True;

#Retrieve the web pages containing the games records of the entire season schedule
#OBSOLETE
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
        lId = -1
        lConn = sqlite3.connect(gDB)
        lCur = lConn.cursor()
        
        lIdReq = "SELECT id FROM teams WHERE name = '"+teamName+"'"
        lCur.execute(lIdReq)
        lCurResp = lCur.fetchone()
        if lCurResp == None:
                lCur.execute("INSERT INTO teams (name) VALUES ('"+teamName+"')")
                lConn.commit()
                lCur.execute(lIdReq)
                lId = lCur.fetchone()[0]
        else:
            lId = lCurResp[0] 
        lConn.close()
        return lId;

#Insert a new player into the DB if not existing
def InsertPlayer(pPlayerName,pConn):
        lId = -1
        if pConn==None:
            lConn = sqlite3.connect(gDB)
        else:
            lConn = pConn
        lCur = lConn.cursor()

        lIdReq = 'SELECT id FROM players WHERE name = "'+pPlayerName+'"'
        lCur.execute(lIdReq)
        lCurResp = lCur.fetchone()
        if lCurResp == None:
                lCur.execute('INSERT INTO players (name) VALUES ("'+pPlayerName+'")')
                lConn.commit()
                lCur.execute(lIdReq)
                lId = lCur.fetchone()[0]
        else:
            lId = lCurResp[0]
        if pConn==None:
            lConn.close()
        return lId;

#Insert a new game into the DB if not existing
def InsertGame(pGameStruct):
        lId = -1
        lConn = sqlite3.connect(gDB)
        lCur = lConn.cursor()
        
        lHomeTeamId = InsertTeam(pGameStruct['HomeTeam'])
        lAwayTeamId = InsertTeam(pGameStruct['AwayTeam'])

        lIdReq = lCur.execute("SELECT id FROM games WHERE date = '"+pGameStruct['Date'].strftime("%d-%m-%Y")+"' AND home_team="+str(lHomeTeamId)+" AND visitor_team="+str(lAwayTeamId)).fetchone()
        if lIdReq == None:
                #insert game
                lCur.execute("INSERT INTO games (date,home_team,visitor_team) VALUES ('"+pGameStruct['Date'].strftime("%d-%m-%Y")+"',"+str(lHomeTeamId)+","+str(lAwayTeamId)+")")
                lId = lCur.execute("SELECT id FROM games WHERE date = :date AND home_team=:hometeam AND visitor_team=:awayteam", {"date":pGameStruct['Date'].strftime("%d-%m-%Y"), "hometeam":lHomeTeamId, "awayteam":lAwayTeamId}).fetchone()[0]
                #insert game record
                #AWAY
                for lStatsLine in pGameStruct['Record_awayteam']:
                    lPlayerId = InsertPlayer(lStatsLine['Player'],lConn)
                    lCur.execute("INSERT INTO game_records (game,player,team,SP,FG,FGA,THREEP,THREEPA,FT,FTA,ORB,DRB,AST,STL,BLK,TOV,PF,plusminus) VALUES ("+str(lId)+","+str(lPlayerId)+","+str(lAwayTeamId)+","+lStatsLine['SP']+","+lStatsLine['FG']+","+lStatsLine['FGA']+","+lStatsLine['FG3']+","+lStatsLine['FG3A']+","+lStatsLine['FT']+","+lStatsLine['FTA']+","+lStatsLine['ORB']+","+lStatsLine['DRB']+","+lStatsLine['AST']+","+lStatsLine['STL']+","+lStatsLine['BLK']+","+lStatsLine['TOV']+","+lStatsLine['PF']+","+lStatsLine['PM']+")")
                #HOME
                for lStatsLine in pGameStruct['Record_hometeam']:
                    lPlayerId = InsertPlayer(lStatsLine['Player'],lConn)
                    lCur.execute("INSERT INTO game_records (game,player,team,SP,FG,FGA,THREEP,THREEPA,FT,FTA,ORB,DRB,AST,STL,BLK,TOV,PF,plusminus) VALUES ("+str(lId)+","+str(lPlayerId)+","+str(lHomeTeamId)+","+lStatsLine['SP']+","+lStatsLine['FG']+","+lStatsLine['FGA']+","+lStatsLine['FG3']+","+lStatsLine['FG3A']+","+lStatsLine['FT']+","+lStatsLine['FTA']+","+lStatsLine['ORB']+","+lStatsLine['DRB']+","+lStatsLine['AST']+","+lStatsLine['STL']+","+lStatsLine['BLK']+","+lStatsLine['TOV']+","+lStatsLine['PF']+","+lStatsLine['PM']+")")
                lConn.commit()
                print("Game added to DB !")
        else:
            lId = lIdReq[0]
            print("Game already in the DB at id "+str(lId))
        lConn.close()
        return lId;


#Read the list of the team from the teams page of BR and insert them if necessary into the DB
#OBSOLETE
def ExtractTeams(BRTeamsWebPage):
        print("Extracting teams data ...")
        req = urllib2.Request(BRTeamsWebPage)
        resp = urllib2.urlopen(req)
        page = resp.read()

        soup = BeautifulSoup(page,"lxml")
        activeTeams = soup.find_all("table", {"id":"teams_active"})
        currentTeams = activeTeams[0].find_all("tr", class_="full_table")
        for team in currentTeams:
                #insert into db
                lTeamId = InsertTeam(team.find_all("a")[0].string)
        print("DONE.")
        return;

#Convert a word date to date type
def StrToDate(value):
        tokens = re.findall(r"[\w']+",value)
        
        print(tokens)

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

        lDriver = webdriver.Firefox()
        lDriver.minimize_window()
        lDriver.get(BRGameWebPage)
        try:
            WebDriverWait(lDriver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="nba-stat-table__overflow"]'))
)
        except:
            print("WebDriverWait error:", sys.exc_info()[0])
            
        lPage = lDriver.page_source
        lDriver.quit()

        if not lPage:
                print("Error : webpage "+BRGameWebPage+" is empty. Data cannot be extracted.")        
                return;

        #extract game information (home team, away team and date)
        soup = BeautifulSoup(lPage,"lxml")

        description = soup.find_all("meta", {"name":"description"})
        if description != None:
                #here extract from description the home team, the away team and the date
                text = description[0]["content"]
                print(text)
                startIndex1 = len("NBA Stats Official Boxscore for ")
                endIndex1 = text.find(" @");
                startIndex2 = endIndex1+3
                endIndex2 = text.find(" on");
                startIndex3 = text.find(", ")+2;

                #Description data here
                lGameStruct['AwayTeam'] = text[startIndex1:endIndex1]
                lGameStruct['HomeTeam'] = text[startIndex2:endIndex2]
                lGameStruct['Date'] = StrToDate(text[startIndex3:])
                
                #print(lGameStruct['AwayTeam'])
                #print(lGameStruct['HomeTeam'])
                #print(lGameStruct['Date'])
        else:
                print("Error: could not find game description")
        
        #extract game record
        statsTables = soup.find_all("div",{"class":"nba-stat-table__overflow"})
        
        #extract away team stats
        awayStatsTable = statsTables[0]
        
        lGameStruct['Record_awayteam']=[]
        statsLines = awayStatsTable.find_all("tbody")[0].find_all("tr")
        for statsLine in statsLines:
            lStatsLineStruct = {}
            if not statsLine.find_all("td",{"class":"dnp"}):
                lFields = statsLine.find_all("td")
                lTemp = lFields[0].find_all("a")[0].text
                endIndex = lTemp.find(" <sup>")
                lStatsLineStruct['Player'] = lTemp[:endIndex]
                #convert minutes to seconds
                lMPStr = lFields[1].text
                lMPTokens = lMPStr.split(':')
                lSP = int(lMPTokens[0])*60 + int(lMPTokens[1])
                lStatsLineStruct['SP'] = str(lSP)
                lStatsLineStruct['FG'] = lFields[2].text
                lStatsLineStruct['FGA'] = lFields[3].text
                lStatsLineStruct['FG3'] = lFields[5].text
                lStatsLineStruct['FG3A'] = lFields[6].text
                lStatsLineStruct['FT'] = lFields[8].text
                lStatsLineStruct['FTA'] = lFields[9].text
                lStatsLineStruct['ORB'] = lFields[11].text
                lStatsLineStruct['DRB'] = lFields[12].text
                lStatsLineStruct['AST'] = lFields[14].text
                lStatsLineStruct['TOV'] = lFields[15].text
                lStatsLineStruct['STL'] = lFields[16].text
                lStatsLineStruct['BLK'] = lFields[17].text
                lStatsLineStruct['PF'] = lFields[18].text
                lStatsLineStruct['PM'] = lFields[19].text
                if not lStatsLineStruct['PM']:
                    lStatsLineStruct['PM']="0"
                lGameStruct['Record_awayteam'].append(lStatsLineStruct)
            
        #extract home team stats
        homeStatsTable = statsTables[1]
        
        lGameStruct['Record_hometeam']=[]
        statsLines = homeStatsTable.find_all("tbody")[0].find_all("tr")
        for statsLine in statsLines:
            if not statsLine.find_all("td",{"class":"dnp"}):
                lStatsLineStruct = {}
                lFields = statsLine.find_all("td")
                lTemp = lFields[0].find_all("a")[0].text
                endIndex = lTemp.find(" <sup>")
                lStatsLineStruct['Player'] = lTemp[:endIndex]
                #convert minutes to seconds
                lMPStr = lFields[1].text
                lMPTokens = lMPStr.split(':')
                lSP = int(lMPTokens[0])*60 + int(lMPTokens[1])
                lStatsLineStruct['SP'] = str(lSP)
                lStatsLineStruct['FG'] = lFields[2].text
                lStatsLineStruct['FGA'] = lFields[3].text
                lStatsLineStruct['FG3'] = lFields[5].text
                lStatsLineStruct['FG3A'] = lFields[6].text
                lStatsLineStruct['FT'] = lFields[8].text
                lStatsLineStruct['FTA'] = lFields[9].text
                lStatsLineStruct['ORB'] = lFields[11].text
                lStatsLineStruct['DRB'] = lFields[12].text
                lStatsLineStruct['AST'] = lFields[14].text
                lStatsLineStruct['TOV'] = lFields[15].text
                lStatsLineStruct['STL'] = lFields[16].text
                lStatsLineStruct['BLK'] = lFields[17].text
                lStatsLineStruct['PF'] = lFields[18].text
                lStatsLineStruct['PM'] = lFields[19].text
                if not lStatsLineStruct['PM']:
                    lStatsLineStruct['PM']="0"
                lGameStruct['Record_hometeam'].append(lStatsLineStruct)
            
        #Insert data in DB if not existing
        InsertGame(lGameStruct)
        
        print("DONE.")
        return;


#------#
# test #
#------#
#ExtractGameRecord('http://stats.nba.com/game/0021600005/')

#exit()

#------#
# MAIN #
#------#

lStartTime = datetime.now()

#Initial SavePoint
lSavePoint = gStartGame

#Read the save point if existing
lSkipping = False
try:
    lFile = open("extract.save","r")
    if lFile !=None:
            print("Extraction save exists! Reading save point ...")
            lSavePoint = lFile.readline()
            print("DONE.")
except IOError:
    print("No extraction save. start extraction from the beginning.")

lGame = int(lSavePoint)
lRetry = 0
while lSavePoint != gEndGame:
    
    try:
        ExtractGameRecord(gSite+str(lSavePoint)+"/")
        lGame += 1
        lSavePoint = str(lGame).zfill(10)
        lRetry = 0
    except:
        lRetry += 1
        if lRetry == 4:
            print("Unexpected error:", sys.exc_info()[0])
            print("Saving last game extracted")
            lFile = open("extract.save","w")
            lFile.write(lSavePoint)
            lFile.close()
            break
        else:
            print("Game extraction failed. Retry = "+str(lRetry))

#ExtractGameRecord("https://www.basketball-reference.com/boxscores/201704040IND.html")

lStopTime = datetime.now()
lDeltaTime = lStopTime - lStartTime
print(lDeltaTime)

print("END OF PROGRAM")
