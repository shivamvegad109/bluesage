from django.shortcuts import render
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from shop.models import Category, Product
import razorpay
from django.views.decorators.csrf import csrf_exempt

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
        auth=("rzp_test_88F3rieZjfa2JB", "ld99CgKD2G8NKlmqANNPVTab")
    )

def homepage(request):
	currency = 'INR'
	amount = 20000 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	
	cart = request.session.get("cart", {})
	all_category = Category.objects.all()
	total_price = 0
	for item in cart:
		temp = {}
		temp["product"] = Product.objects.get(id=int(item))
		temp["quantity"] = cart[item]["quantity"]
		temp["total_price"] = int(cart[item]["quantity"]) * temp["product"].price
		total_price += temp["total_price"]
	context = {
        "cart": len(request.session.get("cart", {}).keys()),
        "categories": all_category,
        "total_price": total_price,
    }
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = "rzp_test_1DP5mmOlF5G5ag",
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url
	print(context)
	return render(request, 'cart/checkout1.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()
