from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.db.models import Count, Q
# Import only the model(s) you need
from .models import Report, userdetails


def home_redirect(request):
    return redirect('index')


def index(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, "index.html", {'username': username})


# Signup View
def signup(request):
    if request.method == "POST":
        full_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = full_name
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def submit_signup(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        upw = request.POST.get('password')

        if not uname or not upw:
            return HttpResponse("All fields required!", status=400)

        userdetails.objects.create(username=uname, userpw=upw)
        return HttpResponse("Account created successfully!")
    return HttpResponse("Method not allowed", status=405)


# Login View (render)
def login_view(request):
    return render(request, 'login.html')


# handles the login form submission
def submit_login(request):
    if request.method != 'POST':
        return redirect('login')

    uname = request.POST.get('username', '').strip()
    upw = request.POST.get('password', '')

    if not uname or not upw:
        messages.error(request, "Username and password are required.")
        return redirect('login')

    try:
        user = User.objects.get(username=uname)
    except User.DoesNotExist:
        messages.error(request, "Invalid username or password.")
        return redirect('login')

    # check_password(raw_password, encoded_password)
    if check_password(upw, user.password):
        request.session['username'] = user.username
        messages.success(request, f"Welcome, {user.username}!")
        return redirect('home')
    else:
        messages.error(request, "Invalid username or password.")
        return redirect('login')


# logout user and clear session
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('index')


# home page (after successful login)
def home(request):
    uname = request.session.get('username')
    if not uname:
        messages.error(request, "Please login first.")
        return redirect('login')
    return render(request, 'home.html', {'username': uname})


# Report submission view
def report_view(request):
    if request.method == "POST":
        report_type = request.POST.get('type')           # form field name="type"
        item_name   = request.POST.get('name')           # form field name="name"
        description = request.POST.get('description')
        location    = request.POST.get('location')
        date_value  = request.POST.get('date')           # optional: YYYY-MM-DD

        # If your model's date field uses auto_now_add, avoid setting it manually
        try:
            auto_now_add = Report._meta.get_field('date').auto_now_add
        except Exception:
            auto_now_add = False

        if auto_now_add:
            Report.objects.create(
                report_type=report_type,
                item_name=item_name,
                description=description,
                location=location
            )
        else:
            Report.objects.create(
                report_type=report_type,
                item_name=item_name,
                description=description,
                location=location,
                date=date_value or None
            )

        messages.success(request, "Report submitted.")
        return redirect('listings')

    return render(request, 'report.html')


def edit_report(request, id):
    report = get_object_or_404(Report, id=id)

    if request.method == "POST":
        # update fields from POST data
        report.report_type = request.POST.get('type', report.report_type)
        report.item_name = request.POST.get('name', report.item_name)
        report.description = request.POST.get('description', report.description)
        report.location = request.POST.get('location', report.location)
        date_val = request.POST.get('date')
        if date_val:
            report.date = date_val
        report.save()
        messages.success(request, "Report updated.")
        return redirect('listings')

    return render(request, 'edit_report.html', {'report': report})


def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        report.delete()
        messages.success(request, "Report deleted.")
        return redirect('listings')
    # Protect against GET deletes — redirect back
    messages.error(request, "Invalid request.")
    return redirect('listings')


def listings(request):
    # Order by the actual field defined in your model.
    items = Report.objects.order_by('-date')
    return render(request, 'listings.html', {'items': items})

def view_listings(request):
    items = Report.objects.all().order_by('-date')
    return render(request, 'listings.html', {'items': items})


def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    
    # Optional: Ensure only the user who created the report can delete it
    # if report.user != request.user:
    #     return redirect('listings')
    
    report.delete()
    return redirect('listings')

def dashboard(request):
    lost_count = Report.objects.filter(report_type__iexact='lost').count()
    found_count = Report.objects.filter(report_type__iexact='found').count()
    users_count = User.objects.count()

    # Option A: pending = total reports
    pending_count = Report.objects.count()

    # Option B (alternate): pending = lost reports awaiting match
    # pending_count = lost_count

    context = {
        'lost_count': lost_count,
        'found_count': found_count,
        'users_count': users_count,
        'pending_count': pending_count,
    }
    return render(request, 'dashboard.html', context)

def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(item, id=item_id)
        item.delete()
        messages.success(request, 'Item deleted successfully!')
    return redirect('dashboard')