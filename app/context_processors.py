
import os
from django.shortcuts import redirect
from app.models import Auth_user
import requests
from django_globals import globals


def extras(request):
    data = None

    print('USER_AUTH: ', str(globals.request))

    access = Auth_user.objects.all().first()
    if(access):

        response = requests.get(' http://127.0.0.1:8000/api/auth/user/', headers={
            'Authorization': 'Bearer ' + access.access_token
        })
        data = response.json()
        if not data['id']:
            if data['code'] == 'token_not_valid':
                Auth_user.delete(user_id=access.user_id)
                return redirect('index_page')
            print(data)

    return {'userAuth': data}
