import json
import datetime

from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Order, OrderItem, ShippingAddress, Customer
from .utils import cart_info, guest_cart, guest_order


# Create your views here.
def store(request):
    
    cart_data = cart_info(request)
    cart_items = cart_data['cart_items']
    
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
    return render(request, 'store/store.html', context)


def checkout(request):
    
    cart_data = cart_info(request)
    cart_items = cart_data['cart_items']
    order = cart_data['order']
    items = cart_data['items']
    
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)


def cart(request):
    
    cart_data = cart_info(request)
    cart_items = cart_data['cart_items']
    order = cart_data['order']
    items = cart_data['items']
    
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def update_item(request):
    
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
       
    return JsonResponse('Item was added', safe=False)


def get_queryset(search=None):
    
    queryset = []
    queries = search.split()
    for query in queries:
        posts = Product.objects.filter(
            Q(name__icontains=query)
        )
    
        for post in posts:
            queryset.append(post)
            
    return list(set(queryset))


def process_order(request):
    
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    
    return JsonResponse('Payment submitted', safe=False)

