from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from models import db, Vehicle, Database, User, IdealVehicle # database model imported here too 
import usermanagement as dbHandler
import sqlite3 as sql
import time
import random
import bcrypt

def init_routes(app):

    #menu page
    @app.route('/menu', methods=['GET'])
    @app.route('/', methods=['GET'])
    def menu():
        popup = request.args.get('popup')
        ActiveUser=request.args.get('ActiveUser')
        users = User.query.all()
        if ActiveUser is not None:
            userid = request.args.get('userid')
            if userid is not None:
                return render_template('menu.html', ActiveUser=ActiveUser, userid=userid, users=users)
            else:
                return render_template('menu.html', ActiveUser=ActiveUser, users=users)
        else:
            return render_template('menu.html', ActiveUser="Guest", users=users)
    

    #view all vehicles in database
    @app.route('/index', methods=['GET'])
    def index():
        if request.args.get('name') is not None:
            name = request.args.get('name')
            vehicles = Vehicle.query.filter(Vehicle.name.ilike(f'%{name}%')).all()
        else:
            vehicles = Vehicle.query.all()
        return render_template('index.html', vehicles=vehicles)
    

    #user profile loader to view and edit current user's details
    @app.route('/user_profile', methods=['GET'])
    def user_profile():
        con = sql.connect("instance/collection.db")
        cur = con.cursor()
        ActiveUser = request.args.get('ActiveUser')
        uid = request.args.get('userid')
        uid = int(uid)
        username = ActiveUser
        user = User.query.get(username)
        if ActiveUser is not None:
            if uid >0:
                user = User.query.get(uid)
                return render_template('user_profile.html', user = user, ActiveUser=ActiveUser)
            else:
                return redirect(url_for('menu', ActiveUser=ActiveUser, popup="No User ID"))
        else:
            return redirect(url_for('menu', ActiveUser="Guest", popup="Guest User"))
        

    #Edit User
    @app.route('/edit_user', methods=['GET', 'POST'])
    def edit_user():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        #get user
        id = request.args.get('id')
        user = User.query.get(id)

        if request.method == 'GET':
            return render_template('edit_user.html', user = user, ActiveUser=ActiveUser, userid=userid)
        
        if request.method == 'POST':
            salt = bcrypt.gensalt()
            
            
            id = request.form["id"]
        
            user = User.query.get(id)
            user.profile_pic = request.form.get("Profile Picture")
            user.username = request.form.get("Username")
            password = request.form.get("Password")
            hashedpassword = bcrypt.hashpw(password.encode("utf-8"), salt)
            user.password = hashedpassword
            db.session.commit()

            userid=request.form.get("userid")
            ActiveUser=request.form.get("ActiveUser")
            return redirect(url_for('user_profile', ActiveUser=ActiveUser, userid=userid))


    #view all databases
    @app.route('/databases', methods=['GET'])
    def databases():
        ActiveUser=request.args.get('ActiveUser')
        userid=request.args.get('userid')
        if request.args.get('userid') is not None:
            userid = request.args.get('userid')
            databases = Database.query.filter(Database.userid.ilike(f'%{userid}%')).all()
        else:
            databases = Database.query.all()
        return render_template('databases.html', databases=databases, ActiveUser=ActiveUser, userid=userid)
    
    #view vehicle details
    @app.route('/view_vehicle', methods=['GET'])
    def view_vehicle():
        ActiveUser=request.args.get('ActiveUser')
        userid=request.args.get('userid')
        id = request.args.get('id')
        vehicle = Vehicle.query.get(id)
        return render_template('view_vehicle.html', vehicle = vehicle, ActiveUser=ActiveUser, userid=userid)
    

    #view contents of one database
    @app.route('/view_database', methods=['GET'])
    def view_database():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        dbid = request.args.get('dbid')
        database = Database.query.get(dbid)
        if request.args.get('name') is not None:
            name = request.args.get('name')
            vehicles = Vehicle.query.filter((Vehicle.name.ilike(f'%{name}%')), (Vehicle.databaseid.ilike(f'%{dbid}%'))).all()
        else:
            vehicles = Vehicle.query.filter(Vehicle.databaseid.ilike(f'%{dbid}%')).all()
        return render_template('view_database.html', database = database, vehicles = vehicles, databases = Database.query.all(), ActiveUser=ActiveUser, userid=userid)

    #add vehicle
    @app.route('/add_vehicle', methods=['POST'])
    def add_vehicle():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        newvehicle = Vehicle(
            image = request.form.get("Image"),
            name = request.form.get("Name"),
            quote = request.form.get("Quote"),
            description = request.form.get("Description"),
            odometer = request.form.get("Odometer"),
            owner = request.form.get("Owner"),
            type = request.form.get("Type"),
            make = request.form.get("Make"),
            model = request.form.get("Model"),
            year = request.form.get("Year"),
            features = request.form.get("Features"),
            currentissues = request.form.get("CurrentIssues"),
            previousissues = request.form.get("PreviousIssues"),
            databaseid = request.form.get("databaseid")
            )
        db.session.add(newvehicle)
        db.session.commit()
        
        return redirect(url_for('view_database', dbid = request.form.get("databaseid"), userid=userid))

    #add a database
    @app.route('/add_database', methods=['POST'])
    def add_database():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        databases = Database.query.all()
        counter = 1
        for i in databases:
            counter = counter + 1

        newdatabase = Database(
            image = request.form.get("Image"),
            name = request.form.get("Name"),
            description = request.form.get("Description"),
            databaseid = counter
            )
        db.session.add(newdatabase)
        db.session.commit()
        
        return redirect(url_for('databases', userid=userid))

    #edit database
    @app.route('/edit_database', methods=['GET', 'POST'])
    def edit_database():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        user = User.query.get(userid)
        #get database
        id = request.args.get('id')
        database = Database.query.get(id)

        if request.method == 'GET':
            return render_template('edit_database.html', database = database, ActiveUser=ActiveUser, userid=userid, user=user)
    
        if request.method == 'POST':
            
            id = request.form["id"]
            database = Database.query.get(id)
            database.image = request.form.get("Image")
            database.name = request.form.get("Name")
            database.description = request.form.get("Description")
            
            db.session.commit()

            userid=request.form.get("userid")
            ActiveUser=request.form.get("ActiveUser")
            return redirect(url_for('databases', ActiveUser=ActiveUser, userid=userid))


    #edit vehicle
    @app.route('/edit_vehicle', methods=['GET', 'POST'])
    def edit_vehicle():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        user = User.query.get(userid)
        #get vehicle
        id = request.args.get('id')
        vehicle = Vehicle.query.get(id)

        if request.method == 'GET':
            return render_template('edit_vehicle.html', vehicle = vehicle, ActiveUser=ActiveUser, user=user)
    
        if request.method == 'POST':
            
            id = request.form["id"]
            vehicle = Vehicle.query.get(id)
            vehicle.image = request.form.get("Image")
            vehicle.name = request.form.get("Name")
            vehicle.alias = request.form.get("Alias")
            vehicle.quote = request.form.get("Quote")
            vehicle.description = request.form.get("Description")
            vehicle.odometer = request.form.get("Odometer")
            vehicle.owner = request.form.get("Owner")
            vehicle.type = request.form.get("Type")
            vehicle.make = request.form.get("Make")
            vehicle.model = request.form.get("Model")
            vehicle.year = request.form.get("Year")
            vehicle.features = request.form.get("Features")
            vehicle.currentissues = request.form.get("CurrentIssues")
            vehicle.previousissues = request.form.get("PreviousIssues")
                
            db.session.commit()
            userid=request.form.get("userid")
            ActiveUser=request.form.get("ActiveUser")
            return redirect(url_for('databases', ActiveUser=ActiveUser, userid=userid))
        

    #delete database
    @app.route('/delete_database', methods=['GET'])
    def delete_database():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        id = request.args.get('id')
        database = Database.query.get(id)
        db.session.delete(database)
        db.session.commit()

        return redirect(url_for('databases', userid=userid))

    #delete vehicle
    @app.route('/delete_vehicle', methods=['GET'])
    def delete_vehicle():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        id = request.args.get('id')
        dbid = request.args.get('dbid')
        vehicle = Vehicle.query.get(id)
        db.session.delete(vehicle)
        db.session.commit()

        return redirect(url_for('view_database', dbid = dbid, userid=userid))

    #creates new user; receives information from signup from and adds data to Users
    @app.route('/signup', methods=["GET", "POST", "PUT", "POST", "DELETE"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            profile_pic = request.form["profile_pic"]
            Day = request.form["Day"]
            Month = request.form["Month"]
            Year = request.form["Year"]
            DoB = (f"{Day} {Month} {Year}")
            dbHandler.insertUser(username, password, profile_pic, DoB)
            return render_template('signin.html')
        else:
            return render_template('signup.html')

    #sign in
    @app.route('/signin', methods=["GET", "POST"])
    def signin():
        con = sql.connect("instance/collection.db")
        cur = con.cursor()
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            isLoggedIn = dbHandler.retrieveUsers(username, password)
            if isLoggedIn:
                cur.execute("SELECT id FROM user WHERE username = ?", [username])
                userid = cur.fetchone()
                return redirect(url_for('menu', ActiveUser=username, state=isLoggedIn, userid=userid))
            else:
                return redirect(url_for('menu', ActiveUser="Guest"))
        else:
            return render_template('signin.html', ActiveUser="Guest")
            
            
    @app.route('/quiz', methods=['GET','POST'])
    def quiz():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')

        if request.method == 'GET':
            return render_template('quiz.html', ActiveUser=ActiveUser, userid=userid)
        
        if request.method == 'POST':
            con = sql.connect("instance/collection.db")
            cur = con.cursor()

            options = {"Sports Car": 0, "Sedan": 0, "Hatchback": 0, "Station Wagon": 0, "Minivan": 0, "Van": 0, "SUV": 0, "Ute": 0}
            

            Residence = request.form["Residence"]
            People = request.form["People"]
            Purpose = request.form["Purpose"]
            Towing = request.form["Towing"]
            Carry = request.form["Carry"]
            
            #First Question: Residence
            if Residence == "Suburbs": 
                options["Sports Car"] += 3
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 2


            elif Residence == "Outskirts":
                options["Sports Car"] += 3
                options["Sedan"] += 2
                options["Hatchback"] += 2
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 2
                

            elif Residence == "City":
                options["Sports Car"] += 3
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 2
                options["Minivan"] += 2
                options["Van"] += 2
                options["SUV"] += -1
                options["Ute"] += 0


            elif Residence == "Far From Town":
                options["Sports Car"] += 2
                options["Sedan"] += 2
                options["Hatchback"] += 2
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 3
                options["SUV"] += 2
                options["Ute"] += 2
                

            elif Residence == "Farm":
                options["Sports Car"] += 1
                options["Sedan"] += 1
                options["Hatchback"] += 1
                options["Station Wagon"] += 2
                options["Minivan"] += 1
                options["Van"] += 2
                options["SUV"] += 3
                options["Ute"] += 3


            #Second Question: People
            if People == "1": 
                options["Sports Car"] += 3
                options["Sedan"] += 2
                options["Hatchback"] += 3
                options["Station Wagon"] += 1
                options["Minivan"] += 1
                options["Van"] += 2
                options["SUV"] += -1
                options["Ute"] += 1


            elif People == "2": 
                options["Sports Car"] += 3
                options["Sedan"] += 2
                options["Hatchback"] += 3
                options["Station Wagon"] += 2
                options["Minivan"] += 1
                options["Van"] += 2
                options["SUV"] += -1
                options["Ute"] += 1


            elif People == "3-5": 
                options["Sports Car"] += -5
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 3
                options["Minivan"] += 2
                options["Van"] += 2
                options["SUV"] += 1
                options["Ute"] += 1


            elif People == "5-6": 
                options["Sports Car"] += -5
                options["Sedan"] += 1
                options["Hatchback"] += 1
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 3
                options["SUV"] += 2
                options["Ute"] += 1


            elif People == "7+": 
                options["Sports Car"] += -5
                options["Sedan"] += -5
                options["Hatchback"] += -5
                options["Station Wagon"] += 1
                options["Minivan"] += 3
                options["Van"] += 3
                options["SUV"] += 2
                options["Ute"] += -5



            #Third Question: Purpose
            if Purpose == "Daily Runabout": 
                options["Sports Car"] += -1
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 2
                options["Minivan"] += 2
                options["Van"] += 2
                options["SUV"] += 1
                options["Ute"] += 1


            elif Purpose == "Family Daily Runabout":
                options["Sports Car"] += 0
                options["Sedan"] += 2
                options["Hatchback"] += 2
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 1
                options["SUV"] += 1
                options["Ute"] += 0

            
            elif Purpose == "Farm Vehicle": 
                options["Sports Car"] += -3
                options["Sedan"] += -1
                options["Hatchback"] += -1
                options["Station Wagon"] += 0
                options["Minivan"] += 0
                options["Van"] += 2
                options["SUV"] += 3
                options["Ute"] += 3

            
            elif Purpose == "Fun": 
                options["Sports Car"] += 3
                options["Sedan"] += 2
                options["Hatchback"] += 2
                options["Station Wagon"] += 1
                options["Minivan"] += -1
                options["Van"] += -1
                options["SUV"] += -1
                options["Ute"] += -1


            elif Purpose == "Off-Road": 
                options["Sports Car"] += -6
                options["Sedan"] += -5
                options["Hatchback"] += -6
                options["Station Wagon"] += -3
                options["Minivan"] += -4
                options["Van"] += -3
                options["SUV"] += 5
                options["Ute"] += 5


            elif Purpose == "Utility": 
                options["Sports Car"] += -3
                options["Sedan"] += -1
                options["Hatchback"] += -1
                options["Station Wagon"] += 1
                options["Minivan"] += 0
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 3
                

            elif Purpose == "Workhorse": 
                options["Sports Car"] += -2
                options["Sedan"] += -1
                options["Hatchback"] += 0
                options["Station Wagon"] += 1
                options["Minivan"] += 0
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 3
                

            #Fourth Question: Towing
            if Towing == "Never": 
                options["Sports Car"] += 3
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 3
                options["Minivan"] += 3
                options["Van"] += 2
                options["SUV"] += 1
                options["Ute"] += 2


            elif Towing == "Yearly": 
                options["Sports Car"] += 2
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 3
                options["Minivan"] += 2
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 2


            elif Towing == "Semi-Yearly": 
                options["Sports Car"] += 1
                options["Sedan"] += 2
                options["Hatchback"] += 1
                options["Station Wagon"] += 2
                options["Minivan"] += 2
                options["Van"] +=  3
                options["SUV"] += 2
                options["Ute"] += 2
                

            elif Towing == "Quarterly": 
                options["Sports Car"] += 0
                options["Sedan"] += 2
                options["Hatchback"] += 1
                options["Station Wagon"] += 2
                options["Minivan"] += 2
                options["Van"] += 2
                options["SUV"] += 2
                options["Ute"] += 2
                

            elif Towing == "Monthly": 
                options["Sports Car"] += -2
                options["Sedan"] += 0
                options["Hatchback"] += -1
                options["Station Wagon"] += 1
                options["Minivan"] += 0
                options["Van"] += 0
                options["SUV"] += 3
                options["Ute"] += 3
                

            elif Towing == "Every Week": 
                options["Sports Car"] += -3
                options["Sedan"] += -1
                options["Hatchback"] += 0
                options["Station Wagon"] += 1
                options["Minivan"] += 0
                options["Van"] += 1
                options["SUV"] += 3
                options["Ute"] += 3
                

            elif Towing == "Every Day": 
                options["Sports Car"] += -2
                options["Sedan"] += 1
                options["Hatchback"] += 0
                options["Station Wagon"] +=1
                options["Minivan"] +=0
                options["Van"] += 1
                options["SUV"] += 3
                options["Ute"] += 3


            #Fifth Question: Carry
            if Carry == "Strong No": 
                options["Sports Car"] += 3
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 2
                options["Minivan"] += 1
                options["Van"] += 0
                options["SUV"] += -1
                options["Ute"] += 0

            elif Carry == "No": 
                options["Sports Car"] += 2
                options["Sedan"] += 3
                options["Hatchback"] += 3
                options["Station Wagon"] += 2
                options["Minivan"] += 2
                options["Van"] += 1
                options["SUV"] += 0
                options["Ute"] += 1

            elif Carry == "Yes": 
                options["Sports Car"] += 1
                options["Sedan"] += 1
                options["Hatchback"] += 2
                options["Station Wagon"] += 3
                options["Minivan"] += 2
                options["Van"] += 3
                options["SUV"] += 1
                options["Ute"] += 2

            elif Carry == "Strong Yes": 
                options["Sports Car"] += 0
                options["Sedan"] += 1
                options["Hatchback"] += 0
                options["Station Wagon"] += 3
                options["Minivan"] += 2
                options["Van"] += 3
                options["SUV"] += 3
                options["Ute"] += 3


            highest = max(options, key=options.get)
        

            rank = sorted(options.items(), key=lambda item: item[1], reverse=True)
            rank = dict(rank)
            vehicle = rank.keys
            ranked = rank.values

            ideal = IdealVehicle.query.filter(IdealVehicle.name.ilike(f'{highest}')).all()
            return render_template('quiz.html', ideal = ideal, rank = rank, Residence=Residence, People=People, Purpose=Purpose, Towing=Towing, Carry=Carry, highest=highest, options = options, ranked = ranked, vehicle = vehicle)

    
    @app.route('/quiz_questions', methods=['GET', 'POST'])
    def quiz_questions():
        userid=request.args.get('userid')
        ActiveUser=request.args.get('ActiveUser')
        id=userid
        user = User.query.get(id)
        if request.method == 'GET':
            return render_template('quiz_questions.html', ActiveUser=ActiveUser, userid=userid, user=user)


