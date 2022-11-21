from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist                   
from django.shortcuts import render, get_object_or_404, redirect                      
from django.views.generic import ListView, DetailView  ,View                    
from django.utils import timezone 
from .forms import CheckoutForm                      
from .models import (                           
    Item,
    Order,
    OrderItem,
    CheckoutAddress,
    Payment
)
from django.db.models import Q 
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.
def my_login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user  
        if not (user.id ):
            return redirect("pages:warning", )
        else:
            return function(request, *args, **kw)
    return wrapper
class HomePageView(TemplateView):
    template_name = "home.html"
class WarningPageView(TemplateView):
    template_name = "warning.html"
class AboutPageView(TemplateView):
    template_name = "about.html"
class TimelinePageView(TemplateView):
    template_name = "timeline.html"
class FAQPageView(TemplateView):
    template_name = "faq.html"
class ItemView(ListView):
    model = Item
    template_name = "item.html"
class StationaryView(ListView):
    model = Item
    template_name = "stationary.html"
class GroceriesView(ListView):
    model = Item
    template_name = "groceries.html"
class SnacksView(ListView):
    model = Item
    template_name = "snacks.html"
class FruitsView(ListView):
    model = Item
    template_name = "fruits.html"
class HomeEssentialsView(ListView):
    model = Item
    template_name = "homeessentials.html"
class ToiletriesView(ListView):
    model = Item
    template_name = "toiletries.html"
class HygieneView(ListView):
    model = Item
    template_name = "hygiene.html"
class FoodView(ListView):
    model = Item
    template_name = "food.html"
class MedicinesView(ListView):
    model = Item
    template_name = "medicines.html"
class SearchResultsView(ListView):
    model = Item
    template_name = "search_results.html"
    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Item.objects.filter(
            Q(item_name__icontains=query) 
        )
        return object_list

class ProductView(DetailView):
    model = Item
    template_name = "product.html"
@my_login_required
def add_to_cart(request, pk) :
    item = get_object_or_404(Item, pk = pk )
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered= False)

    if order_qs.exists() :
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists() :
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("pages:order-summary", )
           
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("pages:order-summary", )
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("pages:order-summary", )
@my_login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.item_name+"\" remove from your cart")
            return redirect("pages:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("pages:product", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("pages:product", pk = pk)
class OrderSummaryView(LoginRequiredMixin, View):
    
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")
@my_login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("pages:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("pages:order-summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("pages:order-summary")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("pages:order-summary")
        
import razorpay
client = razorpay.Client(auth=("rzp_test_4pTTJ8OGXPUjPp", "1PHP4az86CAmwIPpyMHxo9fi"))     
def payment(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        amount = int(order.get_total_price() * 100)
        price = int(amount/100)
        
    except:
            return HttpResponse("No product in cart")    

    razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency='INR',  payment_capture='1' ))
    
    payment = Payment()
            
    payment.user = request.user
    payment.amount = amount/100
    payment.paid = True  
    payment.save()

            # assign payment to order
    order.ordered = True
    order.payment = payment
    order.save()
    #payment.payment_id = razorpay_order.id
    
    return render(request,"pay.html",{'amount':amount,'price':price})


       



    
    
