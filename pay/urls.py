from django.urls import path
from  .views import home, success
app_name = 'pay'
urlpatterns = [
    path('pay', home, name='pay'),
     path('success' , success , name='success')
]