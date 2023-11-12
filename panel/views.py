from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseServerError

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import *

import logging

# Obtiene un logger para tu aplicación
logger = logging.getLogger(__name__)


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, 'Username and password did not match')
            return redirect('signin')
        else:
            login(request, user)
            return redirect("home")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] != request.POST["password2"]:
            messages.error(request, 'Passwords did not match')
            return redirect('signup')
        elif request.POST["username"] == "" or request.POST["password1"] == "" or request.POST["password2"] == "":
            messages.error(request, 'Please fill all the fields')
            return redirect('signup')
        try:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"]
            )
            user.save()
            login(request, user)
            return redirect("signin")
        except IntegrityError:
            messages.error(request, 'Username already exists')
            return redirect('signup')


def signout(request):
    logout(request)
    return redirect("signin")


@login_required
def index(request):
    try:
        nombre_usuario = request.user.username
        return render(request, "home.html", {'nombre_usuario': nombre_usuario})
    except Exception as e:
        logger.error(f"Error en la vista home: {e}")
        return HttpResponseServerError("Error interno del servidor")


@login_required
def users(request):
    nombre_usuario = request.user.username
    return render(request, "users.html", {'nombre_usuario': nombre_usuario})


@login_required
def persons(request):
    nombre_usuario = request.user.username
    personas_list = Persona.objects.filter(user=request.user)
    personas_por_pagina = 10
    paginator = Paginator(personas_list, personas_por_pagina)
    page = request.GET.get('page', 1)

    try:
        personas = paginator.page(page)
    except PageNotAnInteger:
        personas = paginator.page(1)
    except EmptyPage:
        personas = paginator.page(paginator.num_pages)

    if request.method == "GET":
        return render(request, "persons.html", {'nombre_usuario': nombre_usuario, 'form': PersonForm(), 'personas': personas})

    elif request.method == "POST":
        try:
            form = PersonForm(request.POST)
            if form.is_valid():
                nueva_persona = form.save(commit=False)
                nueva_persona.user = request.user
                nueva_persona.save()
                messages.success(request, 'Persona agregada exitosamente.')
                return redirect('persons')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo {
                                       field}: {error}')
                return render(request, "persons.html", {'nombre_usuario': nombre_usuario, 'form': form, 'personas': personas})
        except Exception as e:
            messages.error(request, f'Error al agregar la persona: {e}')
            return redirect('persons')


@login_required
def update_person(request, persona_dni):
    persona = get_object_or_404(Persona, dni=persona_dni, user=request.user)

    if request.method == "GET":
        form = PersonForm(instance=persona)
        return render(request, "update_person.html", {'form': form, 'persona': persona})

    elif request.method == "POST":
        form = PersonForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Persona actualizada exitosamente.')
            return redirect('persons')
        else:
            messages.error(
                request, 'Error al actualizar la persona. Por favor, verifica los datos.')
            return render(request, "update_person.html", {'form': form, 'persona': persona})


@login_required
def delete_person(request, persona_dni):
    try:
        persona = Persona.objects.get(dni=persona_dni, user=request.user)
        persona.delete()
        messages.success(request, 'Persona eliminada exitosamente.')
    except Persona.DoesNotExist:
        messages.error(
            request, 'La persona que intentas eliminar no existe o no tienes permisos.')
    return redirect('persons')
