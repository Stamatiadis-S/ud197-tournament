-- Table definitions for the tournament project.

-- Move outside tournament database if already connected.
\c postgres;

-- Recreate database and connect.
-- Warning! This erases all previous data under the "tournament" database.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create tables and views.
CREATE TABLE tournaments (
id SERIAL,
name TEXT NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE players (
id SERIAL,
name TEXT NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE tournaments_score (
tournament_id INTEGER,
player_id INTEGER,
wins INTEGER DEFAULT 0,
matches INTEGER DEFAULT 0,
FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
FOREIGN KEY (player_id) REFERENCES players (id),
PRIMARY KEY (tournament_id, player_id)
);

CREATE TABLE matches (
id SERIAL,
tournament_id INTEGER,
winner_id INTEGER,
loser_id INTEGER,
FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
FOREIGN KEY (winner_id) REFERENCES players (id),
FOREIGN KEY (loser_id) REFERENCES players (id),
PRIMARY KEY (tournament_id, winner_id, loser_id)
);
