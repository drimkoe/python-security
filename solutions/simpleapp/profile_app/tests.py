from django.contrib.auth import get_user_model
from django.test import TestCase

class TestAuthentication(TestCase):

    def test_authenticated_workflow(self):
        passphrase = 'wool reselect resurface annuity' 
        get_user_model().objects.create_user('user1', password=passphrase) 
        self.client.login(username='user1', password=passphrase) 
        self.assertIn('sessionid', self.client.cookies) 
        response = self.client.get( 
        '/accounts/profile/', 
        secure=True) 
        self.assertEqual(200, response.status_code) 
        self.assertContains(response, 'user1') 
        self.client.logout() 
        self.assertNotIn('sessionid', self.client.cookies)

    def test_prohibit_anonymous_access(self):
        response = self.client.get('/accounts/profile/', secure=True) 
        self.assertEqual(302, response.status_code) 
        self.assertIn('/accounts/login/', response['Location'])  