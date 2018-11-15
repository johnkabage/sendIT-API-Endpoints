from unittest import TestCase
import json
from APP.Api import create_app

class TestParcels(TestCase):
    def setUp(self):
        """ Setting up for testing """
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        '''tear down after testing'''
        self.app_context.pop()

    def signup(self):
        '''Sign up function'''
        sigup_cred = {
            "username":"john",
            "email":"john@gmail.com",
            "password":"Password123",
            "confirm_password":"Password123"
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(sigup_cred),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        ''' Login function '''
        login_cred = {
            "username":"john",
            "password":"Password123"
        }
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(login_cred),
            headers={'content-type': 'application/json'}
        )

        return response

    def test_signup(self):
        '''
        Test user signup
        '''
        res = self.signup()
        self.assertEquals(res.status_code, 201)
        self.assertEquals(json.loads(res.data)['message'], 'Account for john created successfully')

    def test_login(self):
        '''
        Test a user can successfully login after creating an account
        '''
        self.signup()
        response = self.login()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data)['message'],"successfully logged in as john")

    def test_invalid_username(self):
        '''
        test for invalid username
        '''
        sigup_cred = {
            "username":"*****",
            "email":"john@gmail.com",
            "password":"Password123",
            "confirm_password":"Password123"
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(sigup_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "enter a valid username")

    def test_invalid_email(self):
        '''
        test for invalid email
        '''
        sigup_cred = {
            "username":"john",
            "email":"$$%%$",
            "password":"Password123",
            "confirm_password":"Password123"
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(sigup_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid email")

    def test_invalid_password(self):
        '''
        test for invalid password
        '''
        sigup_cred = {
            "username":"john",
            "email":"john@gmail.com",
            "password":"Password",
            "confirm_password":"Password123"
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(sigup_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid password")

    def test_invalid_confirm_password(self):
        '''
        test for confirm password
        '''
        sigup_cred = {
            "username":"john",
            "email":"john@gmail.com",
            "password":"Password123",
            "confirm_password":"Password12"
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(sigup_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "password does not match")

    def test_user_does_not_exist(self):
        '''
        test user does not exist
        '''
        login_cred = {
            "username":"kikkim",
            "password":"Password123"
        }
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(login_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.data)['message'], "user does not exist")

    def test_wrong_password(self):
        '''
        test user does not exist
        '''
        login_cred = {
            "username":"john",
            "password":"Password12"
        }
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(login_cred),
            headers={'content-type': 'application/json'}
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'],
        "Invalid password, enter the correct password")

    def create_parcel(self):
        '''
        function to create a parcel
        '''
        parcel_cred = {
            "sender":"john",
            "_from":'thka',
            "destination":"ruiru",
            "weight":10,
            "parcel":"phone",
            "recipient":"reciever"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )

        return response

    def test_create_parcel(self):
        '''
        test create a parcel
        '''
        response = self.create_parcel()
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.data)['message'], "parcel order created")

    def test_Invalid_from(self):
        '''
        test invalid from location
        '''
        parcel_cred = {
            "sender":"john",
            "_from":'$%$$%%',
            "destination":"ruiru",
            "weight":10,
            "parcel":"phone",
            "recipient":"reciever"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid location")

    def test_Invalid_destination(self):
        '''
        test invalid destination location
        '''
        parcel_cred = {
            "sender":"john",
            "_from":'thika',
            "destination":"#$$%^$",
            "weight":10,
            "parcel":"phone",
            "recipient":"reciever"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid location")

    def test_Invalid_parcel(self):
        '''
        test invalid parcel item
        '''
        parcel_cred = {
            "sender":"john",
            "_from":'thika',
            "destination":"juja",
            "weight":10,
            "parcel":"",
            "recipient":"reciever"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid parcel item")

    def test_Invalid_recipient(self):
        '''
        test invalid recipient name
        '''
        parcel_cred = {
            "sender":"john",
            "_from":'thika',
            "destination":"juja",
            "weight":10,
            "parcel":"laptop",
            "recipient":"@#$"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid recipient name")



    def test_Invalid_sender(self):
        '''
        test invalid sender name
        '''
        parcel_cred = {
            "sender":"*&^%%$",
            "_from":'thika',
            "destination":"juja",
            "weight":10,
            "parcel":"laptop",
            "recipient":"receiver"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid sender name")


    def test_get_all_parcels(self):
        '''
        test get all parcels
        '''

        self.create_parcel()
        response = self.client.get(
            "/api/v1/parcels"
        )

        self.assertEquals(response.status_code, 200)

    def test_get_specific_parcel(self):
        '''
        test get specific parcel
        '''
        self.create_parcel()

        response = self.client.get(
            "/api/v1/parcels/1"
        )

        self.assertEquals(response.status_code, 200)

    def test_get_non_existing_parcel(self):
        '''
        test get non existing parcel
        '''
        self.create_parcel()

        response = self.client.get(
            "/api/v1/parcels/100000"
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.data)['message'], 'parcel not found')

    def test_cancel_parcel(self):
        '''
        test cancel order
        '''
        self.create_parcel()

        response = self.client.put(
            "/api/v1/parcels/1/cancel"
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data)['message'], 'parcel cancelled successfully')

    def test_get_all_users(self):
        '''
        test get all users
        '''
        self.signup()
        response = self.client.get(
            "/api/v1/users"
        )
        self.assertEquals(response.status_code, 200)

    def test_specific_user_parcels(self):
        '''
        test get specific user parcels
        '''
        response = self.client.get(
            "/api/v1/users/1/parcels"
        )
        self.assertEquals(response.status_code, 200)

    def test_user_not_found(self):
        '''
        test a non existing user
        '''
        response = self.client.get(
            "/api/v1/users/1000/parcels"
        )
        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.data)['message'], 'User not found')

