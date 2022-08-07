import os
from flask import Flask
from flask_restful import Api
from resources.user import UserLogin, UserRegister
from resources.security import ForgotPassword, ChangePassword
from db import db
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('APP_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(UserRegister,'/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(ForgotPassword, '/forpass')
api.add_resource(ChangePassword, '/changepass')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)