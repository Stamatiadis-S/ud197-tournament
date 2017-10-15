#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2

database_name = "tournament"

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection along with a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)

def executeQuery(query, data=None):
    db, cursor = connect()
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    result = cursor.fetchall()
    db.close()
    return result

def commitQuery(query, data=None):
    db, cursor = connect()
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    db.commit()
    db.close()

def deleteMatches(tournament):
    """Remove all the match records from the database for a specific tournament.

    Args:
      tournament: the tournament's id.
    """
    commitQuery("DELETE FROM matches WHERE tournament_id = %s", (tournament,))
    commitQuery("UPDATE tournaments_score SET wins = 0, matches = 0 WHERE tournament_id = %s", (tournament,))

def deletePlayers():
    """Remove all players registered in the database."""
    commitQuery("DELETE FROM players")

def deleteTournaments():
    """Remove all the tournaments from the database."""
    commitQuery("DELETE FROM tournaments_score")
    commitQuery("DELETE FROM matches")
    commitQuery("DELETE FROM tournaments")

def countPlayers():
    """Returns the number of players currently registered in the database."""
    return executeQuery("SELECT COUNT(*) FROM players")[0][0]

def createTournament(name):
    """Adds a tournament to the database.

    Args:
       name: the tournament's name.
    """
    commitQuery("INSERT INTO tournaments (name) VALUES(%s)", (name,))

def createTournamentWithId(id, name):
    """Adds a torunament to the database.

    Args:
       id: the tournament's id.
       name: the tournament's name.
    """
    commitQuery("INSERT INTO tournaments (id, name) VALUES(%s, %s)", (id, name))

def registerPlayer(name):
    """Adds a player to the database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    commitQuery("INSERT INTO players (name) VALUES (%s)", (name,))

def registerPlayerWithId(id, name):
    """Adds a player to the database.

    Args:
      id: the player's id (please choose a unique one).
      name: the player's full name (need not be unique).
    """
    commitQuery("INSERT INTO players (id, name) VALUES (%s, %s)", (id, name))

def joinTournament(player, tournament):
    """Register a player to a specific tournament

    Args:
      player: the player's id.
      tournament: the tournament's id.
    """
    commitQuery("INSERT INTO tournaments_score (tournament_id, player_id) VALUES(%s,%s)", (tournament, player))

def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins for a specific tournament.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      tournament: the tournament's id.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return executeQuery("SELECT player_id, name, wins, matches FROM tournaments_score, players WHERE tournaments_score.player_id = players.id AND tournament_id = %s ORDER BY wins DESC", (tournament,))

def reportMatch(tournament, winner, loser):
    """Records the outcome of a single match between two players for a specific tournament.

    Args:
      tournament: the tournament's id.
      winner: the id number of the player who won.
      loser: the id number of the player who lost.
    """
    commitQuery("INSERT INTO matches (tournament_id, winner_id, loser_id) VALUES (%s, %s, %s)", (tournament, winner, loser))
    commitQuery("UPDATE tournaments_score SET wins = wins + 1, matches = matches + 1 WHERE tournament_id = %s AND player_id = %s", (tournament, winner))
    commitQuery("UPDATE tournaments_score SET matches = matches + 1 WHERE tournament_id = %s AND player_id = %s", (tournament, loser))

def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match for a specific tournament.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament: the tournament's id.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    players = playerStandings(tournament)
    if len(players) < 2:
        raise KeyError("Not enough players.")
    for i in range(0, len(players), 2):
        pairings.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1]))
    return pairings
