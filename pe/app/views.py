from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import ShopDetailsForm
from .models import ShopDetails
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request, 'base.html')

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

@login_required(login_url='/users/login/')
def user_dashboard(request):
    shops = ShopDetails.objects.all()
    return render(request, "user_dash.html", {"shops": shops})


@login_required(login_url='/users/login/')
def shop_dashboard(request):
    shop_details = get_object_or_404(ShopDetails, user=request.user)
    return render(request, 'shop_dash.html', {'shop_details': shop_details})

@login_required
def shop_details_view(request):
    shop_details, created = ShopDetails.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ShopDetailsForm(request.POST, instance=shop_details)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.details_filled = True  # Mark details as filled
            shop.save()

            # Send email to the shop owner
            subject = "Shop Details Submission Confirmation"
            message = f"""
            Dear {shop.owner_name},

            Thank you for submitting your shop details. Here are the details you provided:

            **Shop Details:**
            - Shop Name: {shop.shop_name}
            - Owner Name: {shop.owner_name}
            - Area: {shop.area}
            - City: {shop.city}
            - State: {shop.state}
            - Pincode: {shop.pincode}
            - Contact Number: {shop.contact_number}
            - GSTIN: {shop.gstin if shop.gstin else 'Not Provided'}
            - Operating Hours: {shop.start_time} - {shop.end_time}

            **Printing Rates:**
            - Black & White Print Price: ₹{shop.bw_price if shop.bw_price else 'Not Provided'} per page
            - Color Print Price: ₹{shop.color_price if shop.color_price else 'Not Provided'} per page

            If any details need to be corrected, please update your form.

            Best Regards,  
            **PrintEase Team**
            """
            recipient_email = request.user.email  # Ensure the user has an email set in their profile
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

            return redirect('app:shop-dashboard')
    else:
        form = ShopDetailsForm(instance=shop_details)

    return render(request, "shop_details_form.html", {"form": form})


@login_required(login_url='/users/login/')
def shop_print_view(request, shop_id):
    shop = get_object_or_404(ShopDetails, id=shop_id)

    if request.method == "POST":
        uploaded_files = request.FILES.getlist("document[]")
        page_options = request.POST.getlist("page_option")
        custom_pages = request.POST.getlist("custom_pages")
        copies = request.POST.getlist("copies")
        print_types = request.POST.getlist("print_type")
        side_options = request.POST.getlist("side_option")

        total_price = 0
        for i, file in enumerate(uploaded_files):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            
            num_pages = 10  
            if page_options[i] == "custom":
                selected_pages = parse_page_numbers(custom_pages[i])
                num_pages = len(selected_pages)

            price_per_page = shop.bw_price if print_types[i] == "bw" else shop.color_price
            total_price += num_pages * int(copies[i]) * price_per_page

        return JsonResponse({"total_price": total_price})

    return render(request, "shop_print.html", {"shop": shop})

def parse_page_numbers(page_string):
    pages = set()
    for part in page_string.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return pages
