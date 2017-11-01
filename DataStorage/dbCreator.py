import sqlite3

conn = sqlite3.connect('data.db')

#Create players
conn.execute('''CREATE TABLE players (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT)''')

#Create teams
conn.execute('''CREATE TABLE teams (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT
		city TEXT)''')

#Create game_records
conn.execute('''CREATE TABLE game_records (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		player INTEGER,
		team INTEGER,
		SP INTEGER,
		FG INTEGER,
		FGA INTEGER,
		THREEP INTEGER,
		THREEPA INTEGER,
		FT INTEGER,
		FTA INTEGER,
		ORB INTEGER,
		DRB INTEGER,
		AST INTEGER,
		STL INTEGER,
		BLK INTEGER,
		TOV INTEGER,
		PF INTEGER,
		plusminus INTEGER,
		FOREIGN KEY(player) REFERENCES players(id),
		FOREIGN KEY(team) REFERENCES teams(id))''')

#Create games
conn.execute('''CREATE TABLE games (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		date TEXT,
		home_team INTEGER,
		visitor_team INTEGER,
		game_record INTEGER,
		FOREIGN KEY(home_team) REFERENCES teams(id),
		FOREIGN KEY(visitor_team) REFERENCES teams(id),
		FOREIGN KEY(game_record) REFERENCES game_records(id))''')

conn.close()
