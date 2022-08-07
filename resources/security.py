import os
from flask_restful import Resource, reqparse
import random
import smtplib
from db import db
from models.user import UserModel, VerificationModel


class ForgotPassword(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str,
                        required=True)
    
    def post(self):
        verification_number = random.randrange(10000, 100000)
        
        data = ForgotPassword.parser.parse_args()
        user = UserModel.query.filter_by(email=data['email']).first()
        dt = VerificationModel(user.username, verification_number)
        db.session.add(dt)
        db.session.commit()

        sender_address = os.getenv['ADDRESS']
        sender_password = os.getenv['PASSWORD']
        
        subject = "Forgot Password : Verification Code"
        body = f"""
        verification code : {verification_number}
        """

        try:
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(user=sender_address,password=sender_password) #login with mail_id and password
            session.sendmail(
                from_addr=sender_address, 
                to_addrs=data['email'], 
                msg = f"Subject:{subject}\n\nVerification code : {verification_number}")
            session.quit()
            
            return {"message" : "Email sent successfully!"}
        except Exception as ex:
            return {"message" : f"Something went wrong….,{ex}"}
        

class ChangePassword(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('verification_code',
                        type=int,
                        required=True)
    
    parser.add_argument('new_password',
                        type=str,
                        required=True)
    
    def post(self):
        data = ChangePassword.parser.parse_args()
        
        user = VerificationModel.query.filter_by(verification_code=data['verification_code']).first()
        
        if user:
            new_user = UserModel.query.filter_by(username=user.username).first()
            new_user.password = data['new_password']
            db.session.commit()
            return {"message" : "Password changed successfully!"}
        
        return {"user" : user.username}