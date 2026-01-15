from django.shortcuts import render, redirect
import requests


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


def logout_view(request):
    request.session.flush()#clears access and refresh tokens
    return redirect('/login/')



def product_list(request):
    headers=get_auth_headers(request)
    # if not headers:
    #     return redirect('/login/')
    res=requests.get(f"{API_URL}products/", headers=headers)
    if res.status_code!=200:
        return redirect('/login/')
    products=res.json()
    return render(request,'products.html',{'products':products})

def product_detail(request,product_id):
    headers=get_auth_headers(request)
    # if not headers:
    #     return redirect('/login/')
    res=requests.get(f"{API_URL}products/{product_id}/", headers=headers)
    if res.status_code!=200:
        return redirect('/login/')
    product=res.json()
    return render(request,'product_detail.html',{'product':product})

def my_orders(request):
    headers=get_auth_headers(request)
    # if not headers:
    #     return redirect('/login/')
    res=requests.get(f"{API_URL}orders/", headers=headers)
    if res.status_code!=200:
        return redirect('/login/')
    orders=res.json()
    return render(request,'my_orders.html',{'orders':orders})

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
