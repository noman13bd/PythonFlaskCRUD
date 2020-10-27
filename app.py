from flask import Flask
from flask import request
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#postgresql://USER:PASS@HOST:PORT/DB = "postgresql://postgres:postgres@docker_service_name_or_localhost:5405/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class PersonsModel(db.Model):
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return "Person ({}, {})".format(self.name, self.age)

@app.route("/")
def index():
    return {
        'hello':'world'
    }
    
@app.route("/persons", methods=['POST', 'GET'])
def persons_op():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_person = PersonsModel(data['name'], data['age'])
            db.session.add(new_person)
            db.session.commit()
            return {
                "message": "Person({}, {}) created.".format(new_person.name, new_person.age)
            }
        else:
            return {
                "message": "not a json request"
            }
    elif request.method == 'GET':
        persons = PersonsModel.query.all()
        
        results = [
            {
                "name": person.name,
                "age": person.age
            } for person in persons]

        return {"count": len(results), "persons": results}

if __name__ == "__main__":    
    manager.run()