from flask import request,Blueprint,jsonify
from .import mycursor,mydb
from flask_jwt_extended import create_access_token,jwt_required
import bcrypt

auths=Blueprint('auths',__name__)

@auths.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    mycursor = mydb.cursor() 
    mycursor.execute("SELECT * FROM register WHERE username = %s",(username,))
    user = mycursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        access_token = create_access_token(identity=user[0])
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
    

