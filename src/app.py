"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Peoples, Planets, Favorite_Planet, Favorite_People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# AQUI EMPIEZAN LOS ENDPOINTS

#TRAEME TODOS LOS USUARIOS

@app.route('/user', methods=['GET'])
def get_all_user():
    all_user = User.query.all()
    results = list(map(lambda element:element.serialize(), all_user))

    return jsonify(results), 200

#TRAEME TODOS LOS CHARACTERS

@app.route('/peoples', methods=['GET'])
def get_people():
    all_people = Peoples.query.all()
    results = list(map(lambda element:element.serialize(), all_people))

    return jsonify(results), 200

#TREAME UN CHARACTER POR SU ID

@app.route('/peoples/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    people = Peoples.query.filter_by(id=people_id).first()
    
    return jsonify(people.serialize()), 200

#TRAEME TODOS LOS PLANETAS

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda element:element.serialize(), all_planets))

    return jsonify(results), 200

#TRAEME UN PLANETA POR SU ID

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    Planet = Planets.query.filter_by(id=planet_id).first()
    
    return jsonify(Planet.serialize()), 200

#TRAEME LOS PLANETAS FAVORITOS DE UN USUARIO

@app.route('/favorites/planets/<int:favorite_id>', methods=['GET'])
def get_favorite_planet(favorite_id):
    all_favorite_planet = Favorite_Planet.query.filter_by(id=favorite_id).all()
    results = list(map(lambda element:element.serialize(), all_favorite_planet))

    return jsonify(results), 200

#TRAEME LOS CHARACTERS FAVORITOS DE UN USUARIO

@app.route('/favorites/people/<int:favorite_id>', methods=['GET'])
def get_favorite_people(favorite_id):
    all_favorite_people = Favorite_People.query.filter_by(id=favorite_id).all()
    results = list(map(lambda element:element.serialize(), all_favorite_people))

    return jsonify(results), 200

#CREA UN NUEVO FAVORITO DE PLANETA

@app.route('/favorites/planet', methods=['POST'])
def add_favorite_planet():
    print(request.get_json())
    user_id = request.get_json()['user_id']
    planet_id = request.get_json()['planets_id']

    favorite_planet = Favorite_Planet(user_id = user_id, planets_id = planet_id)
    db.session.add(favorite_planet)
    db.session.commit()

    response_body = {
       'message': 'Planeta Favorito añadido correctamente'
    }

    return jsonify(response_body), 200

#CREA UN NUEVO FAVORITO DE PEOPLE

@app.route('/favorites/people', methods=['POST'])
def add_favorite_people():
    print(request.get_json())
    user_id = request.get_json()['user_id']
    people_id = request.get_json()['peoples_id']

    favorite_people = Favorite_People(user_id = user_id, people_id = people_id)
    db.session.add(favorite_people)
    db.session.commit()

    response_body = {
       'message': 'Character Favorito añadido correctamente'
    }

    return jsonify(response_body), 200

@app.route('/favorites/people/delete/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    delete = Favorite_People.query.filter_by(id=people_id).first()

    if delete:
        
        db.session.delete(delete)
        db.session.commit()

        response_body = {
           'message': 'Character Favorito eliminado correctamente'
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           'message': 'El favorito no existe'
        }
        return jsonify(response_body), 404

@app.route('/favorites/planet/delete/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    delete = Favorite_Planet.query.filter_by(id=planet_id).first()

    if delete:
        
        db.session.delete(delete)
        db.session.commit()

        response_body = {
           'message': 'Planeta Favorito eliminado correctamente'
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           'message': 'El favorito no existe'
        }
        return jsonify(response_body), 404


# Aquí termina mi codigo

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
