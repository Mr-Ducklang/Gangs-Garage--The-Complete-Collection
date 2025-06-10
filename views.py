from flask import render_template, request, redirect, url_for, flash
from models import db, Vehicle # database model imported here too 

def init_routes(app):

    @app.route('/', methods=['GET'])
    def index():
        if request.args.get('name') is not None:
            name = request.args.get('name')
            vehicles = Vehicle.query.filter(Vehicle.name.ilike(f'%{name}%')).all()
        else:
            vehicles = Vehicle.query.all()
        return render_template('index_html', vehicles=vehicles)