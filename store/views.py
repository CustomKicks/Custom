from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.http import  HttpResponse
from django.utils.translation import  gettext as _
from django.db.models import Q
import json
from cart.cart import Cart
import random
from django.contrib.auth.decorators import login_required



# home page Route/View
def home(request):
    output = _("TEST")
    products = Product.objects.all()
    #products = Product.objects.order_by('?')[:6]
    #products = Product.objects.all()[:12]
    return render(request, 'home.html', {'products':products})


# About bage
def about(request):
    return render(request, 'about.html', {})


# Login
def login_user(request):
    # Determine if user filled the form
    if request.method == 'POST':
        # Inputs linked to to the login.html form 
        # <input type="text" class="form-control" name="username" placeholder="Username"> 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff 
            # Get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            # get thier save cart in the DB model
            saved_cart = current_user.old_cart 
            # convert db str to python dict
            if saved_cart:
                # convert
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ('Login Was Successful!'))
            return redirect('home')
        else:
            messages.success(request, ('Login Not Successful! Try Again!!'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


# Logout
def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out!"))
    return redirect('home')


# Register Users
def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Username & Account Created, Fill Out User Info. '))
            return redirect('update_info')
        
        else:
            messages.success(request, ('Registration Not Successfully. Try Again!!'))
            return redirect('register')   
    else:
        return render(request, 'register.html', {'form':form})


# update User Account

def update_user(request):
	if request.user.is_authenticated:
        # What/Which user is authenticated/
		current_user = User.objects.get(id=request.user.id)
        # create form
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

        # Validate  the form and its content and login user
		if user_form.is_valid():
			user_form.save()
			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('update_info')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')
     
# update User Account
def update_password(request):
    # Authenticate User
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password Updated!!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})#          
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')    

# User Info

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')
    
"""
def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})"""


# Individual product page
def product(request, pk):
    # Query the DB table to get product id for each selected product
    product = Product.objects.get(id=pk)
    # pass the product to the product.html file to be viewed/shown
    #products = Product.objects.all()[:4]
    products = Product.objects.order_by('?')[:6]
    return render(request, 'product.html', {'product':product, 'products':products} )


# Category page later will be used as a search filter
def category(request, cat):
    cat = cat.replace('-', ' ')
    # filter the Category Model by product category
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
        #return render(request, 'category.html', {'product':product, 'category':category})
    except:
        messages.success(request, ("Category Doesn't Exist!"))
        return redirect('home')


'''
#test
#def all(request):
 #   all = Category.objects.all()

    return render(request, 'all.html', {'all': all})
'''

# Search for products
def search(request):
    # Determine if the user filled the form
    if request.method == 'POST':
        searched = request.POST['searched']
        # Lets query the products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        # Test for Null searches
        if not searched:
            messages.success(request, ("Searched Item Doesn't Not Exist"))
            return render(request, 'search.html')
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html')