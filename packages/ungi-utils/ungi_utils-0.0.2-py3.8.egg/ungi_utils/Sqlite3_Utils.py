#!/usr/bin/env python3

"""
UNGI - Unseen Giants Intelligence
This script is for CRUD operations.
"""

import sqlite3
from hashlib import sha256
def hash_(str_in):
    return sha256(bytes(str_in, encoding="utf8")).hexdigest()
from urllib.parse import urlparse
def get_path(url):
    """
    used to return the telegram
    group name.
    """
    name = urlparse(url)
    return name.path.split("/")[1]
def db_init(path, sql_file):
    """
    used for setup (main.py -i)
    reads in a sql file conatining sql commands to
    setup the sqlite3 database.
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        with open(sql_file, "r", encoding="utf-8") as script_file:
            script_sql = script_file.read()
        cur.executescript(script_sql)
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(e)


def create_operation(path, name, description=None):
    """
    Ops are used as a way to track which entities belong to a
    Mission/Operation. its to prevent all the data from globing together
    """
    try:
        if description is None:
            discription = "No dscription provided"
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO operations(operation_name, operation_description) VALUES(?,?)", (name, description))
        conn.commit()
        return {"Status": "True"}
    except sqlite3.IntegrityError as duplicate_op:
        return {"Status": "Error Duplicate"}

def add_subreddit(path, subreddit, operation_id):
    """
    Adds a Subbreddit to the database.
    Requires: Subreddit name, db path, operation id
    the reddit bot will select all subreddits from the table and scrape them.
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("""INSERT INTO reddit(subreddit, operation_id) VALUES(?,?)""", (subreddit, operation_id))
        conn.commit()
        return {"Status": "True"}
        conn.close()
    except sqlite3.IntegrityError as e:
        print(e)
        return {"Status": "Error Duplicate"}


def list_ops(path):
    """
    List Operations
    only requires a path to the database
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        ops = cur.execute("SELECT operation_id, operation_name, alert_level FROM operations")
        data = ops.fetchall()
        return data
        print(ops.fetchall())
        conn.close()
    except sqlite3.DataError as e:
        print(e)


def set_alert(path, operation_id, level):
    """
    Used to update an alert level to a new one
    Alerts are from 0-100
    if a alert is greater or eq to alert level
    an alert is sent

    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("UPDATE operations SET alert_level = ? WHERE operation_id = ? ", (level, operation_id))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(e)
def get_alert_level(path, operation_id):
    """
    used to get get alert level
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        level = cur.execute("SELECT alert_level FROM operations WHERE operation_id = ?", (operation_id,))
        return level.fetchone()
    except sqlite3.DatabaseError as e:
        print(e)

def get_op_id(path, name):
    """
    gets operation id from name
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        op_name = cur.execute("SELECT operation_id FROM operations WHERE operation_name = ?", (name,))
        return op_name.fetchone()
        conn.close()
    except sqlite3.DataError as e:
        print(e)

def list_subreddits(path):
    """
    list monitored subreddits
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM reddit")
        return data.fetchall()
        conn.close()
    except sqlite3.DataError as e:
        print(e)

def add_discord(path, server_id, operation_id):
    """
    We Add a discord Server to the monitor list
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO discord(server_id, operation_id) values(?,?);", (server_id, operation_id))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as duplicate_record:
        print(e)

def list_servers(path):
    """
    Listing Servers.
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        servers =  cur.execute("SELECT * from discord;")
        return servers.fetchall()
    except sqlite3.DataError as e:
        print(e)

def get_op_name(path, id):
    """
    return operation name matching id
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        name = cur.execute("SELECT operation_name FROM operations WHERE operation_id = ?;", (id,))
        return name.fetchone()
    except sqlite3.DataError as e:
        print(e)

def add_watch_word(path, word, operation_id):
    """
    Function used to add a word to the watchlist
    inputs:
    word (string)
    operation_id (int)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO watch_list(word, operation_id) VALUES(?,?)", (word, operation_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("word is already in database.")

def delete_operation(path, operation_id):
    """
    used to remove a operation from the database
    inputs:
    db path (string)
    operation_id (int)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("DELETE FROM operations WHERE operation_id = ?", (operation_id,))
        conn.commit()
    except Exception as e:
        print(e)

def log_user(path, username, source, website, operation_id):
    """
    used to add a user to the loot db
    inputs:
    db path (string)
    operation_id (int)
    source (string)
    hash_id (string)
    """
    # hash id used for data integerty, not for security
    hash_id = hash_(username + source + website)
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, website, source, hash_id, operation_id) VALUES(?,?,?,?,?)", (username, website, source, hash_id, int(operation_id),))
        conn.commit()
    except sqlite3.IntegrityError as duplicate:
        pass

def update_target(path, username, target_number):
    """
    used to update a user to the target list
    inputs:
    db path (string)
    operation_id
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_target = ? WHERE username = ?;", (target_number, username))
        conn.commit()
    except sqlite3.DataError as e:
        print(e)


def add_telegram(path, chan_id, operation_id, name):
    """
    used to add a telegram chat/group
    inputs:
    database path (string)
    chan_id (int)
    operation_id (int)
    name (string)
    """

    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO telegram(chan_id, name, operation_id) VALUES(?,?,?)", (chan_id, name, operation_id))
        conn.commit()
    except sqlite3.IntegrityError as duplicate_chat:
        print(f"{chan_id} {name} Was already in db!")

def list_telegram(path):
    """
    used to list telgram chats
    inputs:
    database path (string)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        data = cur.execute("SELECT chan_id, name, operation_id FROM telegram")
        return data.fetchall()
    except sqlite3.DataError as e:
        print(e)

def add_twitter(path, username, operation_id):
    """
    used to add a twitter account to the database
    inputs:
    database path (string)
    username (string)
    operation_id (int)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("INSERT INTO twitter(username, operation_id) VALUES(?,?)", (username, operation_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"{username} is already in db")

def list_twitter(path):
    """
    used to list monitored twitter accounts
    inputs:
    path (string)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        data = cur.execute("SELECT username, operation_id FROM twitter")
        return data.fetchall()
    except sqlite3.DataError as e:
        print(e)

def move_twitter(path, username, operation_id):
    """
    used to move a twitter username to a differant operation
    inputs:
    path (string)
    username (string)
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("UPDATE twitter SET operation_id = ? WHERE username = ?", (operation_id, username))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Error Moving {username} to operation: {operation_id}\nMost Likly that operation does not exist")


def list_targets(path):
    """
    used to list targets
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        data = cur.execute("SELECT username, source, operation_id FROM users WHERE is_target = 1;")
        return data.fetchall()
    except sqlite3.DataError as e:
        print(e)


def get_words(path):
    """
    used to list watch words
    """
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        data = cur.execute("SELECT word, operation_id FROM watch_list")
        return data.fetchall()
    except sqlite3.DataError as e:
        print(e)
