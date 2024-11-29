from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create views for Cart Summary
def cart_summary(request):
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	#size = cart.get_size
	totals = cart.cart_total()
	
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

	

# Adding items to cart
def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		#product_size = int(request.POST.get('product_size'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)#, size=product_size

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		#response = JsonResponse({'size': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response    


# deleting items from cart
def cart_delete(request):
	cart = Cart(request)

	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		

		cart.delete(product=product_id)
		messages.success(request, ("Item Deleted From Cart..."))
		response = JsonResponse({'product':product_id})
		return response




# Update items in the cart
def cart_update(request):
	cart = Cart(request)

	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		messages.success(request, ("Your Cart Has Been Updated..."))
		return redirect('cart_summary')
		#return response
