import sqlite3 as sql
import time
import random
import bcrypt

def insertUser(username, password, profile_pic, DoB):
    con = sql.connect("instance/collection.db")
    cur = con.cursor()
    salt = bcrypt.gensalt()
    hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
    cur.execute(
        "INSERT INTO user (username,password,profile_pic,DateofBirth) VALUES (?,?,?,?)",
        (username, hashedpassword, profile_pic, DoB),
    )
    con.commit()
    con.close()

def retrieveUser(username):
    con = sql.connect("instance/collection.db")
    cur = con.cursor()
    #SQL injection fix
    cur.execute("SELECT * FROM user WHERE username = ?",[username])
    result = cur.fetchone()
    if result is None:
        con.close()
        return False

def retrieveUsers(username, password):
    con = sql.connect("instance/collection.db")
    cur = con.cursor()
    #SQL injection fix
    cur.execute("SELECT * FROM user WHERE username = ?",[username])
    result = cur.fetchone()
    if result is None:
        con.close()
        return False
    
    #hashedpassword equals the result from the 3rd database column (where passwords are stored)
    hashedpassword = result[3]
    #checks user-inputted password against stored password
    if bcrypt.checkpw(password.encode("utf-8"), hashedpassword):
        cur.execute("SELECT * FROM user WHERE password = ?",[hashedpassword])
        # Plain text log of visitor count as requested by Unsecure PWA management
        #with open("visitor_log.txt", "r") as file:
            #number = int(file.read().strip())
            #number += 1
        #with open("visitor_log.txt", "w") as file:
            #file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True
