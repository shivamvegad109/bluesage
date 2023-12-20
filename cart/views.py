from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from shop.models import Category, Order, Product
import razorpay
import uuid
from django.views.decorators.csrf import csrf_exempt


def cart_page(request):
    cart = request.session.get("cart", {})
    context = []
    total_price = 0
    delivery_charge = 0
    for item in cart:
        temp = {}
        print(item)
        temp["product"] = Product.objects.get(id=int(item))
        temp["quantity"] = cart[item]["quantity"]
        temp["total_price"] = int(cart[item]["quantity"]) * temp["product"].price
        total_price += temp["total_price"]
        context.append(temp)
    all_category = Category.objects.all()
    data_context = {
        "cart_product": context,
        "total_price": total_price,
        "delivery_charge": delivery_charge,
        "cart": len(request.session.get("cart", {}).keys()),
        "categories": all_category,
        "discount": 0,
    }

    return render(request, "cart/cart.html", data_context)


def remove_from_cart(request):
    cart = request.session.get("cart", {})
    product_id = request.POST.dict()["id"]
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return JsonResponse({"status": "ok"})


def checkout(request):
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
    if total_price == 0:
        return render(request, "cart/cart.html", context)
    return render(request, "cart/checkout.html", context)

import razorpay
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
def payment(request):
    
    data = request.POST.dict()
    if not request.user.is_authenticated:
        User.objects.create_user(
            username=data["emailaddress"],
            password=data["password"],
            email=data["emailaddress"],
            first_name=data["firstname"],
            last_name=data["lastname"],
        )
        user = authenticate(
            request, username=data["emailaddress"], password=data["password"]
        )
        login(request, user)

    cart = request.session.get("cart", {})
    order_id = uuid.uuid4().hex[:10]
    razorpay_client = razorpay.Client(
        auth=("rzp_test_88F3rieZjfa2JB", "ld99CgKD2G8NKlmqANNPVTab")
    )
    total_price = 0
    items_data = []
    for item in cart:
        temp = {}
        item_product = Product.objects.get(id=int(item))
        temp["product_name"] = item_product.name
        temp["quantity"] = cart[item]["quantity"]
        temp["total_price"] = int(cart[item]["quantity"])  * item_product.price
        # * temp["product"].price
        total_price += temp["total_price"]
        items_data.append(temp)
    payment = razorpay_client.order.create(
        {"amount": total_price, "currency": "INR", "payment_capture": "1"}
    )
    print(items_data,payment)
    print(data,"dasda")
    Order.objects.create(
        order_id=order_id,
        firstname=data["firstname"],
        lastname=data["lastname"],
        state=data["state"],
        streetaddress=data["streetaddress"],
        streetaddress1=data["streetaddress1"],
        towncity=data["towncity"],
        postcodezip=data["postcodezip"],
        phone=data["phone"],
        emailaddress=data["emailaddress"],
        total_price=total_price,
        items=items_data,
        payment_id=payment["id"],
        payment_status="pending",
    )

    return JsonResponse(
        {
            "status": "ok",
            "payment": payment,
            "order_id": order_id,
            "total_price": total_price,
            "id": payment["id"]
        }
    )


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            razorpay_client = razorpay.Client(
                auth=("rzp_test_88F3rieZjfa2JB", "ld99CgKD2G8NKlmqANNPVTab")
            )

            # get the required parameters from post request.
            payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
            print(params_dict, "params_dict")
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                order = Order.objects.get(payment_id=payment_id)
                order.payment_status = "success"
                order.payment_signature = signature
                order.payment_order_id = razorpay_order_id
                order.save()
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,", result)
                return render(request, "cart/paymentsuccess.html")
            else:
                # if signature verification fails.
                return render(request, "cart/paymentfail.html")
        except razorpay.errors.SignatureVerificationError as e:
            # if signature verification fails.
            return render(request, "cart/paymentfail.html")

    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


# def place_order(request):
#     # razor pay integration
#     '''
#     Key Id
#     rzp_test_88F3rieZjfa2JB
#     Key Secret
#     ld99CgKD2G8NKlmqANNPVTab

#     '''
#     data = request.POST.dict()
#     print(data)
#     total_price = data["total_price"]
#     print(total_price)
#     address = data["address"]
#     print(address)
#     order_id = uuid.uuid4().hex[:10]
#     print(order_id)
#     razorpay_client = razorpay.Client(
#     auth=("rzp_test_88F3rieZjfa2JB", "ld99CgKD2G8NKlmqANNPVTab"))
#     payment = razorpay_client.order.create({'amount': total_price, 'currency': 'INR', 'payment_capture': '1'})
#     print(payment)
#     razorpay_order_id = payment['id']
#     callback_url = 'paymenthandler/'
#     context = {
#         "cart": len(request.session.get("cart", {}).keys()),
#         "payment": payment,
#         "order_id": order_id,
#         "address": address,
#         "total_price": total_price,
#         "callback_url": callback_url,
#         'razorpay_merchant_key': 'rzp_test_88F3rieZjfa2JB',
#         'razorpay_order_id': razorpay_order_id,
#         'currency' : 'INR',
#         'razorpay_amount' : total_price


#     }
#     return render(request, "cart/payment.html", context)
