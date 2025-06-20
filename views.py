from flask import render_template, request, redirect, url_for, flash
from models import db, Vehicle, Database # database model imported here too 

def init_routes(app):

    @app.route('/', methods=['GET'])
    def menu():
        return render_template('menu.html')

    @app.route('/database', methods=['GET'])
    def view_databases():
        if request.args.get('name') is not None:
            name = request.args.get('name')
            databases = Database.query.filter(Database.name.ilike(f'%{name}%')).all()
        else:
            databases = Database.query.all()
        return render_template('database.html', databases=databases)
    
    @app.route('/signin', methods=['GET'])
    def signin():
        return render_template('signin.html')
    
    @app.route('/quiz', methods=['GET'])
    def quiz():
        return render_template('quiz.html')
    
    @app.route('/index', methods=['GET'])
    def index():
        if request.args.get('name') is not None:
            name = request.args.get('name')
            vehicles = Vehicle.query.filter(Vehicle.name.ilike(f'%{name}%')).all()
        else:
            vehicles = Vehicle.query.all()
        return render_template('index.html', vehicles=vehicles)