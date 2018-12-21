from werkzeug.security import generate_password_hash
from datetime import datetime
users_store = []
parcels_store = []

class ParcelOrder:
    parcel_id = 1
    def __init__(self,sender=None, _from = None,destination = None,weight = None, parcel = None, recipient = None, price=None):
        self.sender = sender
        self._from = _from
        self.destination = destination
        self.weight = weight
        self.parcel = parcel
        self.recipient = recipient
        self.price = price
        self.date = str(datetime.now())
        self.id = ParcelOrder.parcel_id

        ParcelOrder.parcel_id += 1

    def get_parcel_by_id(self, id):
        for parcel in parcels_store:
            if parcel.id == id:
                return parcel

    def get_parcels_by_sender(self, sender):
        pacels_sender = [parcel for parcel in parcels_store if parcel.sender == sender]
        return pacels_sender

class User:
    user_id = 1
    def __init__(self, username = None, email =None, password = None, confirm_password=None):
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        if confirm_password:
            self.confirm_password = generate_password_hash(confirm_password)
        self.id = User.user_id

        User.user_id += 1

    def get_user_by_username(self, username):
        for user in users_store:
            if user.username == username:
                return user

    def get_user_by_id(self, id):
        for user in users_store:
            if user.id == id:
                return user

    def serialize(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email
        )