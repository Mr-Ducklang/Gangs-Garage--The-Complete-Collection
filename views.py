from flask import render_template, request, redirect, url_for, flash
from models import db, Vehicle, Database # database model imported here too 

def init_routes(app):

    #menu page
    @app.route('/', methods=['GET'])
    def menu():
        return render_template('menu.html')
    

    #view databases
    @app.route('/database', methods=['GET'])
    def view_databases():
        if request.args.get('name') is not None:
            name = request.args.get('name')
            databases = Database.query.filter(Database.name.ilike(f'%{name}%')).all()
        else:
            databases = Database.query.all()
        return render_template('database.html', databases=databases)
    
    #view vehicles
    @app.route('/view_vehicle', methods=['GET'])
    def view_vehicle():
        id = request.args.get('id')
        vehicle = Vehicle.query.get(id)
        return render_template('view_vehicle.html', vehicle = vehicle)
    

    #edit vehicle
    @app.route('/edit', methods=['GET'])
    def edit_vehicle():
        #get vehicle
        id = request.args.get('id')
        vehicle = Vehicle.query.get(id)

        if request.method == 'GET':
            return render_template('edit.html', vehicle = vehicle)
    
        if request.method == 'POST':
            
            id = request.form["id"]
            vehicle = Vehicle.query.get(id)
            vehicle.image = request.form.get("Image")
            vehicle.name = request.form.get("Name")
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
            return redirect(url_for('index'))
        

    #delete vehicle
    @app.route('/delete', methods=['GET'])
    def delete_vehicle():
        id = request.args.get('id')
        vehicle = Vehicle.query.get(id)
        db.session.delete(vehicle)
        db.session.commit()

        return redirect(url_for('index'))

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