from flask_jwt_extended import create_access_token
from db import db
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask import session

class UserRegister(Resource):        
	def num_range(range):
		def validate(value):
			s = str(value)
			length = len(s)
			if length == range:
				return s
			raise ValueError(f"phone number must be in {range} digits, not {length}")

		return validate

	def type_check():
		def validate(value):
			if isinstance(value, int):
				raise ValueError("Username must be string!")

		return validate

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=type_check(),
		required=True)
	parser.add_argument('password',
		type=str,
		required=True)
	parser.add_argument('email',
		type=str,
		required=True)
	parser.add_argument('phone_number',
		type=num_range(10),
		required=True)
	
	
	def post(self):
		data = UserRegister.parser.parse_args()
		
		if UserModel.find_by_email(data['email']):
			return {"message" : "User already exists"}, 404
		
		user = UserModel(**data)
		db.session.add(user)
		db.session.commit()
		return {"message" : "User successfully created"}
	
	
class UserLogin(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True)
	parser.add_argument('password',
		type=str,
		required=True)
	
	def get(self):
		session['attempt'] = 3
	
	def post(self):
		data = UserLogin.parser.parse_args()
		
		user = UserModel.find_by_username(data['username'])
		print(user)
    
		
	
		if user and user.password == data['password']:
			session['logged_in'] = True    
			access_token = create_access_token(data['username'])
			session['username'] = user.username
			return {"access token" : access_token}, 200

		attempt = session.get('attempt')
		print(attempt)
		attempt -= 1
		session['attempt'] = attempt
		
		if attempt == 0:
			session['attempt'] = 3
			return {"message" :'Cant login, will be blocked for 24hr'}
		
		return {"message" : "Invalid Credentials"}, 401
	

