from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from ..models import User, users_store
from validators.validators import Validators

class SignUp(Resource):
    def post(self):
        '''
        user can signup
        '''
        request_data = request.get_json()
        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        confirm_password = request_data['confirm_password']

        if not Validators().valid_username(username):
            return {
                'message':'enter a valid username'
            }, 401

        if not Validators().valid_email(email):
            return {
                "message":"Enter a valid email"
            }, 401

        if not Validators().valid_password(password):
            return {
                'message':'Enter a valid password'
            }, 401

        if password != confirm_password:
            return {
                'message':'password does not match'
            }, 401

        user = User(username, email, password, confirm_password)

        users_store.append(user)

        return {
            'message':f'Account for {username} created successfully'
        }, 201

class Login(Resource):
    def post(self):
        '''
        user can login
        '''
        request_data = request.get_json()

        username = request_data['username']
        password = request_data['password']

        if not Validators().valid_username(username):
            return {
                'message':'enter a valid username'
            }, 401

        if not Validators().valid_password(password):
            return {
                'message':'Enter a valid password'
            }, 401

        user = User().get_user_by_username(username)

        if not user:
            return {
                'message':'user does not exist'
            }, 404
        if not check_password_hash(user.password, password):
            return {
                'message':'Invalid password, enter the correct password'
            }, 401

        token = create_access_token(identity=user.__dict__)

        return {
            'token':token,
            'message':f'successfully logged in as {user.username}'
        }