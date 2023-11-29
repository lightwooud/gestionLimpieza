from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, ActividadForm, CuadrillaForm, EmpleadoCuadrillaForm
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse
from .models import EmpleadoCuadrilla, Actividad, Cuadrilla, Colonia, Usuario
from django.http import HttpResponseForbidden

def index(request):
    template = loader.get_template("components/home.html")
    return HttpResponse(template.render({}, request))


def lista_actividades(request):
    actividades = Actividad.objects.all() 
    return render(request, 'actividades/lista_actividades.html', {'actividades': actividades})

def lista_cuadrillas(request):
    cuadrillas = Cuadrilla.objects.all().prefetch_related('empleados')
    return render(request, 'cuadrillas/lista_cuadrillas.html', {'cuadrillas': cuadrillas})
  

@login_required

def actividad(request):
    if not request.user.is_authenticated or request.user.rol not in['ADMINISTRADOR', 'JEFE DE CUADRILLA']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    elif request.method == 'POST':
            form = ActividadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
    else:
        form = ActividadForm()
    return render(request, 'actividades/actividad.html', {'form': form})

def cuadrilla(request):
    if not request.user.is_authenticated or request.user.rol not in['ADMINISTRADOR', 'JEFE DE CUADRILLA']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    elif request.method == 'POST':
            cuadrilla_form = CuadrillaForm(request.POST)
            if cuadrilla_form.is_valid():
                cuadrilla = cuadrilla_form.save()
                empleados = cuadrilla_form.cleaned_data.get('empleados')
                
                for empleado in empleados:
                    EmpleadoCuadrilla.objects.create(cuadrilla=cuadrilla, empleado=empleado)

                return redirect('home')
    else:
        cuadrilla_form = CuadrillaForm()

    context = {
        'cuadrilla_form': cuadrilla_form,
    }
    return render(request, 'cuadrillas/cuadrilla.html', context)



def editar_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect('lista_actividades')
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'actividades/editar_actividades.html', {'form': form})

def editar_cuadrilla(request, id):
    cuadrilla = get_object_or_404(Cuadrilla, id=id)
    if request.method == 'POST':
        form = CuadrillaForm(request.POST, instance=cuadrilla)
        if form.is_valid():
            form.save()
            return redirect('lista_cuadrillas')
    else:
        form = CuadrillaForm(instance=cuadrilla)
    return render(request, 'cuadrillas/editar_cuadrillas.html', {'form': form})


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form
    return render(request, 'registration/register.html', data)
