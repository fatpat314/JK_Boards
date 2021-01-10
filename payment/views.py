from django.shortcuts import render
from django.http import HttpResponse
from .forms import OrderForm
from django.conf import settings
from django.urls import reverse


import stripe, requests

# Create your views here.
def index(request):
    form = OrderForm()

    if request.method == 'POST':
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form' : form,}
    return render(request, "home.html", context)

def thanks(request):
    """send email"""
    # send_simple_message()

    form = OrderForm()

    if request.method == 'POST':
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form' : form,}

    return render(request, "thanks.html", context)

def send_simple_message():
    print("SENT!!!!!")
    return requests.post(
        "https://api.mailgun.net/v3/inclineskateboards.com/messages",
        auth=("api", settings.MAILGUN_PRIVATE_KEY),
        data={"from": "MAILGUN TEST <mailgun@inclineskateboards.com>",
              "to": ["w.patrick.kelly@gmail.com", "YOU@inclineskateboards.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = [{
            'price': 'price_1I77x6EkTNLsoF64jpgmu7k4',
            'quantity': 1,
        }],
        mode = 'payment',
        success_url= request.build_absolute_uri(reverse('thanks')) + '?session_id={CEHCKOUT_SESSION_ID}',
        cancel_url= request.build_absolute_uri(reverse('index')),
    )
    context = {
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    }

    return render(request, "payment.html", context)
