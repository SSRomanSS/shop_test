from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import Order
from .forms import OrderForm


# Create your tests here.
class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):
    def test_login(self):
        user = User.objects.create(username='test_user')
        user.set_password('qwerty')
        user.save()
        c = Client()
        logged_in = c.login(username='test_user', password='qwerty')
        self.assertTrue(logged_in)


class StudentModelTests(TestCase):
    def test_str(self):
        order = Order(name='Product', price='1000', user='test_user')
        self.assertEqual(str(order), 'Product costs 1000 ordered by test_user')


class NewOrderSent(TestCase):
    def test_forms(self):
        form_data ={'name': 'Order',
                    'price': '1000'}
        form = OrderForm(form_data)
        self.assertTrue(form.is_valid())
