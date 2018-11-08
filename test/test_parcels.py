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

    def get_user_token(self):
        '''
        Get token function
        '''

        self.signup()
        response = self.login()
        token = json.loads(response.data).get('token', None)

        return token


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


    def test_user_get_token(self):
        '''
        Test a user gets a token after login
        '''
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

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

    def test_invalid_confir_password(self):
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
        self.assertEquals(json.loads(response.data)['message'], "Invalid password, enter the correct password")

    def create_parcel(self):
        '''
        function to create a parcel
        '''
        token = self.get_user_token()
        parcel_cred = {
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
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
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
        test invalid from
        '''
        token = self.get_user_token()
        parcel_cred = {
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
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "enter valid text")

    def test_Invalid_destination(self):
        '''
        test invalid destination
        '''
        token = self.get_user_token()
        parcel_cred = {
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
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "enter valid text")

    def test_Invalid_parcel(self):
        '''
        test invalid parcel name
        '''
        token = self.get_user_token()
        parcel_cred = {
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
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "enter valid text")

    def test_Invalid_recipient(self):
        '''
        test invalid recipient
        '''
        token = self.get_user_token()
        parcel_cred = {
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
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "enter valid text")


    def test_Invalid_weight(self):
        '''
        test invalid weight
        '''
        token = self.get_user_token()
        parcel_cred = {
            "_from":'thika',
            "destination":"juja",
            "weight":'hasdfg',
            "parcel":"laptop",
            "recipient":"receiver"
        }
        response = self.client.post(
            "/api/v1/parcels",
            data=json.dumps(parcel_cred),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
             }
        )

        self.assertEquals(response.status_code, 401)
        self.assertEquals(json.loads(response.data)['message'], "Enter a valid weight")

    def test_get_all_parcels(self):
        '''
        test get all parcels
        '''
        token = self.get_user_token()
        self.create_parcel()

        response = self.client.get(
            "/api/v1/parcels",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )

        self.assertEquals(response.status_code, 200)

    def test_get_specific_parcel(self):
        '''
        test get specific parcel
        '''
        token = self.get_user_token()
        self.create_parcel()

        response = self.client.get(
            "/api/v1/parcels/1",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )

        self.assertEquals(response.status_code, 200)

    def test_get_non_existing_parcel(self):
        '''
        test get non existing parcel
        '''
        token = self.get_user_token()
        self.create_parcel()

        response = self.client.get(
            "/api/v1/parcels/100000",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.data)['message'], 'parcel not found')

    def test_cancel_parcel(self):
        '''
        test cancel order
        '''
        token = self.get_user_token()
        self.create_parcel()

        response = self.client.put(
            "/api/v1/parcels/1/cancel",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data)['message'], 'parcel cancelled successfully')

    def test_get_all_users(self):
        '''
        test get all users
        '''
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/users",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 200)

    def test_specific_user_parcels(self):
        '''
        test get specific user parcels
        '''
        token = self.get_user_token()
        response = self.client.get(
            "/api/v1/users/1/parcels",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 200)

    def test_user_not_found(self):
        '''
        test a non existing user
        '''
        token = self.get_user_token()
        response = self.client.get(
            "/api/v1/users/1000/parcels",
            headers={
                'Authorization': f'Bearer {token}'
             }
        )
        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.data)['message'], 'User not found')