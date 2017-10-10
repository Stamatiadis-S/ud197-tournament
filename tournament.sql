-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- First create a database named "tournament" using the psql command: 'CREATE DATABASE tournament;'.
-- Connect to the database.
\c tournament;

-- Drop previously created tables.
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS tournaments_score CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS players CASCADE;

-- Create tables and views.
CREATE TABLE tournaments (
id serial,
name text NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE players (
id serial,
name text NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE tournaments_score (
tournament_id integer,
player_id integer,
wins integer DEFAULT 0,
matches integer DEFAULT 0,
FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
FOREIGN KEY (player_id) REFERENCES players (id),
PRIMARY KEY (tournament_id, player_id)
);

CREATE TABLE matches (
id serial,
tournament_id integer,
winner_id integer,
loser_id integer,
FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
FOREIGN KEY (winner_id) REFERENCES players (id),
FOREIGN KEY (loser_id) REFERENCES players (id),
PRIMARY KEY (tournament_id, winner_id, loser_id)
);