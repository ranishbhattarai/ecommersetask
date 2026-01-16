from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.
API_URL="http://127.0.0.1:8000/api/"


def login_view(request):
    if request.method =='POST':
        username=request.POST.get('username', '')
        password=request.POST.get('password', '')
        
        print(f"DEBUG: Login attempt - username: {username}, password: {password}")
        
        if not username or not password:
            return render(request,'login.html',{'error': 'Username and password are required'})
        
        try:
            res=requests.post(f"{API_URL}token/",data={'username':username,'password':password})
            print(f"DEBUG: API Response Status: {res.status_code}")
            print(f"DEBUG: API Response: {res.text}")
            
            if res.status_code==200:
                token=res.json()
                request.session['access']=token['access']
                request.session['refresh']=token['refresh']
                request.session['username']=username
                
                # Try to get user role from the API
                headers = {'Authorization': f'Bearer {token["access"]}'}
                print(f"DEBUG: Headers being used: {headers}")
                try:
                    user_res = requests.get(f"{API_URL}user-profile/", headers=headers)
                    print(f"DEBUG: User profile response status: {user_res.status_code}")
                    print(f"DEBUG: User profile response text: {user_res.text}")
                    if user_res.status_code == 200:
                        user_data = user_res.json()
                        print(f"DEBUG: User profile data: {user_data}")
                        role = user_data.get('role', 'customer')
                        request.session['role'] = role
                        print(f"DEBUG: User role from API: {role}")
                    else:
                        print(f"DEBUG: User profile API returned error status {user_res.status_code}")
                        request.session['role'] = 'customer'  # default
                except Exception as e:
                    print(f"DEBUG: Could not fetch user profile: {e}")
                    import traceback
                    traceback.print_exc()
                    request.session['role'] = 'customer'  # default
                
                # Save session explicitly
                request.session.modified = True
                print(f"DEBUG: Session saved with role: {request.session.get('role')}")
                print(f"DEBUG: Login successful, redirecting to /")
                return redirect('/')
            else:
                error_message = res.json().get('detail', 'Invalid credentials')
                return render(request,'login.html',{'error':error_message})
        except Exception as e:
            error_message = f'Login failed: {str(e)}'
            print(f"DEBUG: Exception: {error_message}")
            return render(request,'login.html',{'error':error_message})
        
    return render(request,'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        if not username or not password:
            return render(request, 'register.html', {'error': 'Username and password are required'})
        
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        try:
            res = requests.post(f"{API_URL}register/", data={
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'password2': password2
            })
            
            if res.status_code == 201:
                return render(request, 'register.html', {
                    'success': 'Registration successful! Please login.'
                })
            else:
                error_data = res.json()
                error_message = error_data.get('error', 'Registration failed')
                return render(request, 'register.html', {'error': error_message})
        except Exception as e:
            return render(request, 'register.html', {'error': f'Registration failed: {str(e)}'})
    
    return render(request, 'register.html')


def logout_view(request):
    request.session.flush()#clears access and refresh tokens
    return redirect('/login/')

def debug_session(request):
    """Debug view to see what's in the session"""
    return render(request, 'debug.html', {
        'session_data': dict(request.session),
        'role': request.session.get('role'),
        'username': request.session.get('username'),
        'access': 'Present' if request.session.get('access') else 'Not Present',
    })



def product_list(request):
    headers=get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    res=requests.get(f"{API_URL}products/", headers=headers)
    
    # If unauthorized, try to refresh token
    if res.status_code == 401:
        headers = refresh_token_and_retry(request)
        if headers:
            res = requests.get(f"{API_URL}products/", headers=headers)
        else:
            return redirect('/login/')
    
    if res.status_code == 200:
        products = res.json()
        return render(request, 'products.html', {'products': products})
    else:
        return redirect('/login/')

def product_detail(request,product_id):
    headers=get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    res=requests.get(f"{API_URL}products/{product_id}/", headers=headers)
    
    # If unauthorized, try to refresh token
    if res.status_code == 401:
        headers = refresh_token_and_retry(request)
        if headers:
            res = requests.get(f"{API_URL}products/{product_id}/", headers=headers)
        else:
            return redirect('/login/')
    
    if res.status_code == 200:
        product = res.json()
        return render(request, 'product_detail.html', {'product': product})
    else:
        return redirect('/login/')

def my_orders(request):
    headers=get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    res=requests.get(f"{API_URL}orders/", headers=headers)
    
    # If unauthorized, try to refresh token
    if res.status_code == 401:
        headers = refresh_token_and_retry(request)
        if headers:
            res = requests.get(f"{API_URL}orders/", headers=headers)
        else:
            return redirect('/login/')
    
    if res.status_code == 200:
        orders = res.json()
        return render(request, 'orders.html', {'orders': orders})
    else:
        return redirect('/login/')

def refresh_token_and_retry(request):
    """Try to refresh the access token using refresh token"""
    refresh = request.session.get('refresh')
    if not refresh:
        return None
    
    refresh_response = requests.post(f"{API_URL}token/refresh/", data={'refresh': refresh})
    if refresh_response.status_code == 200:
        access = refresh_response.json().get('access')
        request.session['access'] = access
        return {'Authorization': f'Bearer {access}'}
    else:
        request.session.flush()
        return None

def get_auth_headers(request):
    access=request.session.get('access')
    refresh=request.session.get('refresh')
    if not access and not refresh:
        return {}
    #try access token first
    if not access and refresh:
        refresh_response=requests.post(f"{API_URL}token/refresh/",data={'refresh':refresh})
        if refresh_response.status_code==200:
            access=refresh_response.json().get('access')
            request.session['access']=access
        else:
            request.session.flush()
            return {}
    return {'Authorization':f'Bearer {access}'}

def get_user_role(request):
    """Get the user's role from session"""
    role = request.session.get('role')
    print(f"DEBUG: get_user_role - role from session: {role}")
    return role

def admin_dashboard(request):
    headers = get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    # Check if user is admin
    user_role = get_user_role(request)
    print(f"DEBUG: admin_dashboard - user_role: {user_role}")
    
    if not user_role:
        return redirect('/login/')
    
    if user_role != 'admin':
        return render(request, 'error.html', {
            'error': 'Access Denied',
            'message': 'You do not have permission to access the admin dashboard. Only administrators can access this page.'
        })
    
    # Get products count
    products_res = requests.get(f"{API_URL}products/", headers=headers)
    if products_res.status_code == 200:
        products_data = products_res.json()
        # Handle paginated response
        if isinstance(products_data, dict) and 'results' in products_data:
            products_count = products_data.get('count', len(products_data['results']))
        else:
            products_count = len(products_data) if isinstance(products_data, list) else 0
    else:
        products_count = 0
    
    # Get orders count
    orders_res = requests.get(f"{API_URL}orders/", headers=headers)
    if orders_res.status_code == 200:
        orders_data = orders_res.json()
        # Handle paginated response
        if isinstance(orders_data, dict) and 'results' in orders_data:
            orders = orders_data['results']
            orders_count = orders_data.get('count', len(orders))
        else:
            orders = orders_data if isinstance(orders_data, list) else []
            orders_count = len(orders)
    else:
        orders = []
        orders_count = 0
    
    # Get deliveries count
    deliveries_res = requests.get(f"{API_URL}deliveries/", headers=headers)
    if deliveries_res.status_code == 200:
        deliveries_data = deliveries_res.json()
        # Handle paginated response
        if isinstance(deliveries_data, dict) and 'results' in deliveries_data:
            deliveries = deliveries_data['results']
            deliveries_count = deliveries_data.get('count', len(deliveries))
        else:
            deliveries = deliveries_data if isinstance(deliveries_data, list) else []
            deliveries_count = len(deliveries)
    else:
        deliveries = []
        deliveries_count = 0
    
    context = {
        'products_count': products_count,
        'orders_count': orders_count,
        'deliveries_count': deliveries_count,
        'orders': orders[:5],  # Show last 5 orders
        'deliveries': deliveries[:5],  # Show last 5 deliveries
    }
    return render(request, 'admin_dashboard.html', context)

def supplier_dashboard(request):
    headers = get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    # Check if user is supplier
    user_role = get_user_role(request)
    print(f"DEBUG: supplier_dashboard - user_role: {user_role}")
    
    if not user_role:
        return redirect('/login/')
    
    if user_role != 'supplier':
        return render(request, 'error.html', {
            'error': 'Access Denied',
            'message': 'You do not have permission to access the supplier dashboard. Only suppliers can access this page.'
        })
    
    # Get supplier's products
    products_res = requests.get(f"{API_URL}products/", headers=headers)
    if products_res.status_code == 200:
        products_data = products_res.json()
        # Handle paginated response
        if isinstance(products_data, dict) and 'results' in products_data:
            products = products_data['results']
        else:
            products = products_data if isinstance(products_data, list) else []
    else:
        products = []
    
    # Calculate inventory stats
    total_products = len(products)
    low_stock_products = [p for p in products if p.get('stock', 0) < 10]
    out_of_stock_products = [p for p in products if p.get('stock', 0) == 0]
    
    context = {
        'total_products': total_products,
        'low_stock_count': len(low_stock_products),
        'out_of_stock_count': len(out_of_stock_products),
        'products': products,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'supplier_dashboard.html', context)

def delivery_dashboard(request):
    headers = get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    # Check if user is delivery person
    user_role = get_user_role(request)
    print(f"DEBUG: delivery_dashboard - user_role: {user_role}")
    
    if not user_role:
        return redirect('/login/')
    
    if user_role not in ['delivery', 'delivery_person']:
        return render(request, 'error.html', {
            'error': 'Access Denied',
            'message': 'You do not have permission to access the delivery dashboard. Only delivery personnel can access this page.'
        })
    
    # Get delivery person's assignments
    deliveries_res = requests.get(f"{API_URL}deliveries/", headers=headers)
    if deliveries_res.status_code == 200:
        deliveries_data = deliveries_res.json()
        # Handle paginated response
        if isinstance(deliveries_data, dict) and 'results' in deliveries_data:
            deliveries = deliveries_data['results']
        else:
            deliveries = deliveries_data if isinstance(deliveries_data, list) else []
    else:
        deliveries = []
    
    # Group by status
    assigned = [d for d in deliveries if d.get('status') == 'assigned']
    picked = [d for d in deliveries if d.get('status') == 'picked']
    on_way = [d for d in deliveries if d.get('status') == 'on_way']
    delivered = [d for d in deliveries if d.get('status') == 'delivered']
    
    context = {
        'total_deliveries': len(deliveries),
        'assigned_count': len(assigned),
        'picked_count': len(picked),
        'on_way_count': len(on_way),
        'delivered_count': len(delivered),
        'deliveries': deliveries,
        'pending_deliveries': assigned + picked + on_way,
    }
    return render(request, 'delivery_dashboard.html', context)

def dashboard(request):
    """Main dashboard that redirects based on user role"""
    headers = get_auth_headers(request)
    if not headers:
        return redirect('/login/')
    
    # Get user info from session or make an API call
    # For now, redirect to products page as default
    return redirect('/')
