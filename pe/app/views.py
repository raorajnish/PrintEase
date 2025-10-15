from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import ShopDetailsForm
from .models import ShopDetails, Order, OrderItem
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from decimal import Decimal
import os
import PyPDF2
import io

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
    try:
        shop_details = ShopDetails.objects.get(user=request.user)
        
        # Get shop statistics
        shop_orders = Order.objects.filter(shop=shop_details)
        total_orders = shop_orders.count()
        total_earnings = shop_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        pending_orders = shop_orders.filter(status='pending').count()
        
        # Calculate total pages printed
        total_pages = 0
        for order in shop_orders.filter(status__in=['processing', 'ready', 'completed']):
            for item in order.items.all():
                total_pages += item.pages * item.copies
        
        # Get recent orders
        recent_orders = shop_orders.order_by('-created_at')[:5]
        
        context = {
            'shop_details': shop_details,
            'total_orders': total_orders,
            'total_earnings': total_earnings,
            'total_pages': total_pages,
            'pending_orders': pending_orders,
            'recent_orders': recent_orders,
        }
        
    except ShopDetails.DoesNotExist:
        context = {
            'shop_details': None,
            'total_orders': 0,
            'total_earnings': 0,
            'total_pages': 0,
            'pending_orders': 0,
            'recent_orders': [],
        }
    
    return render(request, 'shop_dash.html', context)

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
def shop_details_modal(request, shop_id):
    """View to get shop details for modal popup"""
    shop = get_object_or_404(ShopDetails, id=shop_id)
    
    # Get Indian state name from code
    state_name = dict(ShopDetails._meta.get_field('state').choices).get(shop.state, shop.state)
    
    context = {
        'shop': shop,
        'state_name': state_name,
    }
    
    return render(request, 'shop_details_modal.html', context)


@login_required(login_url='/users/login/')
def shop_print_view(request, shop_id):
    # Get shop and ensure we have the correct one
    try:
        shop = ShopDetails.objects.get(id=shop_id)
        print(f"Found shop: {shop.shop_name} (ID: {shop.id})")
        print(f"Shop prices - B/W: {shop.bw_price}, Color: {shop.color_price}")
        
        # Check for other shops with similar names
        similar_shops = ShopDetails.objects.filter(shop_name__icontains=shop.shop_name.split()[0])
        if similar_shops.count() > 1:
            print(f"Found {similar_shops.count()} shops with similar names:")
            for s in similar_shops:
                print(f"  - {s.shop_name} (ID: {s.id}) - B/W: {s.bw_price}, Color: {s.color_price}")
    except ShopDetails.DoesNotExist:
        messages.error(request, "Shop not found!")
        return redirect('app:user-dashboard')

    if request.method == "POST":
        uploaded_files = request.FILES.getlist("document[]")
        page_options = request.POST.getlist("page_option")
        custom_pages = request.POST.getlist("custom_pages")
        copies = request.POST.getlist("copies")
        print_types = request.POST.getlist("print_type")
        side_options = request.POST.getlist("side_option")
        frontend_total_price = request.POST.get("frontend_total_price", "0")

        try:
            # Create order
            order = Order.objects.create(
                user=request.user,
                shop=shop,
                total_amount=Decimal('0.00')
            )

            total_amount = Decimal('0.00')

            for i, file in enumerate(uploaded_files):
                # Save file
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                
                # Calculate pages
                num_pages = 10  # Default
                if page_options[i] == "custom" and custom_pages[i]:
                    selected_pages = parse_page_numbers(custom_pages[i])
                    num_pages = len(selected_pages)
                else:
                    # Use the page estimation function
                    num_pages = estimate_pages_for_file(file)

                # Calculate price using shop's actual prices
                if print_types[i] == "bw":
                    price_per_page = shop.bw_price or Decimal('0.00')
                else:
                    price_per_page = shop.color_price or Decimal('0.00')
                
                item_total = Decimal(str(num_pages * int(copies[i]) * price_per_page))
                
                # Apply double-sided discount (20% off)
                if side_options[i] == "double":
                    item_total = item_total * Decimal('0.8')
                
                # Debug logging
                print(f"File: {file.name}")
                print(f"Pages: {num_pages}")
                print(f"Copies: {copies[i]}")
                print(f"Print Type: {print_types[i]}")
                print(f"Price per page: {price_per_page}")
                print(f"Side option: {side_options[i]}")
                print(f"Item total: {item_total}")
                print("---")

                total_amount += item_total

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    file_name=file.name,
                    file_path=file_path,
                    page_option=page_options[i],
                    custom_pages=custom_pages[i] if page_options[i] == "custom" else None,
                    copies=int(copies[i]),
                    print_type=print_types[i],
                    side_option=side_options[i],
                    pages=num_pages,
                    price_per_page=price_per_page,
                    total_price=item_total
                )

            # Use frontend calculated price if available, otherwise use backend calculation
            if frontend_total_price and frontend_total_price != "0":
                order.total_amount = Decimal(frontend_total_price)
                print(f"Using frontend calculated price: {frontend_total_price}")
            else:
                order.total_amount = total_amount
                print(f"Using backend calculated price: {total_amount}")
            
            order.save()

            messages.success(request, f"Order placed successfully! Order number: {order.order_number}")
            return redirect('app:past-orders')

        except Exception as e:
            messages.error(request, f"Error placing order: {str(e)}")
            return redirect('app:shop-print', shop_id=shop_id)

    # Ensure shop prices are available and refresh from database
    shop = ShopDetails.objects.get(id=shop_id)  # Refresh from database
    
    if not shop.bw_price:
        shop.bw_price = Decimal('0.00')
    if not shop.color_price:
        shop.color_price = Decimal('0.00')
    
    # Debug: Print shop prices
    print(f"Shop {shop.shop_name} prices:")
    print(f"B/W Price: {shop.bw_price}")
    print(f"Color Price: {shop.color_price}")
    
    return render(request, "shop_print.html", {"shop": shop})


@login_required(login_url='/users/login/')
def past_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "past_orders.html", {"orders": orders})


@login_required(login_url='/users/login/')
def order_details(request, order_id):
    """View to get order details for modal popup"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Calculate total pages
    total_pages = sum(item.pages * item.copies for item in order.items.all())
    
    context = {
        'order': order,
        'total_pages': total_pages,
    }
    
    return render(request, 'order_details_modal.html', context)


@login_required(login_url='/users/login/')
def cancel_order(request, order_id):
    """Cancel an order"""
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Only allow cancellation of pending orders
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f"Order {order.order_number} has been cancelled successfully.")
        else:
            messages.error(request, f"Order {order.order_number} cannot be cancelled. Only pending orders can be cancelled.")
        
        return redirect('app:past-orders')
    
    return redirect('app:past-orders')


@login_required(login_url='/users/login/')
def shop_orders(request):
    """View all orders for a shop"""
    try:
        shop_details = ShopDetails.objects.get(user=request.user)
        orders = Order.objects.filter(shop=shop_details).order_by('-created_at')
        
        context = {
            'orders': orders,
            'shop_details': shop_details,
        }
        
    except ShopDetails.DoesNotExist:
        messages.error(request, "Shop details not found!")
        return redirect('app:shop-dashboard')
    
    return render(request, 'shop_orders.html', context)


@login_required(login_url='/users/login/')
def update_order_status(request, order_id):
    """Update order status"""
    if request.method == "POST":
        try:
            shop_details = ShopDetails.objects.get(user=request.user)
            order = get_object_or_404(Order, id=order_id, shop=shop_details)
            new_status = request.POST.get('status')
            
            if new_status in ['confirmed', 'processing', 'ready', 'completed', 'cancelled']:
                order.status = new_status
                order.save()
                messages.success(request, f"Order {order.order_number} status updated to {order.get_status_display()}")
            else:
                messages.error(request, "Invalid status")
                
        except ShopDetails.DoesNotExist:
            messages.error(request, "Shop details not found!")
        except Exception as e:
            messages.error(request, f"Error updating order: {str(e)}")
    
    return redirect('app:shop-dashboard')


@login_required(login_url='/users/login/')
def analytics(request):
    """Shop analytics page"""
    try:
        shop_details = ShopDetails.objects.get(user=request.user)
        shop_orders = Order.objects.filter(shop=shop_details)
        
        # Overall statistics
        total_orders = shop_orders.count()
        total_earnings = shop_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        total_pages = 0
        for order in shop_orders.filter(status__in=['processing', 'ready', 'completed']):
            for item in order.items.all():
                total_pages += item.pages * item.copies
        
        # Status breakdown
        status_counts = shop_orders.values('status').annotate(count=Count('id'))
        
        # Monthly earnings (last 6 months)
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        monthly_earnings = []
        for i in range(6):
            month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            month_orders = shop_orders.filter(created_at__gte=month_start, created_at__lte=month_end)
            month_earnings = month_orders.aggregate(total=Sum('total_amount'))['total'] or 0
            
            monthly_earnings.append({
                'month': month_start.strftime('%B %Y'),
                'earnings': month_earnings,
                'orders': month_orders.count(),
            })
        
        # Daily earnings (last 30 days)
        daily_earnings = []
        for i in range(30):
            day = timezone.now().date() - timedelta(days=i)
            day_orders = shop_orders.filter(created_at__date=day)
            day_earnings = day_orders.aggregate(total=Sum('total_amount'))['total'] or 0
            
            daily_earnings.append({
                'date': day.strftime('%Y-%m-%d'),
                'earnings': day_earnings,
                'orders': day_orders.count(),
            })
        
        # Recent orders for chart
        recent_orders_data = shop_orders.order_by('-created_at')[:10]
        
        context = {
            'shop_details': shop_details,
            'total_orders': total_orders,
            'total_earnings': total_earnings,
            'total_pages': total_pages,
            'status_counts': status_counts,
            'monthly_earnings': monthly_earnings,
            'daily_earnings': daily_earnings,
            'recent_orders_data': recent_orders_data,
        }
        
    except ShopDetails.DoesNotExist:
        messages.error(request, "Shop details not found!")
        return redirect('app:shop-dashboard')
    
    return render(request, 'analytics.html', context)


def parse_page_numbers(page_string):
    pages = set()
    for part in page_string.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return pages

def estimate_pages_for_file(file):
    """Estimate page count for different file types"""
    filename = file.name.lower()
    
    if filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            page_count = len(pdf_reader.pages)
            file.seek(0)  # Reset file pointer
            return page_count
        except Exception as e:
            print(f"Error reading PDF {file.name}: {e}")
            return 10  # Default fallback
    
    elif filename.endswith(('.doc', '.docx')):
        # For Word documents, estimate based on file size
        # This is a rough estimation - in production you'd want proper parsing
        file_size_mb = file.size / (1024 * 1024)
        estimated_pages = max(1, int(file_size_mb * 2))  # Rough estimate
        return min(estimated_pages, 50)  # Cap at 50 pages
    
    elif filename.endswith(('.ppt', '.pptx')):
        # For PowerPoint, estimate based on file size
        file_size_mb = file.size / (1024 * 1024)
        estimated_pages = max(1, int(file_size_mb * 3))  # Rough estimate
        return min(estimated_pages, 30)  # Cap at 30 pages
    
    elif filename.endswith('.txt'):
        # For text files, estimate based on content length
        try:
            content = file.read().decode('utf-8', errors='ignore')
            lines = content.split('\n')
            estimated_pages = max(1, len(lines) // 50)  # ~50 lines per page
            file.seek(0)  # Reset file pointer
            return min(estimated_pages, 20)  # Cap at 20 pages
        except:
            return 5  # Default for text files
    
    else:
        return 10  # Default for unknown file types
