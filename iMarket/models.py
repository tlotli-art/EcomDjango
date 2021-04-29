from django.db import models
#import the defaulf django user model
from django.contrib.auth.models import User

#Customer model with a one to one relationship with the django User model
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE,related_name='customer')
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#product model with its atributes
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default= False, null=True, blank= True)
    #image field 
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    #property decorator to access the model method like a attribute
    @property
    #model method to quiry the image url and if it doesnt exist return a empty string.
    #this is to prevent a error if a product doesnt have a image
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#Order model with a many to one relationship with the Customer model
#One Customer can have multiple orders
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_odered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    #Shipping method that loops though all the items and checks if there is a single
    #digital item in the order, if all the products are not digital set the shipping to
    #true
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    #Model method that will calculate the total of the cart
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    #Model method that will calculate the total number of items within the cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#Order item model with a many to one relationship to the Product model and Order model
#One order can have multiple items
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #Model method that will calculate the total value of our order item
    @property
    def get_total(self):
        total = float(self.product.price) * float(self.quantity)
        return total

#Shipping Adress model with a many to one relationship with the customer and order model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address =  models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address