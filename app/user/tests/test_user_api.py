from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params) :
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase) :
    #Test the user api (public)
    def setUp(self) :
        self.client = APIClient()

    def test_create_valid_user_success(self) :
        #test creating user with valid payload is successful
        payload = {
            'email' : 'test@samacyc.com',
            'password' : 'testpass' ,
            'name' : 'test name'
        }
        res =self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password' , res.data)

    def test_user_already_exist(self) :
        payload ={
             'email' : 'test@samacyc.com',
            'password' : 'testpass' ,
            'name' : 'test name'
        }
        create_user(**payload)
        res =self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_password (self) :
        payload = {
            'email' : 'test@samacyc.com' ,
            'password' : '@'
        }
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
    def test_create_user_token(self) :
        payload ={
            'email' : 'test@samacyc.com' ,
            'password' : 'testpass'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL , payload)
        self.assertIn('token' , res.data)
        self.assertEqual(res.status_code , 200)

    def test_create_token_invalid_credentials(self) :

        create_user(email = 'test@samacyc.com' , password = 'testpass')
        payload = {
            'email' : 'test@samacyc.com',
            'password' : 'egfdgbj'
        }
        res = self.client.post(TOKEN_URL , payload)
        self.assertIn('non_field_errors' , res.data)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self) :
        payload = {
            'email' : 'test@samacyc.com',
            'password' : 'worngpass'
        }
        res = self.client.post(TOKEN_URL , payload)
        self.assertIn('non_field_errors' , res.data)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
    def test_create_token_missing_field(self) :
        payload = {
            'email' : 'test@samacyc.com',
            'password' : ''
        }
        res = self.client.post(TOKEN_URL , payload)
        self.assertIn('password' , res.data)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
