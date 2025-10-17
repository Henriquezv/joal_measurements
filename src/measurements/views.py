import os
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import MeasurementForm
from .decorators import group_required
from .models import Measurement, MeasurementStatus


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("redirect_after_login")
        else:
            messages.error(request, "Login ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, "measurements/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        return redirect('manager')
    elif user.groups.filter(name='Manager').exists():
        return redirect('manager')
    elif user.groups.filter(name='Engineer').exists():
        return redirect('engineer')
    elif user.groups.filter(name='EngineerAssistant').exists():
        return redirect('engineer')
    else:
        return redirect('home')


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
            measurement.start_date = date.today()  # define automaticamente a data inicial
            measurement.save()
            messages.success(request, "Medição criada com sucesso!")
            return redirect("home")
    else:
        form = MeasurementForm()

    return render(request, "measurements/create_measurement.html", {"form": form})



@login_required
@group_required(['Engineer', 'EngineerAssistant'])
def engineer(request):
    return render(request, 'measurements/engineer.html')


@login_required
@group_required(['Manager', 'Director'])
def manager(request):
    return render(request, 'measurements/dashboard.html')


@login_required
def board(request):
    return render(request, 'measurements/board.html')


@login_required
def view_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    from .forms import MeasurementMessageForm

    # Trata envio de nova mensagem
    if request.method == "POST":
        form = MeasurementMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.measurement = measurement
            msg.user = request.user
            msg.save()
            return redirect("view_measurement", pk=pk)
    else:
        form = MeasurementMessageForm()

    messages_list = measurement.messages.select_related("user").all()

    context = {
        "measurement": measurement,
        "form": form,
        "messages_list": messages_list,
    }
    return render(request, "measurements/view_measurement.html", context)


@login_required
def edit_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)

    # calcula nome amigável do anexo (basename)
    attachment_filename = None
    if measurement.attachment:
        attachment_filename = os.path.basename(measurement.attachment.name)

    if request.method == 'POST':
        # botão "Remover anexo" -> trata e volta para a mesma página de edição
        if 'remove_attachment' in request.POST:
            if measurement.attachment:
                measurement.attachment.delete(save=False)
                measurement.attachment = None
                measurement.save()
                messages.success(request, "Anexo removido com sucesso.")
            return redirect('edit_measurement', pk=pk)

        # submeter edição (inclui arquivos)
        form = MeasurementForm(request.POST, request.FILES, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, "Medição atualizada com sucesso.")
            return redirect('view_measurement', pk=measurement.pk)
        else:
            # se invalid, recalcula nome do anexo para exibir novamente
            if measurement.attachment:
                attachment_filename = os.path.basename(measurement.attachment.name)
            messages.error(request, "Erros no formulário. Verifique os campos.")
    else:
        form = MeasurementForm(instance=measurement)

    return render(request, 'measurements/edit_measurement.html', {
        'form': form,
        'measurement': measurement,
        'attachment_filename': attachment_filename,
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
