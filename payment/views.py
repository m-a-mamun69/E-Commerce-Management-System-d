from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
# Create your views here.


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the Order
        order = Order.objects.get(id=pk)
        # Get the Order Items
        items = OrderItem.objects.filter(order=pk)

        return render(request, 'payment/orders.html', {"order":order, "items":items})

    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        return render(request, 'payment/not_shipped_dash.html', {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        return render(request, 'payment/shipped_dash.html', {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def process_order(request):
    if request.POST:
        #Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        #Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address From session Info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        
        # Create an Order
        if request.user.is_authenticated:
            # logged in 
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order Items
            # Get the Order id
            order_id = create_order.pk
            # Get Product Info
            for product in cart_products():
                # Get Product id
                product_id = product.id
                # Get Product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()


            #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]


            messages.success(request, "Order Placed!")
            return redirect('home')

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order Items
            # Get the Order id
            order_id = create_order.pk
            # Get Product Info
            for product in cart_products():
                # Get Product id
                product_id = product.id
                # Get Product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

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
