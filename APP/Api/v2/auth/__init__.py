from flask import Blueprint
from .views import SignUp, Login

auth_blueprint=Blueprint('auth',__name__)