import json
from .models import *

#function that handles cookie data for a guest user
def cookieCart(request):

    
    #Trt except call for if we dont have cookies we return a empty dictionary
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    print('Cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    # for loop to update the order with what is found within our cookies 
    for i in cart:

        try:
            #increase cart items on each iteration by the quantity
            cartItems += cart[i]['quantity']
            #quiry the product and set the total
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            #Incremet the cart total and the cart items
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            #dictionary reprisentation of the order
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total':total
            }
            #append the dictionary reprisentation of the order(item) to items
            items.append(item)

            #If the product is not digital, set shipping to true
            if product.digital == False:
                order['shipping'] = True

        #Pass if product does not exist
        except:
            pass

    return{

        'cartItems': cartItems,
        'order': order,
        'items': items

    }

def cartData(request):
    #If the user is authenicated create a order or get an order if it alredy exists
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #If user is a guest get cookies and then update cart items with what is in our cookies
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return{
        'cartItems': cartItems,
        'order': order,
        'items': items
}

def guestOrder(request, data):
    print('User is not logged in') 

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete= False,
        )
    
    for item in items:
        product= Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )

    return customer, order