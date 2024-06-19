from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get Request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        #If the user is new, no session key! Create One!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all page of site
        self.cart = cart


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            # self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save Carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            # self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save Carty to the Profile Model
            current_user.update(old_cart=str(carty))
    

    def cart_total(self):
        # Get Product IDS
        product_ids = self.cart.keys()
        # Lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():

            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total 
    

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids From Cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # Return Those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

		# Get cart
        ourcart = self.cart
		# Update Dictionary/cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save Carty to the Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete From Dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save Carty to the Profile Model
            current_user.update(old_cart=str(carty))