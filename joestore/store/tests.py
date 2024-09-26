from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import *

class TestStore(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser',
                                            password='password')
        self.book = Product.objects.create(name='book', price=20)
        self.laptop = Product.objects.create(name='laptop', price=250)
        self.headset = Product.objects.create(name='headset', price=100)
        self.smartphone = Product.objects.create(name='smartphone', price=150)
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        self.client.login(username='testuser', password='password')


    def test_product_addition(self) -> None:
        cart, _ = Order.objects.get_or_create(
            customer=self.user.customer,
            complete=False)
        OrderItem.objects.get_or_create(
            order=cart,
            product=self.book,
            quantity=1)
        OrderItem.objects.get_or_create(
            order=cart,
            product=self.laptop,
            quantity=2)
        OrderItem.objects.get_or_create(
            order=cart,
            product=self.headset,
            quantity=1)
        self.assertEqual(cart.get_cart_total,
            (self.book.price+(self.laptop.price*2)+self.headset.price))
        self.assertEqual(cart.get_cart_items, 4)
