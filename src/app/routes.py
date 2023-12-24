from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.models import db, User, Product, Order, OrderProduct

api = Blueprint('api', __name__)
api_restful = Api(api)

# RESTful Endpoints

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403

        user = User.query.get(int(user_id))
        if user:
            return jsonify({'id': user.id, 'is_admin': user.is_admin})
        else:
            return jsonify({'error': 'User not found'}), 404

class ProductResource(Resource):
    @jwt_required()
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock_quantity': product.stock_quantity
        })

class CartResource(Resource):
    @jwt_required()
    def get(self):
        cart_items = [product.to_dict() for product in Product.query.filter(Product.id.in_(session.get('cart', [])))]
        total_price = sum(item['price'] for item in cart_items)
        return jsonify({'cart_items': cart_items, 'total_price': total_price})

api_restful.add_resource(UserResource, '/api/user/<int:user_id>')
api_restful.add_resource(ProductResource, '/api/product/<int:product_id>')
api_restful.add_resource(CartResource, '/api/cart')

# Shopping Cart and Checkout functionality

# View all products and add to cart
@api.route('/shop', methods=['GET'])
@jwt_required()
def view_shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

# Add item to cart
@api.route('/add_to_cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    return redirect(url_for('.view_shop'))

# View shopping cart
@api.route('/cart', methods=['GET'])
@jwt_required()
def view_cart():
    cart_items = [Product.query.get(id) for id in session.get('cart', [])]
    total_price = sum(item.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# Remove item from cart
@api.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@jwt_required()
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [id for id in session['cart'] if id != product_id]
    return redirect(url_for('.view_cart'))

# Checkout process
@api.route('/checkout', methods=['GET', 'POST'])
@jwt_required()
def checkout():
    if request.method == 'POST':
        # Perform checkout process (e.g., save order details, clear cart, etc.)
        user = User.query.get(current_user.id)  # Get the user from the current_user
        order = Order(user=user, products=[Product.query.get(product_id) for product_id in session.get('cart', [])])
        db.session.add(order)
        db.session.commit()
        session.pop('cart', None)  # Clear the shopping cart
        return render_template('checkout_success.html')

    cart_items = [Product.query.get(id) for id in session.get('cart', [])]
    total_price = sum(item.price for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

# ... (other routes remain unchanged)
