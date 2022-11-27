from django.urls import path,include
from .views import HomePageView,AboutPageView, TimelinePageView,ItemView,ProductView, remove_from_cart,add_to_cart,reduce_quantity_item,OrderSummaryView,CheckoutView
from . import views
from .views import StationaryView,GroceriesView,SnacksView,FruitsView,HomeEssentialsView,ToiletriesView,HygieneView,FoodView,MedicinesView
from .views import payment, SearchResultsView,WarningPageView,FAQPageView,SellerPageView
from .views import ContactView,AvailableView,ReturnView,TermsView,WhatView
app_name = 'pages'

urlpatterns = [
    
    path('',HomePageView.as_view(),name='home'),
    path('about/',AboutPageView.as_view(),name = "about"),
    path('timeline/',TimelinePageView.as_view(),name="timeline"),
    path('sell/',SellerPageView.as_view(),name="sell"),
    path('contact/',ContactView.as_view(),name="contact"),
    path('available/',AvailableView.as_view(),name="available"),
    path('return/',ReturnView.as_view(),name="return"),
    path('terms/',TermsView.as_view(),name="terms"),
    path('what/',WhatView.as_view(),name="what"),
    path('items/',ItemView.as_view(),name="item"),
    path('stationary/',StationaryView.as_view(),name="stationary"),
    path('groceries/',GroceriesView.as_view(),name="groceries"),
    path('snacks/',SnacksView.as_view(),name="snacks"),
    path('fruits/',FruitsView.as_view(),name="fruits"),
    path('homeessentials/',HomeEssentialsView.as_view(),name="homeessentials"),
    path('toiletries/',ToiletriesView.as_view(),name="toiletries"),
    path('hygiene/',HygieneView.as_view(),name="hygiene"),
    path('food/',FoodView.as_view(),name="food"),
    path('medicines/',MedicinesView.as_view(),name="medicines"),
    path('product/<pk>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('search/',SearchResultsView.as_view(),name="search"),
   path('reduce-quantity-item/<pk>/', reduce_quantity_item,name='reduce-quantity-item'),
   path('checkout', CheckoutView.as_view(), name='checkout'),
   path('pay', payment, name='pay'),
   path('warning',WarningPageView.as_view(),name="warning"),
   path('faq/',FAQPageView.as_view(),name="faq"),
    # path('success' , success , name='success')

]