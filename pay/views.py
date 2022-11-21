from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
auth=("rzp_test_4pTTJ8OGXPUjPp", "1PHP4az86CAmwIPpyMHxo9fi"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
'payment_capture': '1'})

    return render(request, 'pay.html')

@csrf_exempt
def success(request):
    return render(request, "success.html")
