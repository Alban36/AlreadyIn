import sqlite3

conn = sqlite3.connect('data.db')

#Create players
conn.exectute('''CREATE TABLE players (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT)''')

#Create teams
conn.exectute('''CREATE TABLE teams (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT
		city TEXT)''')

#Create game_records
conn.exectute('''CREATE TABLE game_records (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		player INTEGER,
		team INTEGER,
		SP INTEGER,
		FG INTEGER,
		FGA INTEGER,
		
		FOREIGN KEY(player) REFERENCES players(id),
		FOREIGN KEY(team) REFERENCES teams(id),
		)''')

#Create games
conn.exectute('''CREATE TABLE games (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		date TEXT,
		home_team INTEGER,
		visitor_team INTEGER,
		game_record INTEGER,
		FOREIGN KEY(home_team) REFERENCES teams(id),
		FOREIGN KEY(visitor_team) REFERENCES teams(id),
		FOREIGN KEY(game_record) REFERENCES game_records(id),
		)''')

conn.close()
