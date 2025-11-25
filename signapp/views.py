from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # <--- Using Built-in User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Placeholders for API (Keep these so urls.py doesn't break)
def register_user(request): return redirect('registration:login_html')
def list_users(request): return redirect('registration:login_html')
def user_detail(request, pk): return redirect('registration:login_html')

# ---------- LOGIN ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('registration:users_html')

    if request.method == 'POST':
        # Django Admin uses USERNAME, not Email
        u = request.POST.get('username') 
        p = request.POST.get('password')

        # Check against Django Admin database
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            return redirect('registration:users_html')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('registration:login_html')

# ---------- USERS LIST ----------
@login_required(login_url='registration:login_html')
def users_html(request):
    # Get all users from Django Admin
    users = User.objects.all().order_by('id')
    return render(request, 'user_list.html', {'users': users})

# ---------- CREATE USER ----------
@login_required(login_url='registration:login_html')
def user_create_html(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'user_form.html', {'title': 'Add User'})

        try:
            # Create standard Django User
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, "User created successfully.")
            return redirect('registration:users_html')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'user_form.html', {'title': 'Add User'})

# ---------- UPDATE USER ----------
@login_required(login_url='registration:login_html')
def user_update_html(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Update password only if provided
        new_pass = request.POST.get('password')
        if new_pass:
            user.set_password(new_pass)
            
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('registration:users_html')

    return render(request, 'user_form.html', {'title': 'Edit User', 'user': user})

# ---------- DELETE USER ----------
@login_required(login_url='registration:login_html')
def user_delete_html(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('registration:users_html')
    
    return render(request, 'user_confirm_delete.html', {'user': user})