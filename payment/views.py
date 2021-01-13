from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import OrderForm, RegisterForm
from django.conf import settings
from django.urls import reverse


import stripe, requests

# Create your views here.
def index(request):
    return render(request, "home.html")

def info(request):
    return render(request, "info.html")

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('payment'))
    context = {'form' : form,}
    return render(request, "register.html", context)

name = 'x'
address = 'x'
country = 'x'
order_info = 'x'

def thanks(request):

    form = OrderForm()

    if request.method == 'POST':
        info = request.POST
        print("INFO", info.dict())
        for key, value in info.dict().items():
            print(key, ' : ', value)
            if key == 'name':
                global name
                name = value
                print("NAME", name)
            if key == 'address':
                global address
                address = value
            if key == 'country':
                global country
                country = value
        global order_info
        order_info = "Name: " + name + ", Address: " + address + ", Country: " + country
        print("ORDER_INFO", order_info)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            """send email"""
            send_simple_message()
            return HttpResponseRedirect(reverse('info'))
    context = {'form' : form,}

    return render(request, "thanks.html", context)

def send_simple_message():
    print("SENT!!!!!")
    return requests.post(
        "https://api.mailgun.net/v3/inclineskateboards.com/messages",
        auth=("api", settings.MAILGUN_PRIVATE_KEY),
        data={"from": "JK_BOARDS <mailgun@inclineskateboards.com>",
              "to": ["w.patrick.kelly@gmail.com", "YOU@inclineskateboards.com"],
              "subject": "NEW ORDER CONFIRMED!!!",
              "text": order_info})

def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = [{
            'price': 'price_1I8yckEkTNLsoF64tWCHXqq5',
            'quantity': 1,
        }],
        mode = 'payment',
        success_url= request.build_absolute_uri(reverse('thanks')),
        cancel_url= request.build_absolute_uri(reverse('info')),
    )


    context = {
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    }

    return render(request, "payment.html", context)
