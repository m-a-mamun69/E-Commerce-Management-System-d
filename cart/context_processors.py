from .cart import Cart

# Create context processor so our cart can work onall page of the site
def cart(request):
    # Return the default data from orn cart
    return {'cart': Cart(request)}