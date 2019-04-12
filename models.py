from flask_sqlalchemy import SQLAlchemy
import json
  
db = SQLAlchemy()
  

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    business_name = db.Column(db.String)
    business_username = db.Column(db.String)
    business_password = db.Column(db.String)
    website_url = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=True)
    payment = db.relationship("Payment", uselist=False)
    products = db.relationship("Product", secondary=cart, lazy="subquery", backref=db.backref("users", lazy=True))
    
    def __repr__(self):
        return 'User: %s' % (self.first_name)
        
    def to_dict(self):
        products = []
        for x in self.products:
            products.append(x.to_dict_simple())
            
        return { 
          "id": self.id, 
          "first_name": self.first_name, 
          "last_name": self.last_name,
          "email": self.email,
          "password": self.password,
          "business_name": self.business_name,
          "business_username": self.business_username,
          "business_password": self.business_password,
          "website_url": self.website_url,
          "phone": self.phone,
          "payment_id": self.payment_id,
          "payment": self.payment.to_dict() if self.payment is not None else None,
          "products": products
        }
        
    def get_cart(self):
        products = []
        for x in self.products:
            products.append(x.to_dict_simple())
        
        return products
        
    def cart_to_json(self):
        json.dumps(self.products)
        

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # APPLIES TO BOTH
    type = db.Column(db.String, nullable=False) # APPLIES TO BOTH
    name = db.Column(db.String, nullable=False) # APPLIES TO BOTH
    price = db.Column(db.Integer) # APPLIES TO BOTH
    description = db.Column(db.String) # APPLIES TO BOTH
    source_url = db.Column(db.String) # APPLIES TO BOTH
    image = db.Column(db.String) # APPLIES TO BOTH
    number_of_blogs = db.Column(db.Integer) # APPLIES TO PACKAGE ONLY
    blog_word_total = db.Column(db.Integer) # APPLIES TO PACKAGE ONLY
    schedule = db.Column(db.String) # APPLIES TO PACKAGE ONLY
    product_number = db.Column(db.String) # APPLIES TO ADDONS ONLY
    e_blast_software_name = db.Column(db.String) # APPLIES TO ADDONS ONLY
    e_blast_software_url = db.Column(db.String) # APPLIES TO ADDONS ONLY
    e_blast_software_user = db.Column(db.String) # APPLIES TO ADDONS ONLY
    e_blast_user_password = db.Column(db.String) # APPLIES TO ADDONS ONLY
    
    def __repr__(self):
        return 'Product: %s' % (self.name)
        
    def to_dict(self):
        return { 
          "id": self.id, 
          "type": self.type, 
          "name": self.name,
          "price": self.price,
          "description": self.description,
          "source_url": self.source_url,
          "image": self.image,
          "number_of_blogs": self.number_of_blogs,
          "blog_word_total": self.blog_word_total,
          "schedule": self.schedule,
          "product_number": self.product_number,
          "e_blast_software_name": self.e_blast_software_name,
          "e_blast_software_url": self.e_blast_software_url,
          "e_blast_software_user": self.e_blast_software_user,
          "e_blast_user_password": self.e_blast_user_password
        }
        
    def to_dict_simple(self):
        return { 
            "name": self.name, 
            "type": self.type, 
            "price": self.price
        }
        
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cc_number = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.String, nullable=False)
    cvv_code = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return 'Payment: %s' % (self.name)
        
    def to_dict(self):
        return { 
          "id": self.id, 
          "cc_number": self.cc_number, 
          "name": self.name,
          "zip_code": self.zip_code,
          "exp_date": self.exp_date,
          "cvv_code": self.cvv_code
        }
     
     
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    cart_info = db.Column(db.String, nullable=False)
    date_created = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return 'History: %s' % (self.name)