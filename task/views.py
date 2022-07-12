from django.shortcuts import render, redirect
from django.utils.text import slugify
import requests
from django.contrib import messages
from django.http import HttpResponse


def add_task(request, id):
    if request.method == 'POST':
        slug = slugify(request.POST['name'])

        isCompleted = False

        try:
            isCompleted = request.POST['isCompleted']
        except:
            isCompleted = False

        response = requests.post(
            'http://127.0.0.1:8000/api/taks/', data={
                'dateDelivery': request.POST['dateDelivery'],
                'description': request.POST['description'],
                'name': request.POST['name'],
                'slug': slug,
                'project': id,
                'priority': request.POST['priority'],
                'isCompleted': isCompleted

            })

        if response.status_code == 201 or response.status_code == 200:
            messages.success(request, 'Proyecto creado correctamente')
            return redirect('project', id=id)
        else:
            messages.error(request, 'Ya se usa el nombre en otro proyecto.')

    print(id)
    return render(request, 'addTask.html')


def completed_task(request, id):
    if request.method == 'POST':
        response = requests.get(f'http://127.0.0.1:8000/api/taks/{id}/')
        task = response.json()

        isCompleted = False

        if task['isCompleted'] == False:
            isCompleted = True
        else:
            isCompleted = False

        if request.method == 'POST':
            response = requests.patch(f'http://127.0.0.1:8000/api/taks/{id}/',
                                      data={
                                          'isCompleted': isCompleted
                                      })

            if response.status_code == 201 or response.status_code == 200:
                messages.success(
                    request, 'Proyecto se ha actualizado correctamente')
                return redirect('project', id=task['project'])
            else:
                messages.error(
                    request, 'Hubo un error al actualizar el proyecto.')
            return redirect('project', id=task['project'])


def delete_task(request, id):
    if request.method == 'POST':
        response = requests.get(f'http://127.0.0.1:8000/api/taks/{id}/')
        task = response.json()
        if task['name']:
            requests.delete(f'http://127.0.0.1:8000/api/taks/{id}/')
            return redirect('project', id=task['project'])
        else:
            messages.error(request, 'Error al eliminar la tarea.')
            return HttpResponse(status=404)


def edit_task(request, id):
    response = requests.get(f'http://127.0.0.1:8000/api/taks/{id}/')
    task = response.json()

    print(task)

    if request.method == 'POST' and task['id']:
        slug = slugify(request.POST['name'])

        isCompleted = False

        try:
            isCompleted = request.POST['isCompleted']
        except:
            isCompleted = False

        if request.method == 'POST':
            response = requests.patch(f'http://127.0.0.1:8000/api/taks/{id}/',
                                      data={
                                          'dateDelivery': request.POST['dateDelivery'],
                                          'description': request.POST['description'],
                                          'name': request.POST['name'],
                                          'slug': slug,
                                          'priority': request.POST['priority'],
                                          'isCompleted': isCompleted
                                      })

            if response.status_code == 201 or response.status_code == 200:
                messages.success(
                    request, 'Proyecto se ha actualizado correctamente')
                return redirect('project', id=task['project'])
            else:
                messages.error(
                    request, 'Hubo un error al actualizar el proyecto.')
                return redirect('project', id=task['project'])
    return render(request, 'editTask.html', {
        'task': task
    })
