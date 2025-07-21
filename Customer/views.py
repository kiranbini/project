from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from . models import CustomerDetails
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        f_name = request.POST['c_fname']
        l_name = request.POST['c_lname']
        mail = request.POST['c_email']
        contact = request.POST['c_phone']
        passwd = request.POST['c_password']
        cpasswd = request.POST['con_password']
        address = request.POST['c_message']
        photo = request.FILES['image']
        if passwd==cpasswd:
            if User.objects.filter(username=mail).exists():
                messages.info(request, 'User already exists')
            else:
                user = User.objects.create_user(username=mail, password=passwd)
                customer = CustomerDetails(id=user, first_name=f_name, last_name=l_name, phone=contact,
                                           address=address, photo=photo)
                user.save()
                customer.save()
                return redirect('Customer:login')
        else:
            messages.info(request, 'Mismatch Password')
    return render(request, 'Register.html')



def login(request):
    if request.method == 'POST':
        mail = request.POST['c_email']
        password = request.POST['c_password']
        user = auth.authenticate(username=mail, password=password)

        if user is not None and CustomerDetails.objects.filter(id=user.id).exists():
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
    return render(request, 'Login.html')


def Logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url='Customer:login')
def Customer_Profile(request):
    profile = CustomerDetails.objects.get(id=request.user.id)
    return render(request, 'Profile.html', {'profile':profile})
