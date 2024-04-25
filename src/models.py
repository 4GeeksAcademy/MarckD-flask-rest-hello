from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship('Favorite_Planet', backref='user', lazy=True)
    favorite_planet = db.relationship('Favorite_People', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    poblation = db.Column(db.Integer)
    galaxy = db.Column(db.String(120))
    favorite_planet = db.relationship('Favorite_Planet', backref='Planet', lazy=True)

    def __repr__(self):
        return '<planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "poblation": self.poblation,
            "galaxy": self.galaxy
        }
    

class Peoples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(80))
    birth_day = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    favorite_people = db.relationship('Favorite_People', backref='People', lazy=True)

    def __repr__(self):
        return '<people %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "birth_day": self.birth_day,
        }
    

class Favorite_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('peoples.id'), nullable=False)

    def __repr__(self):
        return '<Favorite_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.User_id,
            "people_id": self.people_id,
        }



class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    def __repr__(self):
        return '<Favorite_Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
        }
    
    
    




    
    
