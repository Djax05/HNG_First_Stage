from django.test import TestCase, Client
from django.urls import reverse


class TestHello(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_CountryIp(self):
        response = self.client.get("/hello/", HTTP_X_FORWADED_FOR = '208.67.222.222')
        self.assertEqual(response.status_code, 200) 
