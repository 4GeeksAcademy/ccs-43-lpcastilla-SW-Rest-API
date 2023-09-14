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
from models import db, User, People, Planets, Favorites
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


#Rutas de User

@app.route('/user', methods=['POST'])    
def create_user():
    body = request.json
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")
    last_name = body.get("last_name")
    if email is None or password is None or name is None or last_name is None:
        return jsonify({
            "message": "Email, password, name and last name are required"
        }), 400
    
    user_exist = User.query.filter_by(email=email).one_or_none()
    if user_exist is not None:
        return jsonify({
            "message": "user already exists"
        }), 400
    
    user = User()
    user.email = email 
    user.password = password
    user.name = name
    user.last_name = last_name

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "internal error"
        }), 500
       
    return jsonify({}), 201 
 

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    if id is None:
        return jsonify({
            "message": "id is required"
        }), 400
    user = User.query.get(id)
    if user is None:
        return jsonify(""), 400
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users_list = User.query.all() 
    serialized_users = [user.serialize() for user in users_list]
    return jsonify(serialized_users), 200


# Rutas de people

@app.route('/people', methods=['POST'])    
def create_people():
    body = request.json
    name = body.get("name")
    description = body.get("description")
    if name is None or description is None:
        return jsonify({
            "message": "name and description are required"
        }), 400 
    
    people_exist = People.query.filter_by(name=name).one_or_none()
    if people_exist is not None:
        return jsonify({
            "message": "character already exists"
        }), 400
    
    people = People() 
    people.name = name
    people.description = description

    try:
        db.session.add(people)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "internal error"
        }), 500
       
    return jsonify({}), 201 
 

@app.route('/people/<int:id>', methods=['GET'])
def get_people(id):
    if id is None:
        return jsonify({
            "message": "id is required"
        }), 400
    people = People.query.get(id)
    if people is None:
        return jsonify(""), 400
    return jsonify(people.serialize()), 200 

@app.route('/people', methods=['GET'])  
def get_all_people():
    people_list = People.query.all() 
    serialized_people = [person.serialize() for person in people_list]
    return jsonify(serialized_people), 200


# Rutas de planets

@app.route('/planets', methods=['POST'])    
def create_planet():
    body = request.json
    name = body.get("name")
    description = body.get("description")
    if name is None or description is None:
        return jsonify({
            "message": "name and description are required"
        }), 400
    
    planet_exist = Planets.query.filter_by(name=name).one_or_none()
    if planet_exist is not None:
        return jsonify({
            "message": "planet already exists"
        }), 400
    
    planets = Planets() 
    planets.name = name
    planets.description = description

    try:
        db.session.add(planets)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "internal error"
        }), 500
      
    return jsonify({}), 201 
 

@app.route('/planets/<int:id>', methods=['GET'])
def get_planets(id):
    if id is None:
        return jsonify({
            "message": "id is required"
        }), 400
    planets = Planets.query.get(id)
    if planets is None:
        return jsonify(""), 400
    return jsonify(planets.serialize()), 200 

@app.route('/planets', methods=['GET'])  
def get_all_planets():
    planet_list = Planets.query.all() 
    serialized_planets = [planet.serialize() for planet in planet_list]
    return jsonify(serialized_planets), 200



# Rutas de favorites

@app.route('/favorites/planets/<int:user_id>', methods=['POST'])  
def create_favorite_planet(user_id):
    body = request.json
    user = body.get("user")
    planet = Planets.query.get(user_id)

    if planet is None:
        return jsonify({
            "message": "Planet not found"
        }), 404

    favorite = Favorites.query.filter_by(id_planets=planet.id).one_or_none()
    if favorite is not None:
        return jsonify({
            "message": "Planet is already a favorite"
        }), 400

    new_favorite = Favorites(id_planets=planet.id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "Internal error"
        }), 500

    return jsonify({
        "message": "Planet added to favorites"
    }), 201


@app.route('/favorites/people/<int:people_id>', methods=['POST'])  
def create_favorite_people(people_id):
    people = People.query.get(people_id)

    if people is None:
        return jsonify({
            "message": "People not found"
        }), 404

    favorite = Favorites.query.filter_by(id_people=people.id).one_or_none()
    if favorite is not None:
        return jsonify({
            "message": "People is already a favorite"
        }), 400

    new_favorite = Favorites(id_people=people.id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "Internal error"
        }), 500

    return jsonify({
        "message": "People added to favorites"
    }), 201


# Rutas de Delete

@app.route('/favorites/people/id', methods=['DELETE'])  
def delete_favorite_people(people_id):
    people = People.query.get(people_id)

    if people is None:
        return jsonify({
            "message": "People not found"
        }), 404

    favorite = Favorites.query.filter_by(id_people=people.id).one_or_none()
    if favorite is None:
        return jsonify({
            "message": "People is not in favorites"
        }), 400

    try:
        db.session.delete(favorite)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "Internal error"
        }), 500

    return jsonify({
        "message": "People removed from favorites"
    }), 200


@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])  
def delete_favorite_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({
            "message": "Planet not found"
        }), 404

    favorite = Favorites.query.filter_by(id_planets=planet.id).one_or_none()
    if favorite is None:
        return jsonify({
            "message": "Planet is not in favorites"
        }), 400

    try:
        db.session.delete(favorite)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "Internal error"
        }), 500

    return jsonify({
        "message": "Planet removed from favorites"
    }), 200

    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
   