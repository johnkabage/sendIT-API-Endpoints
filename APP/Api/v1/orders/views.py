from flask import request
from flask_restful import Resource
from ..models import ParcelOrder, parcels_store
from validators.validators import Validators

class Parcel(Resource):

    def post(self):
        '''
        creating a pacel
        '''
        request_data = request.get_json()
        _from = request_data['_from']
        destination = request_data['destination']
        weight = request_data['weight']
        parcel = request_data['parcel']
        recipient = request_data['recipient']
        price = (weight * 10)
        sender = request_data['sender']

        if not Validators().valid_inputs(_from):
            return {
                'message':"enter valid text"
            }, 401

        if not Validators().valid_inputs(destination):
            return {
                'message':"enter valid text"
            }, 401

        if not Validators().valid_inputs(parcel):
            return {
                'message':"enter valid text"
            }, 401

        if not Validators().valid_inputs(recipient):
            return {
                'message':"enter valid text"
            }, 401

        if type(weight) != int:
            return {
                'message':'Enter a valid weight'
            }, 401

        parcel = ParcelOrder(sender, _from, destination, weight, parcel, recipient, price)
        parcels_store.append(parcel)

        return {
            "parcel":parcel.__dict__,
            "message":"parcel order created"
        }, 201

    def get(self):
        '''
        get parcel orders
        '''
        all_parcels = [parcel.__dict__ for parcel in parcels_store]

        return {"parcels": all_parcels}, 200

class GetParcel(Resource):

    def get(self, parcelId):
        '''
        get a single parcel
        '''
        parcel = ParcelOrder().get_parcel_by_id(parcelId)

        if not parcel:
            return {'message': 'parcel not found'}, 404
        return {"parcel":parcel.__dict__}, 200

    def delete(self, parcelId):
        '''
        delete a specific parcel
        '''
        parcel = ParcelOrder().get_parcel_by_id(parcelId)

        if not parcel:
            return {'message': 'parcel not found'}, 404
        parcels_store.remove(parcel)

        return {
            "message": "parcel deleted successfully"
        }, 200


class CancelParcelOrder(Resource):

    def put(self, parcelId):
        '''
        Cancel a parcel order
        '''
        parcel = ParcelOrder().get_parcel_by_id(parcelId)

        if not parcel:
            return {'message': 'parcel not found'}, 404
        parcel.status = 'cancelled'
        return {
            "message":"parcel cancelled successfully",
            "cancelled parcel":parcel.__dict__
            }, 200



