from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# ==========================================
# PART 1: HTML VIEWS (For your Login Lab)
# ==========================================

def login_view(request):
    # Handle the Login Logic
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # Check credentials against Django Admin/User table
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            # Redirect using 'app_name:url_name'
            return redirect('registration:users_html') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    # Just show the page
    return render(request, 'login.html')

def logout_view(request):
    # Handle Logout
    logout(request)
    return redirect('registration:login_html')

def users_html(request):
    # Protected Page - specific to your URLs
    if not request.user.is_authenticated:
        return redirect('registration:login_html')
    
    # Get users to show in the list
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


# ==========================================
# PART 2: API VIEWS (Matches your URL patterns)
# ==========================================

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'], 
                password=data['password'],
                email=data.get('email', '')
            )
            return JsonResponse({'message': 'User created successfully', 'id': user.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=405)

def list_users(request):
    users = list(User.objects.values('id', 'username', 'email'))
    return JsonResponse(users, safe=False)

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email})