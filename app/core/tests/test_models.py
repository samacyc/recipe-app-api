from django.test import TestCase
from django.contrib.auth import get_user_model




class ModelTests(TestCase) : 

    def test_create_user_with_email_successfull(self) : 
        #test creating a new user with an email is successfull
        email = 'test@samcyc.com'
        password = '135462798'
        user = get_user_model().objects.create_user(
            email = email , 
            password = password
        )

        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self) :
        email = 'test@SAMACYC.com'
        user = get_user_model().objects.create_user(email , 'jfnjbf nj')

        self.assertEqual(user.email , email.lower())
    
    def test_new_user_invalid_email(self) : 
        with self.assertRaises(ValueError) :
            get_user_model().objects.create_user(None , 'jgfbh')
    
    def test_create_new_super_user(self) : 
        user = get_user_model().objects.create_superuser(
            'zfrhdrgh@gmail.com' , 
            'sfuhfh'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)