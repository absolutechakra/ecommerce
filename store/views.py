from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Order, OrderItem
import json


# Create your views here.
def store(request):
    
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    products = Product.objects.all()
    context = {'items': items, 'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def checkout(request):
    
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def cart(request):
    
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print ('Action:', action)
    print ('Product ID: ', product_id)
    
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

