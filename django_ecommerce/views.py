from django.shortcuts import render
from shop.models import Product, Category
from contact.forms import SubscriberForm


def home_page(request):
    products = Product.objects.all()[:8]
    category1 = Category.objects.all()[:2]
    category2 = Category.objects.all()[2:4]
    category= Category.objects.all()
    forms = SubscriberForm()
    if request.method == 'POST':
        forms = SubscriberForm(request.POST)
        if forms.is_valid():
            forms.save()
    context = {
        'products': products,
        'forms': forms,
        'categories1': category1,
        "categories2": category2,
        'categories': category,
        'cart': len(request.session.get('cart', {}).keys())
    }
    print(context,"context")
    return render(request, 'home.html', context)
