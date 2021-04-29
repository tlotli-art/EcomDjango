from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


#View for the Loggin page
def loginPage(request):
	"""If we have Post Data take the username and password the user entered and authenticate 
	the user using django authenticate and then login the user 
	""" 
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username= username, password= password)
		Customer.objects.get(user= user, name=user.username, email=user.email)

		#If the user is authenticated redirect the user into the store page
		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Username or Password Incorrect')
	
	context = {}
	return render(request, 'iMarket/login.html')

#Method to logout the user and redirect them to the login page
def logoutUser(request):
    logout(request)
    return redirect('login')

#View for the registration page
def register(request):
	
	#Create a form using the Customised form that we created in forms.py
	form = CreateUserForm
	
	#Condition to process the data from the post and put it into the form
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		#If the form is filled in correctly create a new user,send a flash message then redirect to the login page
		if form.is_valid():
			user = form.save()
			Customer.objects.create(user= user, name=user.username, email=user.email)
			username = form.cleaned_data.get('username')
			messages.success(request, 'Welcome to our market ' + username)
			return redirect('login')

	#Pass the form into the template
	context = {
		'form': form
	}
	return render(request, 'iMarket/register.html', context)

#View For the store page

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	#get all the products and pass them into the template
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'iMarket/store.html', context)

#View for the cart page
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'iMarket/cart.html', context)

#View for the checkout page
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'iMarket/checkout.html', context)

#View to update products on pages
def updateItem(request):
	#Parse the json data as a python dictionary
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	#Quiry a costomer and get the product we passed in and either create or add to the order 
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	'''If the  user action is add, add to the order item quantity and subtract if the action is remove
	then save the order item'''
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	
	#If the order quantity is below 0, delete the order item
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

#View to process the order with a jason response
def processOrder(request):
	#Transaction Id for current time
	transaction_id = datetime.datetime.now().timestamp()
	
	#parse the value of data
	data = json.loads(request.body)

	#Conditional for processing order of a authenticated user and guest user
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	#set the total of the order
	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	#If the total from the fron end is the same as the cart total set order to complete then save order 
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	#Create the shipping address is shipping is set to true
	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		province=data['shipping']['province'],
		postcode=data['shipping']['postcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)