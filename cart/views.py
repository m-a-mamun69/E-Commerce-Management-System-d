from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def cart_summary(request):
    #Get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})


def cart_add(request):
    # Get the Cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #lookup product in db
        product = get_object_or_404(Product, id=product_id)

        #Save to Session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
		# Get stuff
        product_id = int(request.POST.get('product_id'))
        #Call delete Fuction in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'qty':product_id})
		#return redirect('cart_summary')
        messages.success(request, ("Your Cart Has Been Deleted..."))
        return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response
        # return redirect('cart_summary')
    
