from django.db.models import Q
from django.shortcuts import render,redirect
from . models import Categories, GreeneryProducts, Feedback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Customer.models import CustomerDetails
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Cart.models import Orders, ProductOrders


# Create your views here.

def home(request):
    product = GreeneryProducts.objects.all()[:6]
    return render(request, 'Index.html', {'product':product})

def shop(request, link=None):
    if link is not None:
        cat = Categories.objects.get(link=link)
        products = GreeneryProducts.objects.filter(category=cat.id)
    else:
        all_items = GreeneryProducts.objects.all()
        paginator = Paginator(all_items, 9) # Show 9 items per page
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
    return render(request, 'shop.html', {'products': products})


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def Product_search(request):
    query = request.GET.get('q')
    if query:
        results =GreeneryProducts.objects.all().filter(Q(product__icontains=query)|
                                                       Q(category__category__icontains=query))
    else:
        results = []
    return render(request, 'shop.html', {'products': results})




def single_product(request):
    greenery = GreeneryProducts.objects.get(id=pro_id)
    fed = Feedback.objects.filter(product=pro_id)
    return render(request,'shop-single.html',{'pro':greenery,'feedback':fed})


def addfeedback(request,pro_id):
    if request.method == 'POST':
        fed = request.POST['Add_Feedback']
        product = GreeneryProducts.objects.get(id=pro_id)
        user = CustomerDetails.objects.get(id=request.user.id)
        if Feedback.objects.filter(user=user,prduct=product).exits():
            messages.info(request,"Review already added")
            return redirect("pro_details",pro_id)
        else:
            Feedback(user=user,product=product,feedback=fed).save()
            return redirect("pro_details",pro_id)

































def single_product(request, pro_id):
    greenery = GreeneryProducts.objects.get(id=pro_id)
    fed = Feedback.objects.filter(product=pro_id)
    return render(request, 'shop-single.html', {'pro':greenery, 'feedbacks':fed})


@login_required(login_url='Customer:login')
def addfeedback(request, pro_id):
    if request.method=='POST':
        fed = request.POST['Add_Feedback']
        product = GreeneryProducts.objects.get(id=pro_id)
        user = CustomerDetails.objects.get(id=request.user.id)
        if Feedback.objects.filter(user=user, product=product).exists():
            messages.info(request, "* Review already added")
            return redirect("pro_details", pro_id)
        else:
            Feedback(user=user, product=product, feedback=fed).save()
            return redirect("pro_details", pro_id)




@login_required(login_url='Customer:login')
def order_confirmation(request):
    cod_order = Orders.objects.filter(user=request.user.id)
    order_products = ProductOrders.objects.filter(order__in=cod_order).order_by('-order__date_time')

    paginator = Paginator(order_products, 6)
    page = request.GET.get('page')
    try:
        order_items = paginator.page(page)
    except EmptyPage:
        order_items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        order_items = paginator.page(1)

    return render(request, 'Order_Confirmation.html', {'order_items': order_items})



