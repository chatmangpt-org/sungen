from flask import request, jsonify
from services.user_service import UserService
from services.product_service import ProductService

user_service = UserService()
product_service = ProductService()

def register_routes(app):
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = user_service.get_user(user_id)
        return jsonify(user)

    @app.route('/users', methods=['POST'])
    def create_user():
        user_data = request.json
        user = user_service.create_user(user_data)
        return jsonify(user), 201

    @app.route('/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        product = product_service.get_product(product_id)
        return jsonify(product)

    @app.route('/products', methods=['POST'])
    def create_product():
        product_data = request.json
        product = product_service.create_product(product_data)
        return jsonify(product), 201
