from django.shortcuts import render, redirect, get_object_or_404
from Customer.models import CustomerDetails
from Shop.models import GreeneryProducts
from . models import Cart, CartItem, Orders, ProductOrders, Payment
from django.http import HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required




@login_required(login_url='Customer:login')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




@login_required(login_url='Customer:login')
def add_cart(request, product_id):
    user = CustomerDetails.objects.get(id=request.user.id)
    product = GreeneryProducts.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(user = request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request), user=user)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart_detail')




@login_required(login_url='Customer:login')
def cart_details(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(user=request.user.id)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total,counter=counter))



@login_required(login_url='Customer:login')
def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user.id)
    product = get_object_or_404(GreeneryProducts, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


@login_required(login_url='Customer:login')
def full_remove(request, product_id):
    cart = Cart.objects.get(user=request.user.id)
    product = get_object_or_404(GreeneryProducts, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


@login_required(login_url='Customer:login')
def checkout(request, total=0, counter=0):
    user_detail = CustomerDetails.objects.get(id=request.user.id)
    cart = Cart.objects.get(user=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        counter += cart_item.quantity
    return render(request, 'checkout.html', {"cart_items": cart_items,
                                             'total':total, 'user_detail':user_detail, 'cart_id':cart.id})



@login_required(login_url='Customer:login')
def PlaceOrder(request):
    if request.method == 'POST':
        add = request.POST['c_address']
        type = request.POST['payment_option']
        user_detail = CustomerDetails.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=request.user.id)
        total_amount = 0

        order = Orders.objects.create(user=user_detail, cart_id=cart, payment_type=type, address=add,
                                      payment_status=False)

        order.save()

        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            # Reduce stock for each product in the order
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

            total_amount += (product.price * cart_item.quantity)

            ProductOrders.objects.create(order=order, product=product, quantity=cart_item.quantity,
                                         product_total=product.price * cart_item.quantity)
        order.amount = total_amount
        order.save()

        cart_items.delete()

        if type == '1':
            return render(request, 'thankyou.html')
        else:
            return redirect('payments', order.id)
    return HttpResponseNotAllowed(['POST'])




@login_required(login_url='Customer:login')
def payments(request, order_id):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        name = request.POST.get('card_name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')
        user_detail = CustomerDetails.objects.get(id=request.user.id)
        orders = Orders.objects.get(id=order_id)

        pay = Payment(
            user=user_detail,
            order=orders,
            card_number=card_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv
        )
        pay.save()
        orders.payment_status = True
        orders.save()
        return render(request, 'thankyou.html')
    return render(request, 'online_payment.html')





