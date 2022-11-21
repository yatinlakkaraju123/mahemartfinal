from asyncio.windows_events import NULL
from email.policy import default
from pickle import FALSE
from django.db import models
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.
# model which stores item data




class Item(models.Model) :
    CATEGORY = (
    ('ST', 'Stationary'),
    ('GR', 'Groceries'),
    ('SN', 'Snacks'),
    ('FV','fruits and vegetables'),
    ('HE','home essentials'),
    ('TI','toiletries'),
    ('HG','hygiene'),
    ('FO','food'),
    ('MD','medicines'),
)
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    seller = models.CharField(max_length=50,null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    
    description = models.TextField()
    image = models.ImageField(upload_to='images',default=NULL)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("pages:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self) :
        return reverse("pages:add-to-cart", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_cart_url(self) :
        return reverse("pages:remove-from-cart", kwargs={
            "pk" : self.pk
        })
   
        

    
# OrderItem stores data of the product you want to order and the amount of the product
class OrderItem(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"
    def get_total_item_price(self):
        return self.quantity * self.item.price
    def get_final_price(self):
        return self.get_total_item_price()
# The Order model will store detailed information of the orders made, but in this part of the tutorial we will not display complete order information, we will add another field in the next part.
class Order(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
#CheckoutAddress which will store the shipping address of the order
class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=FALSE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username