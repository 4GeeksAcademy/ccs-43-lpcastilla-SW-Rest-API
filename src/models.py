from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(200), unique=False, nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorites', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self): 
        favorites = [fav.serialize() for fav in self.favorites]
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "favorites": favorites
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    favorites = db.relationship('Favorites', back_populates='people')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    favorites = db.relationship('Favorites', back_populates='planets')

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
        
class Favorites(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        id_people = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
        people = db.relationship("People", back_populates='favorites')
        id_planets = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
        planets = db.relationship("Planets", back_populates='favorites')
        id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship("User", back_populates='favorites')

        def __repr__(self):
            return '<Favorites %r>' % self.id_user

        def serialize(self):
            return {
                "id": self.id,
                "id_people": self.id_people,
                "id_planets": self.id_planets,
                "id_user": self.id_user,
            }