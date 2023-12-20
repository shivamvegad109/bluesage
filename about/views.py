from django.shortcuts import render

from shop.models import Category


# Create your views here.
def about_page(request):
    return render(request, 'about/about.html')

def wishlist(request):
    product = request.session.get('wishlist', {})
    print(product)
    all_category = Category.objects.all()
    context = {
        'product': product,
        'cart': len(request.session.get('cart', {}).keys()),
        'categories': all_category
    }

    print(context)

    return render(request, 'shop/wishlist.html', context)

