from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(80))
    email = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)
    
    def __init__(self,username, email, password, phone_number):
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        
    
    def find_by_email(email):
       return UserModel.query.filter_by(email=email).first()
   
    def find_by_username(username):
        return UserModel.query.filter_by(username=username).first()


class VerificationModel(db.Model):
    __tablename__ = 'verification'
    
    username = db.relationship('UserModel', backref='verificationmodel', lazy=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    verification_code = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, username, verification_code):
        self.username = username
        self.verification_code = verification_code