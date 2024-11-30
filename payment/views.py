from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from cart.cart import Cart
from django.contrib.auth .models import User
from store.models import Product, Profile
#
def payment_success(request):
	return render(request, "payment/payment_success.html", {})


def checkout(request):
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	#size = cart.get_size
	totals = cart.cart_total()
	
	if request.user.is_authenticated:
		# Checkout as a User
		shipping_user = ShippingAddress.objects.get(id=request.user.id)
		# Shipping form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_form': shipping_form})
	else:
		# Checkout as a guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_form': shipping_form})


def billing_info(request):
	if request.POST:

		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		#size = cart.get_size
		totals = cart.cart_total()
		# Create a session with billing info 
		my_shipping = request.POST 
		request.session['my_session'] = my_shipping

		# chect if user is loggedin
		if request.user.is_authenticated:
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_info': request.POST, 'billing_form':billing_form})
		else:
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_info': request.POST, 'billing_form':billing_form})


		shipping_form = request.POST
		return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_info': shipping_info})
	else:
		messages.error(request, "Access Denied")
		return redirect('home')
	


def process_order(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		#size = cart.get_size
		totals = cart.cart_total()
		payment_form = PaymentForm(request.POST)
		# Get Shipping Session Stuff
		my_shipping = request.session.get('my_session')
		

		# Lets Gether Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		
		#let craeet shipping address from my_shipping 
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_province']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n "
		amount_paid =  totals
		

		# Create and order
		if request.user.is_authenticated:
			# Loggedin user
			user = request.user
			# craeet order 
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")

			messages.success(request, ('Order Placed!'))
			return redirect('home')
		
		else:
			# Not loggedin 
			# craeet order 
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()


			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			messages.success(request, ('Order Placed!'))
			return redirect('home')



	else:
		messages.success(request, ('Access Denied!'))
		return redirect('home')