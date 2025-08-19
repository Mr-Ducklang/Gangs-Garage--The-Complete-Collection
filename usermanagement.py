import sqlite3 as sql
import time
import random
import bcrypt

def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    salt = bcrypt.gensalt()
    hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashedpassword, DoB),
    )
    con.commit()
    con.close()

def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    #SQL injection fix
    cur.execute("SELECT * FROM users WHERE username = ?",[username])
    result = cur.fetchone()
    if result is None:
        con.close()
        return False
    
    #hashedpassword equals the result from the 3rd database column (where passwords are stored)
    hashedpassword = result[2]
    #checks user-inputted password against stored password
    if bcrypt.checkpw(password.encode("utf-8"), hashedpassword):
        cur.execute("SELECT * FROM users WHERE password = ?",[hashedpassword])
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

#Added protection against Cross Site Scripting
def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    feedback = feedback.replace("&","&amp;")
    feedback = feedback.replace("<","&lt;")
    feedback = feedback.replace(">","&gt;")
    feedback = feedback.replace('"',"&quot;")
    feedback = feedback.replace("'", "&#x27;")
    #SQL injection fix
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)",[feedback])
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
