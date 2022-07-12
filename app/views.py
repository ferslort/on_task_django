import os
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
import jwt
from app.models import Auth_user
from app.context_processors import extras
from django_globals import globals


def index_page(request):

    if request.method == 'POST':
        response = requests.post(
            'http://127.0.0.1:8000/api/auth/login/', data={
                'email': request.POST['email'],
                'password': request.POST['password'],
            })
        data = response.json()

        try:
            user_info = jwt.decode(
                data['access'], 'django-insecure-y(%4-7j8$a@ac#by^x=wtzkv&&qw5mwtx!@^)sl$t4@s1s4jm%', algorithms=['HS256'])
            idUser = user_info['user_id']

            os.environ['USER_AUTH'] = int(idUser)

            globals.set('USER_AUTH', int(idUser))

            Auth_user(access_token=data['access'], user_id=idUser).save()

        except:
            messages.success(request, 'Email o contraseña incorrectos')

        if response.status_code == 201 or response.status_code == 200:
            messages.success(request, 'Te has registrado correctamente')
            return redirect('dashboard_page')

    return render(request, 'index.html')


def register_page(request):

    if request.method == 'POST':

        response = requests.post(
            'http://127.0.0.1:8000/api/register/', data={
                'email': request.POST['email'],
                'password': request.POST['password'],
                'username': request.POST['username'],
            })
        if response.status_code == 201 or response.status_code == 200:
            messages.success(request, 'Te has registrado correctamente')
            return redirect('index_page')
        else:
            messages.warning(
                request, 'El email o usuario ya se encuentra en uso.')

    return render(request, 'register.html')


def logout_page(request):
    userAuth = extras(request)['userAuth']
    user = Auth_user.objects.filter(user_id=userAuth['id'])
    user.delete()

    return redirect('index_page')
