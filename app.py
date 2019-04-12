import os
import sqlalchemy
import json

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, User, Product, Payment
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    print(password)
    user = User.query.filter_by(email=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)
  
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
##Setting the place for the db to run

jwt = JWT(app, authenticate, identity)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/final_project_2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)

CORS(app)


@app.route('/user', methods=['POST'])
def adduser():
    info = request.get_json() or {}
    item = User(first_name=info["first_name"],
                       last_name=info["last_name"],
                       email=info["email"],
                       password=info["password"],
                       business_name=info["business_name"],
                       business_username=info["business_username"],
                       business_password=info["business_password"],
                       website_url=info["website_url"],
                       phone=info["phone"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})
    
@app.route('/user/all')
def user_list():
    users = User.query.all()
    response = []
    for u in users:
        user = u.to_dict()
        response.append(user)
    
    return jsonify({"data": response})
    
    
@app.route('/product', methods=['POST'])
def addproduct():
    info = request.get_json() or {}
    item = Product(type=info["type"],
                       name=info["name"],
                       price=info["price"],
                       description=info["description"],
                       source_url=info["source_url"],
                       image=info["image"],
                       number_of_blogs=info["number_of_blogs"],
                       blog_word_total=info["blog_word_total"],
                       schedule=info["schedule"],
                       product_number=info["product_number"],
                       e_blast_software_name=info["e_blast_software_name"],
                       e_blast_software_url=info["e_blast_software_url"],
                       e_blast_software_user=info["e_blast_software_user"],
                       e_blast_user_password=info["e_blast_user_password"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})
    
    
@app.route('/product/all')
def product_list():
    products = Product.query.all()
    response = []
    for p in products:
        product = p.to_dict()
        response.append(product)
    
    return jsonify({"data": response})
    

@app.route('/product/<product_id>', methods=['DELETE'])
def get_product(product_id):
    
    notfound = {
        'status_code': 400,
        'message': 'product not found'
    }
    
    okresponse = {
        'status_code': 200,
        'message': 'ok'
    }
    
    if product_id != 0 and product_id is not None:
        currentProduct = Product.query.get(product_id)
        if currentProduct is not None:
            db.session.delete(currentProduct)
            db.session.commit()
            return jsonify(okresponse)
    else:
        return make_response(jsonify(notfound), 400)
    
    
@app.route('/user')
@jwt_required()

def get_user():
    
    notfound = {
        'status_code': 400,
        'message': 'user not found'
    }
    
    if current_identity.id != 0 and current_identity.id is not None:
        currentUser = User.query.get(current_identity.id)
        return jsonify(currentUser.to_dict())
    else:
        return jsonify(notfound)
        

@app.route('/create_payment', methods=['POST'])
@jwt_required()
def create_pay():
    
    notfound = {
        'status_code': 400,
        'message': 'user not found'
    }
    
    if current_identity.id != 0 and current_identity.id is not None:
        currentUser = User.query.get(current_identity.id)
        if currentUser is not None:
            info = request.get_json() or {}
            item = Payment(cc_number=info["cc_number"],
                           name=info["name"],
                           zip_code=info["zip_code"],
                           exp_date=info["exp_date"],
                           cvv_code=info["cvv_code"])
            db.session.add(item)
            currentUser.payment = item
            db.session.commit()
            return jsonify({"response": "ok"})
        else:
            return jsonify(notfound)
    else:
        return jsonify(notfound)
        
        
        
@app.route('/cart')
@jwt_required()
def view_cart():
    notfound = {
        'status_code': 400,
        'message': 'user not found'
    }
    
    if current_identity.id !=0 and current_identity.id is not None:
        currentUser = User.query.get(current_identity.id)
        if currentUser is not None:
            return jsonify(currentUser.get_cart())
        else:
            return jsonify(notfound)
    else:
        return jsonify(notfound)
            
  

@app.route('/cart/<product_id>', methods=['POST', 'DELETE'])
@jwt_required()
def update_cart(product_id):
    usernotfound = {
        'status_code': 400,
        'message': 'user not found'
    }
    
    productnotfound = {
        'status_code': 400,
        'message': 'product not found'
    }
    
    if request.method == "DELETE":
        if current_identity.id != 0 and current_identity.id is not None:
            currentUser = User.query.get(current_identity.id)
            if currentUser is not None:
                if product_id !=0 and product_id is not None:
                    currentProduct = Product.query.get(product_id)
                    if currentProduct is not None:
                        currentUser.products.remove(currentProduct)
                        db.session.commit()
                        return jsonify(currentUser.get_cart())
                    else:
                        return jsonify(productnotfound)
                else:
                    return jsonify(productnotfound)
            else:
                return jsonify(usernotfound)
        else:
            return jsonify(usernotfound)
    else:
        if current_identity.id !=0 and current_identity.id is not None:
            currentUser = User.query.get(current_identity.id)
            if currentUser is not None:
                currentProduct = Product.query.get(product_id)
                currentUser.products.append(currentProduct)
                db.session.commit()
                return jsonify(currentUser.get_cart())
            else:
                jsonify(usernotfound)
        else:
            jsonify(usernotfound)
        
        
        
@app.route('/history', methods=["POST"])
@jwt_required()
def push_to_histry():
    notfound = {
        'status_code': 400,
        'message': 'user not found'
    }
    if current_identity.id !=0 and current_identity.id is not None:
        current_user = User.query.get(current_identity.id)
        if current_user is not None:
            current_user.cart_to_json()
        else:
            jsonify(notfound)
    else:
        jsonify(notfound)
    

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))