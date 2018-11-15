from flask import request
from flask_restful import Resource, reqparse
from ..models import ParcelOrder, parcels_store
from validators.validators import Validators

class Parcel(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('sender', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('_from', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('destination', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('weight', type=int, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('parcel', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('recipient', type=str, required=True,
                        help='This field cannot be left blank')


    def post(self):
        '''
        creating a parcel
        '''
        request_data = Parcel.parser.parse_args()

        sender = request_data['sender']
        _from = request_data['_from']
        destination = request_data['destination']
        weight = request_data['weight']
        parcel = request_data['parcel']
        recipient = request_data['recipient']
        price = (weight * 10)

        if not sender:
            return {"message":"This field is reuired"},400

        if not Validators().valid_inputs(_from):
            return {
                'message':"Enter a valid location"
            }, 401

        if not Validators().valid_inputs(destination):
            return {
                'message':"Enter a valid location"
            }, 401

        if not Validators().valid_inputs(parcel):
            return {
                'message':"Enter a valid parcel item"
            }, 401

        if not Validators().valid_inputs(recipient):
            return {
                'message':"Enter a valid recipient name"
            }, 401

        if type(weight) != int:
            return {
                'message':'Enter a valid number'
            }, 401

        if not Validators().valid_inputs(sender):
            return {
                'message':"Enter a valid sender name"
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



