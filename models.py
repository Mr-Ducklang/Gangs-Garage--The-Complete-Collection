from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=True)
    quote = db.Column(db.String(100), nullable = True)
    description = db.Column(db.Text)
    odometer =  db.Column(db.String(100), nullable = True)
    owner = db.Column(db.String(100), nullable = True)
    type = db.Column(db.String(100), nullable=True)
    make = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable = True)
    features = db.Column(db.Text)
    currentissues = db.Column(db.Text)
    previousissues = db.Column(db.Text)
    databaseid = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Task {self.Title}>'

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    databaseid = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Task {self.Title}>'   
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_pic = db.Column(db.String, nullable=True)
    username = db.Column(db.String(100), nullable=False)
    password