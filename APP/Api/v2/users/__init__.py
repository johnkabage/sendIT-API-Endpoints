from flask import Blueprint
from .views import SpecificUserParcels, GetAllUsers

user_blueprint=Blueprint('user',__name__)