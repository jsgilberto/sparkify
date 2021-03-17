-- Fact table
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL NOT NULL UNIQUE,
	start_time TIMESTAMP,
	user_id INTEGER,
	song_id VARCHAR,
	artist_id VARCHAR,
	session_id INTEGER,
	level VARCHAR,
	location VARCHAR,
	user_agent VARCHAR
);

-- Dimension tables
CREATE TABLE IF NOT EXISTS users (
	user_id INTEGER PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	gender CHAR,
	level VARCHAR
);

CREATE TABLE IF NOT EXISTS songs (
	song_id VARCHAR PRIMARY KEY,
	title VARCHAR,
	artist_id INTEGER,
	year SMALLINT,
	duration FLOAT
);

CREATE TABLE IF NOT EXISTS artists (
	artist_id VARCHAR PRIMARY KEY,
	name VARCHAR,
	location VARCHAR,
	latitude FLOAT,
	longitude FLOAT
);

CREATE TABLE IF NOT EXISTS time (
	start_time TIMESTAMP PRIMARY KEY,
	hour VARCHAR,
	day VARCHAR,
	week VARCHAR,
	month VARCHAR,
	year VARCHAR,
	weekday VARCHAR
);