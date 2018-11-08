from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models import User, ParcelOrder, users_store

class GetAllUsers(Resource):
    def get(self):
        '''
        Get all users
        '''

        users = [user.serialize() for user in  users_store ]
        if not users:
            return {
                'message':'there are no users'
            }, 404

        return {
            'all Users':users
        }, 200


class SpecificUserParcels(Resource):

    @jwt_required
    def get(self, userId):
        '''
        Get all parcels from a specific user
        '''
        user = User().get_user_by_id(userId)

        if not user:
            return {
                'message':'User not found'
            }, 404

        all_parcels = [parcel.__dict__ for parcel in ParcelOrder().get_parcels_by_sender(user.username)]

        return {
            f"parcels for {user.username}":all_parcels
        }, 200

