from flask import Flask
from flask_restful import Api
from ..instance.config import app_config
from .v1.auth.views import Login, SignUp
from .v1.orders.views import Parcel, GetParcel, CancelParcelOrder
from .v1.users.views import GetAllUsers, SpecificUserParcels


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    from .v1.auth import auth_blueprint as auth_bp
    auth = Api(auth_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    from .v1.orders import parcel_blueprint as parcel_bp
    parcel = Api(parcel_bp)
    app.register_blueprint(parcel_bp, url_prefix="/api/v1/parcels")

    from .v1.users import user_blueprint as user_bp
    user = Api(user_bp)
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")

    auth.add_resource(SignUp, '/signup')
    auth.add_resource(Login, '/login')
    parcel.add_resource(Parcel, '')
    parcel.add_resource(GetParcel, '/<int:parcelId>')
    parcel.add_resource(CancelParcelOrder, '/<int:parcelId>/cancel')
    user.add_resource(GetAllUsers, '')
    user.add_resource(SpecificUserParcels, '/<int:userId>/parcels')

    return app