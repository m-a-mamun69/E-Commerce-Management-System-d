from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages
# Create your views here.

def process_order(request):
    if request.POST:
        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Create Shipping Address From session Info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        print(shipping_address)

        messages.success(request, "Order Placed!")
        return redirect('home')


    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def billing_info(request):
    if request.POST:
        #Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a Session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is logged In
        if request.user.is_authenticated:
            # Get The Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            # Not Logged In
            # Get The Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def checkout(request):
    #Get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as Logged in User
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # Checkout as Guest
        shipping_form = ShippingForm(request.POST or None) 
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def payment_success(request):

    return render(request, 'payment/payment_success.html', {})