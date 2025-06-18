from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy  # This import was missing
from flask_migrate import Migrate
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models here (or import them if in separate file)
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'hero_powers': [{
            'id': hp.id,
            'hero_id': hp.hero_id,
            'power_id': hp.power_id,
            'strength': hp.strength,
            'power': {
                'id': hp.power.id,
                'name': hp.power.name,
                'description': hp.power.description
            }
        } for hp in hero.hero_powers]
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
        return jsonify({
            'id': hero_power.id,
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength,
            'hero': {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            },
            'power': {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
        }), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400
    
    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
        return jsonify({
            'id': hero_power.id,
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength,
            'hero': {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            },
            'power': {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
        }), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500



if __name__ == '__main__':
    app.run(port=5555)