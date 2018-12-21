from flask import Blueprint
from .views import Parcel, GetParcel, CancelParcelOrder

parcel_blueprint=Blueprint('parcel',__name__)