from flask import Flask
from flask_jwt_extended import JWTManager
import mysql.connector
import uuid
app= Flask(__name__)

def hexid():
    return uuid.uuid4().hex

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)
# Create cursor object
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS  users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    )""")


mycursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(120) NOT NULL,
        name VARCHAR(50) NOT NULL,
        description VARCHAR(120),
        price INT(200) NOT NULL,
        qty INT(3) NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INT(11) NOT NULL,
        PRIMARY KEY(product_id),
        UNIQUE(product_id),
        CONSTRAINT fk_user
            FOREIGN KEY (user_id)
            REFERENCES register(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )
''')


def create_app():
    #app= Flask(__name__)
    #db = SQLAlchemy()
    app.config['SECRET_KEY']= '3d74c695414795926033bc5c09we00'
   
    
    
    
    #db.init_app(app)
    jwt = JWTManager(app)
    #from .import models

    #with app.app_context():
        #db.create_all()

   

    #register view
    
    from .views import views
    from .auths import auths

    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(deletes, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')
    
    return app