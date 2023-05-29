from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Payment
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.


def productPage(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'productPage.html', context=context)


def checkout(request, id):
    if (id == 'success' or id == "cancel"):
        # try:
        # print(request.COOKIES['pay'])
        # if request.COOKIES['pay'] == 'ok':
        #     return render(request, 'success.html')

        return HttpResponse(id)

    if request.method == 'POST':
        DOMAIN = "http:localhost:8000/"
        # product = Product.objects.filter(id=id).first()
        email = request.POST['email']
        name = request.POST['name']
        amount = int(request.POST['amount'])
        # transaction_id =
        print(email, name, amount)
        try:
            checkout_session = stripe.checkout.Session.create(
                # get this data from .env
                api_key="sk_test_51N2DERSGIv7bXlyaiezp5tnQLiWbprrerbvmGHU9MgL4prUrikRqHxU5uzkx50hn9ErxsYxz68N40PCYGR6tFNPB00uI9WfTpn",
                line_items=[
                    {
                        "price_data": {
                            'currency': 'inr',
                            'unit_amount': amount*100,
                            'product_data': {
                                'name': name
                            },
                        },

                        "quantity": 1
                    },
                ],
                metadata={
                    "amount": amount,
                    "name": name,
                    "email": email
                },
                mode='payment',
                success_url='http://localhost:8000/checkout/success/',
                cancel_url='http://localhost:8000/checkout/cancel/'
            )
        # try:
        except Exception as e:
            return HttpResponse(e)
        return redirect(checkout_session.url, code=303)

    return HttpResponse("Bad Request")


@csrf_exempt
def webhook_handler(request):
    payload = request.body
    event = None
    line_items = []

    try:
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        # print(event)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        # session = stripe.checkout.Session.retrieve(
        #     event['data']['object']['id'],
        #     expand=['line_items'], api_key="sk_test_51N2DERSGIv7bXlyaiezp5tnQLiWbprrerbvmGHU9MgL4prUrikRqHxU5uzkx50hn9ErxsYxz68N40PCYGR6tFNPB00uI9WfTpn"
        # )
        session = event['data']['object']
        email = session['customer_details']['email']
        data = {
            "email": email,
            "meta": session['metadata'],
            "payment": True
        }
        request.session['payment_done'] = True
        fulfill(request, data)

    # Fulfill the purchase...
    # print(line_items)
  # Passed signature verification
    response = HttpResponse(status=200)
    response.set_cookie('pay', 'ok')
    return response


def fulfill(request, data):
    print(data)
    # payment = Payment(cust_email=data['meta']['email'],amount=data['meta']['amount'])
    print(data['meta']['email'], data['meta']['amount'])
    # request.session['data'] = data
    # return redirect('/checkout/success/')
    pass
