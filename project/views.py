from flask import request, Blueprint,jsonify
from .import mydb,mycursor,hexid
import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
views= Blueprint('views', __name__)

# Create
@views.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    mycursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, hash_password))
    mydb.commit()
    #
    # mycursor.close()
    return jsonify({'status': 'success', 'message': 'User created'})

@views.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    # Get the user ID from the JWT token
    user_id = get_jwt_identity()
    product_id = hexid()
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    qty = request.json.get('qty')
    
    mycursor = mydb.cursor()
    mycursor.execute('''
        INSERT INTO products (product_id, description, price, qty, name, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (product_id, description, price, qty, name, user_id))
    mydb.commit()
    return jsonify({'message': 'Product added successfully'}), 200

@views.route('/products', methods=['GET'])
@jwt_required()
def user_product():
    current_user_id = get_jwt_identity()
    mycursor = mydb.cursor()
    query = """
        SELECT r.username, p.name, p.description, p.price, p.qty,p.price* p.qty AS Total_price, p.date
        FROM register r
        JOIN products p
        ON r.id = p.user_id
        WHERE r.id = %s ORDER BY p.name
    """
    mycursor.execute(query, (current_user_id,))
    user_products = mycursor.fetchall()
    all_products = []
    
    for product in user_products:
        d = {}
        d['user'] = product[0]
        d['name'] = product[1]
        d['description'] = product[2]
        d['price'] = product[3]
        d['qty'] = product[4]
        d['date'] = product[6]
        d['Total_price'] = product[5]
        all_products.append(d)
    return jsonify(all_products)
