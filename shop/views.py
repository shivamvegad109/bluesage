from django.shortcuts import render
from .models import Category, Product


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)
    all_category = Category.objects.all()
    context = {
        'product': product_details,
        'related_products': related_products,
        'cart': len(request.session.get('cart', {}).keys()),
        'categories': all_category

    }
    return render(request, 'shop/product-details.html', context)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    all_category = Category.objects.all()
    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    print(len(request.session.get('cart', {}).keys()))
    context = {
        'category': category,
        'products': products,
        'categories': all_category,
        'paginator': paginator,
        'cart': len(request.session.get('cart', {}).keys())

    }
    return render(request, 'shop/category.html', context)

from django.http import JsonResponse

def add_product(request):
    product_data =  request.POST.dict()
    data = request.session.get('cart', {})
    print(data)
    print(product_data)
    if data=={}:
        request.session['cart'] = {}
    if product_data['product_id'] not in data:
        data[product_data['product_id']] = product_data
        request.session['cart'] = data
        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Product already in cart'})

def add_prodcut_to_wishlist(request):
    product_data =  request.POST.dict()
    data = request.session.get('wishlist', {})
    print(data)
    print(product_data)
    if data=={}:
        request.session['wishlist'] = {}
    if product_data['id'] not in data:
        data[product_data['id']] = product_data
        request.session['wishlist'] = data
        return JsonResponse({'status': 'success', 'message': 'Product added to wishlist'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Product already in wishlist'})

    # return render(request, 'shop/category.html', context)

def view_cart(request):
    cart = request.session.get('cart', [])
    context = {
        'cart': cart
    }
    return render(request, 'shop/cart.html', context)


def wishlist(request):
    product = request.session.get('wishlist', {})
    print(product)
    all_category = Category.objects.all()
    products = Product.objects.filter(id__in=product.keys())
    print(products)
    context = {
        'products': products,
        'cart': len(request.session.get('cart', {}).keys()),
        'categories': all_category
    }

    print(context)

    return render(request, 'shop/wishlist.html', context)

def remove_from_wishlist(request):
    product_id = request.POST.dict()['id']
    wishlist = request.session.get('wishlist', {})
    if str(product_id) in wishlist:
        del wishlist[str(product_id)]
    request.session['wishlist'] = wishlist
    return JsonResponse({'status': 'ok'})