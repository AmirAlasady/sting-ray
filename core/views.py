import json
from django.shortcuts import redirect, render
import requests
from django.urls import reverse
from ai_api.models import *

# config whre to run the head of the system 'frontend'
host='127.0.0.1' # or depolyment domain
# Create your views here.
def get_token():
    url = f"http://{host}:8000/api/auth/jwt/create/"
    data = {
        'email': 'gtavidk12343@gmail.com',
        'password': '12345abce'
    }
    response = requests.post(url, json=data)
    response_dict = json.loads(response.text)
    print("Token obtained:", response_dict.get('access'))
    return response_dict.get('access')

def get_auth_header():
    token = get_token()
    return {'Authorization': f'Bearer {token}'}

def about(request):
    get_auth_header()
    return render(request,'about.html')

def showconvs(request):
    headers=get_auth_header() 
    url = f"http://{host}:8000/ai_api/conversations"
    if request.method=="POST":
        title=request.POST['title']
        #print(title)
        url2=f"http://{host}:8000/ai_api/conversations/create"
        data = {'title': title}  # Key-value pair with title as data
        response = requests.post(url2, headers=headers, data=data)
        if response.status_code == 200:  
            print('secess')
        else:
            # Handle error (e.g., display error message)
            print(f"Error creating conversation: {response.text}")
        return redirect('showconvs')
    
    response = requests.get(url,headers=headers)
    data = response.json()  # Convert response to JSON data
    context = {'conversations': data}  # Create a context dictionary with the conversations
    return render(request, 'showconvs.html', context=context)

def deleate(request,pk):
    headers=get_auth_header() 
    url = f"http://{host}:8000/ai_api/conversations/"
    url += str(pk)
    response = requests.delete(url,headers=headers)
    if response.status_code == 200:  
        print('secessfully deleated')
        return redirect('showconvs')
    else:
        # Handle error (e.g., display error message)
        print(f"Error deleating conversation: {response.text}")
        return redirect('showconvs')
    

def details(request,pk):
    headers=get_auth_header() 
    url = f"http://{host}:8000/ai_api/conversations/"
    url += str(pk)
    files_url=f'http://{host}:8000/ai_api/files/show/'
    files_url += str(pk)
    response = requests.get(url,headers=headers)
    file_response = requests.get(files_url,headers=headers)
    data = response.json()  # Convert response to JSON data
    files_data = file_response.json()
    context = {'chat': data, "pk":pk, "files_data":files_data}
    return render(request,'details.html',context)


def upload_file(request,pk):
    if request.method=="POST":
        headers=get_auth_header() 
        url=f'http://{host}:8000/ai_api/files/upload/'
        url += str(pk)
        file = request.FILES['file']
        if file:
            print(file)
            print('--------------')
        data = {'file':file}

        response = requests.post(url,headers=headers,files=data)
        if response.status_code == 200:  
            print('secess')
        else:
            # Handle error (e.g., display error message)
            print(f"Error uploading file : {response.text}")
        return redirect('details',pk)
    
def deleate_file(request,pk,id):
    headers=get_auth_header() 
    url=f'http://{host}:8000/ai_api/files/remove/{str(pk)}/{str(id)}'
    response = requests.delete(url,headers=headers)
    if response.status_code == 200:  
        print('deleated! ')
    else:
        # Handle error (e.g., display error message)
        print(f"Error removing file : {response.text}")
    return redirect('details',pk)

def ask(request,pk):
    if request.method=="POST":
        headers=get_auth_header()
        query=request.POST['query']
        option = request.POST.get('option')
        system = request.POST.get('system', '')
        #print(title)
        url = f"http://{host}:8000/ai_api/conversations/"
        url += str(pk)
        data = {
                'query': query,
                'option':option,
                'system':system
                }  # Key-value pair with title as data
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 201:  
            print('secess')
        else:
            # Handle error (e.g., display error message)
            print(f"Error creating conversation: {response.text}")
        return redirect('details',pk)

def update(request,pk):
    headers=get_auth_header()
    url = f"http://{host}:8000/ai_api/conversations/update/"
    url += str(pk)
    title=request.GET['new_title']
    data = {"title":title} 
    response = requests.put(url, headers=headers, data=data)
    if response.status_code == 200:  
        print('secess')
    else:
        # Handle error (e.g., display error message)
        print(f"Error creating conversation: {response.text}")
    return redirect('showconvs')