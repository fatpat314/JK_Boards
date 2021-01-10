from django.forms import ModelForm
from .models import Order, Register

class OrderForm(ModelForm):
    class Meta():
        model = Order
        fields = ['name', 'address', 'country']

class RegisterForm(ModelForm):
    class Meta():
        model = Register
        fields = ['name', 'email', 'phone_number', 'address']
