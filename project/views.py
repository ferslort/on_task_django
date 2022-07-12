import os
from django.shortcuts import render, redirect
import requests
from django.utils.text import slugify
from django.contrib import messages
import time
from django.http import HttpResponse
from app.context_processors import extras


def dashboard_page(request):
    dataUser = extras(request)['userAuth']
    if not dataUser['id']:
        return redirect('index_page')

    response = requests.get('http://127.0.0.1:8000/api/projects/')
    data = response.json()

    projects = []

    for project in data:
        if project['user'] == dataUser['id']:
            projects.append(project)

    return render(request, 'dashboard.html', {
        'projects': projects,
    })


def create_project(request):
    dataUser = extras(request)['userAuth']
    if not dataUser['id']:
        return redirect('index_page')

    if request.method == 'POST':
        slug = slugify(request.POST['name'])
        response = requests.post(
            'http://127.0.0.1:8000/api/projects/', data={
                'dateDelivery': request.POST['dateDelivery'],
                'description': request.POST['description'],
                'name': request.POST['name'],
                'slug': slug,
                'user': int(dataUser['id']),
            })

        if response.status_code == 201 or response.status_code == 200:
            messages.success(request, 'Proyecto creado correctamente')
            return redirect('dashboard_page')
        else:
            messages.error(request, 'Ya se usa el nombre en otro proyecto.')

    return render(request, 'create-project.html')


def project_detail(request, id):
    response = requests.get(f'http://127.0.0.1:8000/api/projects/{id}/')
    project = response.json()
    tasks = []

    return render(request, 'project.html', {
        'project': project,
        'tasks': tasks
    })


def project_edit(request, id):
    response = requests.get(f'http://127.0.0.1:8000/api/projects/{id}/')
    project = response.json()

    if request.method == 'POST':
        slug = slugify(request.POST['name'])
        response = requests.patch(f'http://127.0.0.1:8000/api/projects/{id}/',
                                  data={
                                      'dateDelivery': request.POST['dateDelivery'],
                                      'description': request.POST['description'],
                                      'name': request.POST['name'],
                                      'slug': slug,
                                  })

        if response.status_code == 201 or response.status_code == 200:
            messages.success(
                request, 'Proyecto se ha actualizado correctamente')
            time.sleep(2)
            return redirect('project', id=id)
        else:
            messages.error(request, 'Hubo un error al actualizar el proyecto.')

    return render(request, 'editProject.html', {
        'project': project,
    })


def project_delete(request, id):

    response = requests.get(f'http://127.0.0.1:8000/api/projects/{id}/')
    project = response.json()
    if project['name']:
        requests.delete(f'http://127.0.0.1:8000/api/projects/{id}/')
        return redirect('dashboard_page')
    else:
        messages.error(request, 'Error al eliminar el proyecto.')
        return HttpResponse(status=404)
