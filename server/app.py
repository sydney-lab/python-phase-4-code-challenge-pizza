#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants])


@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    return jsonify(restaurant.to_dict())


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204


@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas])


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(restaurant_pizza.to_dict()), 201
    except (ValueError, Exception):
        return jsonify({'errors': ['validation errors']}), 400


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
