from django.urls import path,include
from .views import HomePageView,AboutPageView,TimelinePageView
urlpatterns = [
    
    path('',HomePageView.as_view(),name="home"),
    path('about/',AboutPageView.as_view(),name = "about"),
    path('timeline/',TimelinePageView.as_view(),name="timeline"),

]