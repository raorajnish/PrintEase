from app.models import ShopDetails
from .models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomerRegisterationForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = CustomerRegisterationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Registration successful')
#             return redirect('app:user-dashboard')
#     else:
#         form = CustomerRegisterationForm()
#     return render(request, 'user_register.html',locals())


# Shop Registration View
def shop_register(request):
    if request.method == "POST":
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_shop = True  # Automatically set is_shop=True
            user.is_user = False  # Ensure is_user=False
            user.save()
            return redirect('app:shop-dashboard')   # Redirect to shop login page after registration
    else:
        form = CustomerRegisterationForm()
    return render(request, 'shop_register.html', {'form': form})

# User Registration View
def user_register(request):
    if request.method == "POST":
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True  # Automatically set is_user=True
            user.is_shop = False  # Ensure is_shop=False
            user.save()
            return redirect('app:user-dashboard')  # Redirect to user login page after registration
    else:
        form = CustomerRegisterationForm()
    return render(request, 'user_register.html', {'form': form})

# User Login View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)

                if user.is_shop:
                    # Check if shop details are filled
                    shop_details = ShopDetails.objects.filter(user=user).first()
                    if shop_details and shop_details.details_filled:
                        return redirect('app:shop-dashboard')
                    else:
                        return redirect('app:shop-details-form')  # Redirect to shop details form
                elif user.is_user:
                    return redirect('app:user-dashboard')
                else:
                    messages.error(request, "Invalid user type.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')  # Redirect to login page after logout