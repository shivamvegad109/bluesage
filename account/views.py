from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from shop.models import Order, Product, Category
from .forms import MyUserCreationForm
from django.contrib import messages


def create_super_user(request):
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')
    return JsonResponse({"status": "ok"})


def signup(request):
    all_category = Category.objects.all()
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get("username")
            login(request, user)
            return redirect("/")
        else:
            return render(
                request,
                "account/signup.html",
                {
                    "form": form,
                    "error": form.errors,
                    "categories": all_category,
                    "cart": len(request.session.get("cart", {}).keys()),
                },
            )
    else:
        form = MyUserCreationForm()
        return render(
            request,
            "account/signup.html",
            {
                "form": form,
                "error": form.errors,
                "categories": all_category,
                "cart": len(request.session.get("cart", {}).keys()),
            },
        )


def signin(request):
    all_category = Category.objects.all()
    if request.user.is_authenticated:
        return render(request, "homepage.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            form = AuthenticationForm(request.POST)
            user = User.objects.filter(username=username)
            print(user)
            if user.exists():
                messages.error(request, "Email/Password is incorrect")
                return render(
                    request,
                    "account/signin.html",
                    {
                        "form": form,
                        "errors": ["Password is incorrect"],
                        "categories": all_category,
                        "cart": len(request.session.get("cart", {}).keys()),
                    },
                )
            messages.error(request, "Email/Password is incorrect")
            return render(
                request,
                "account/signin.html",
                {
                    "form": form,
                    "errors": ["Username does not exist"],
                    "categories": all_category,
                    "cart": len(request.session.get("cart", {}).keys()),
                },
            )
    else:
        form = AuthenticationForm()
        return render(
            request,
            "account/signin.html",
            {
                "form": form,
                "categories": all_category,
                "cart": len(request.session.get("cart", {}).keys()),
            },
        )


def signout(request):
    logout(request)
    return redirect("home")


def getorder(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    order_details = Order.objects.filter(emailaddress=request.user.email).order_by('created_at')
    context = {
        "orders": order_details,
        "categories": Category.objects.all(),
        "cart": len(request.session.get("cart", {}).keys()),
    }
    


    return render(request, "account/order.html", context)
