from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, CustomAuthenticationForm, MeasurementForm
from .decorators import unauthenticated_user, allowed_users
from .models import User, Measurement, MeasurementStatus
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json



@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuário criado com sucesso!")
            login(request, user)
            return redirect("home")
    else:
        form = CreateUserForm()
    return render(request, "measurements/register.html", {"form": form})


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Login ou senha inválidos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "measurements/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


@login_required
def home(request):
    engenheiro_meds = Measurement.objects.filter(status=MeasurementStatus.IN_PROGRESS)
    gerente_meds = Measurement.objects.filter(status=MeasurementStatus.PENDING_MANAGER)
    diretor_meds = Measurement.objects.filter(status=MeasurementStatus.PENDING_DIRECTOR)
    finished_meds = Measurement.objects.filter(status=MeasurementStatus.FINISHED)

    context = {
        "engenheiro_meds": engenheiro_meds,
        "gerente_meds": gerente_meds,
        "diretor_meds": diretor_meds,
        "finished_meds": finished_meds,
    }
    return render(request, "measurements/home.html", context)


@login_required
def create_measurement(request):
    if request.method == "POST":
        form = MeasurementForm(request.POST, request.FILES)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.created_by = request.user
            measurement.status = MeasurementStatus.IN_PROGRESS
            measurement.save()
            messages.success(request, "Medição criada com sucesso!")
            return redirect("home")
    else:
        form = MeasurementForm()

    return render(request, "measurements/create_measurement.html", {"form": form})

@login_required
def manager(request):
    return render(request, 'measurements/manager.html')


@login_required
@allowed_users(allowed_roles=["Engenheiro"])
def engineer(request):
    return render(request, 'measurements/engineer.html')


@login_required
@allowed_users(allowed_roles=["Gerente"])
def dashboard(request):
    return render(request, 'measurements/dashboard.html')


@login_required
def board(request):
    return render(request, 'measurements/board.html')

@login_required
def view_measurement(request, pk):
    measurement = Measurement.objects.get(pk=pk)
    return render(request, "measurements/view_measurement.html", {"measurement": measurement})

@login_required
def edit_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)

    if request.method == "POST":
        form = MeasurementForm(request.POST, request.FILES, instance=measurement)
        if form.is_valid():
            form.save()
            return redirect("view_measurement", pk=measurement.pk)
    else:
        form = MeasurementForm(instance=measurement)

    return render(request, "measurements/edit_measurement.html", {
        "form": form,
        "measurement": measurement,
    })

@login_required
def delete_measurement(request, pk):
    measurement = Measurement.objects.get(pk=pk)
    if request.method == "POST":
        measurement.delete()
        messages.success(request, "Medição excluída com sucesso!")
        return redirect("home")
    
    return render(request, "measurements/confirm_delete.html", {"measurement": measurement})

@csrf_exempt
def ckeditor_upload(request):
    if request.method == "POST" and request.FILES.get("upload"):
        upload = request.FILES["upload"]
        file_path = default_storage.save(f"uploads/{upload.name}", ContentFile(upload.read()))
        file_url = f"/media/{file_path}"

        return JsonResponse({
            "url": file_url
        })
    return JsonResponse({"error": "Invalid upload request"}, status=400)