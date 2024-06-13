from django.shortcuts import redirect, render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import root_config 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request):
    data = {
        "message":f"Hello {request.user.first_name}, welcome to your user area"
    }
    return Response(data)


def Signup(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        re_password=request.POST.get('re_password')

        data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'password': password,
        're_password': re_password
        }

        url = f"http://{root_config.config['root_ip_host']}:8000/api/auth/users/"

        response = requests.post(url, json=data)

        # Check the response status code
        if response.status_code == 201:
            print("User created successfully")
            return redirect('login')
        else:
            print("Failed to create user")
            return render(request,'Signup.html')

    return render(request,'Signup.html')


def login(request):
    if request.method == 'POST':

        email=request.POST.get('email')
        password=request.POST.get('password')

        data = {
        'email': email,
        'password': password,
        }

        url = f"http://{root_config.config['root_ip_host']}:8000/api/auth/jwt/create/"
        response = requests.post(url, json=data)

        # Check the response status code
        if response.status_code == 200:
            
            response_json = response.json()
            jwt_token = response_json['access']
            refresh_token = response_json['refresh']
            print("Token obtained:", jwt_token)
            print("Refresh Token:", refresh_token)
            return redirect('about')
        else:
            print("Failed login")
            return redirect('login')
    return render(request,'login.html')