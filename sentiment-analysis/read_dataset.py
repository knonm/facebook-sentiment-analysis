import sqlite3

conn = sqlite3.connect("/home/knonm/git/dataset/tweets.sqlite")
c = conn.cursor()

c.execute("SELECT * FROM Tweet")
tweets = c.fetchall()

for i in tweets:
    
