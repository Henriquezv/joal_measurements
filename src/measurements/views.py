import os
import re
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
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.contrib.sites.models import Site
from django.db.models import Sum


from .forms import MeasurementForm, MeasurementMessageForm
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
    return render(request, "measurements/pages/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        return redirect('home')
    elif user.groups.filter(name='Manager').exists():
        return redirect('home')
    elif user.groups.filter(name='Engineer').exists():
        return redirect('home')
    elif user.groups.filter(name='EngineerAssistant').exists():
        return redirect('home')
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
    return render(request, "measurements/pages/home.html", context)

@login_required
@group_required(['Manager', 'Director'])
def dashboard(request):
    data_pagamento = (
        Measurement.objects
        .exclude(payment_date__isnull=True)
        .values('payment_date')
        .annotate(total=Sum('final_value'))
        .order_by('payment_date')
    )
    return render(request, 'measurements/pages/dashboard.html', {'data_pagamento': data_pagamento})

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

    return render(request, "measurements/pages/create_measurement.html", {"form": form})



@login_required
@group_required(['Engineer', 'EngineerAssistant'])
def engineer(request):
    return render(request, 'measurements/pages/engineer.html')


@login_required
@group_required(['Manager', 'Director'])
def manager(request):
    return render(request, 'measurements/pages/dashboard.html')


@login_required
def view_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    messages_list = measurement.messages.all()
    form = MeasurementMessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        msg = form.save(commit=False)
        msg.user = request.user
        msg.measurement = measurement
        msg.save()
        return redirect("view_measurement", pk=measurement.pk)

    # Determina o grupo do usuário logado
    user_groups = request.user.groups.values_list("name", flat=True)

    # Define permissões para botões de aprovação/reprovação
    can_approve = can_reject = False
    next_status = None

    can_delete_comments = "Manager" in user_groups or "Director" in user_groups

    # Engenheiro — só aprova o primeiro passo
    if measurement.status == MeasurementStatus.IN_PROGRESS and "Engineer" in user_groups:
        can_approve = True
        next_status = MeasurementStatus.PENDING_MANAGER

    # Gerente — pode aprovar medições em progresso (engenheiro) ou pendentes de gerente
    elif ("Manager" in user_groups) and measurement.status in [
        MeasurementStatus.IN_PROGRESS,
        MeasurementStatus.PENDING_MANAGER,
    ]:
        can_approve = can_reject = True
        next_status = (
            MeasurementStatus.PENDING_DIRECTOR
            if measurement.status == MeasurementStatus.PENDING_MANAGER
            else MeasurementStatus.PENDING_DIRECTOR
        )

    # Diretor — pode aprovar qualquer estágio anterior
    elif ("Director" in user_groups) and measurement.status in [
        MeasurementStatus.IN_PROGRESS,
        MeasurementStatus.PENDING_MANAGER,
        MeasurementStatus.PENDING_DIRECTOR,
    ]:
        can_approve = can_reject = True
        next_status = (
            MeasurementStatus.FINISHED
            if measurement.status == MeasurementStatus.PENDING_DIRECTOR
            else MeasurementStatus.FINISHED
        )

    context = {
        "measurement": measurement,
        "messages_list": messages_list,
        "form": form,
        "can_approve": can_approve,
        "can_reject": can_reject,
        "next_status": next_status,
        "can_delete_comments": can_delete_comments,
    }
    return render(request, "measurements/pages/view_measurement.html", context)

@login_required
def approve_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    user_groups = request.user.groups.values_list("name", flat=True)

    # Engenheiro só envia para o gerente
    if measurement.status == MeasurementStatus.IN_PROGRESS and "Engineer" in user_groups:
        measurement.status = MeasurementStatus.PENDING_MANAGER

    # Gerente pode aprovar qualquer coisa até o diretor
    elif "Manager" in user_groups:
        if measurement.status == MeasurementStatus.IN_PROGRESS:
            measurement.status = MeasurementStatus.PENDING_DIRECTOR
        elif measurement.status == MeasurementStatus.PENDING_MANAGER:
            measurement.status = MeasurementStatus.PENDING_DIRECTOR
        elif measurement.status == MeasurementStatus.PENDING_DIRECTOR:
            measurement.status = MeasurementStatus.FINISHED

    # Diretor pode aprovar tudo direto para "Finalizado"
    elif "Director" in user_groups:
        measurement.status = MeasurementStatus.FINISHED

    else:
        messages.error(request, "Você não tem permissão para aprovar esta medição.")
        return redirect("view_measurement", pk=pk)

    measurement.save()
    messages.success(request, "Medição aprovada com sucesso!")
    return redirect("view_measurement", pk=pk)


@login_required
def reject_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    user_groups = request.user.groups.values_list("name", flat=True)

    if ((measurement.status == MeasurementStatus.PENDING_MANAGER and "Manager" in user_groups)
        or (measurement.status == MeasurementStatus.PENDING_DIRECTOR and "Director" in user_groups)):
        measurement.status = MeasurementStatus.IN_PROGRESS
        measurement.save()
        messages.warning(request, "Medição rejeitada e devolvida ao engenheiro.")
    else:
        messages.error(request, "Você não tem permissão para rejeitar esta medição.")

    return redirect("view_measurement", pk=pk)

@login_required
def edit_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)

    # nome amigável do anexo
    attachment_filename = os.path.basename(measurement.attachment.name) if measurement.attachment else None

    if request.method == 'POST':
        if 'remove_attachment' in request.POST:
            if measurement.attachment:
                measurement.attachment.delete(save=False)
                measurement.attachment = None
                measurement.save()
                messages.success(request, "Anexo removido com sucesso.")
            return redirect('edit_measurement', pk=pk)

        form = MeasurementForm(request.POST, request.FILES, instance=measurement)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.payment_date = form.cleaned_data.get("payment_date") or measurement.payment_date
            updated.save()
            messages.success(request, "Medição atualizada com sucesso.")
            return redirect('view_measurement', pk=measurement.pk)
        else:
            messages.error(request, "Erros no formulário. Verifique os campos.")
    else:
        # carrega a data existente no formulário
        form = MeasurementForm(instance=measurement)

    return render(request, 'measurements/pages/edit_measurement.html', {
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
    
    return render(request, "measurements/pages/confirm_delete.html", {"measurement": measurement})


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

def get_absolute_content(content):
    """
    Substitui todos os src relativos de imagens (/media/...) por URLs absolutas.
    """
    domain = getattr(settings, 'DOMAIN_NAME', '127.0.0.1:8000')
    pattern = r'src=(["\'])/media/(.*?)\1'  # pega src="/media/..." ou src='/media/...'
    
    return re.sub(pattern, f'src="http://{domain}/media/\\2"', content)


@login_required
def generate_email(request, measurement_id):
    measurement = get_object_or_404(Measurement, id=measurement_id)

    subject = f"Medição {measurement.id} - {measurement.created_by.get_full_name()}"
    recipient = [request.user.email]

    html_content = render_to_string('measurements/pages/email_measurement.html', {
        'measurement': measurement,
    })

    # Detecta imagens no HTML
    img_pattern = r'src="(/media/[^"]+)"'
    images = re.findall(img_pattern, html_content)

    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient,
    )
    email.content_subtype = 'html'

    # Substitui src por cid e adiciona como anexos inline
    for i, img_url in enumerate(images):
        # Caminho físico da imagem
        img_path = os.path.join(settings.MEDIA_ROOT, img_url.replace('/media/', '', 1))
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_data = f.read()
            mime_img = MIMEImage(img_data)
            cid = f'image{i}'
            mime_img.add_header('Content-ID', f'<{cid}>')
            mime_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
            email.attach(mime_img)
            # Substitui src no HTML
            html_content = html_content.replace(img_url, f'cid:{cid}')

    # Atualiza o corpo do e-mail com srcs cid
    email.body = html_content

    # Anexos da medição (PDFs, etc.)
    if measurement.attachment:
        email.attach_file(measurement.attachment.path)

    email.send()
    messages.success(request, f"E-mail enviado com sucesso para {request.user.email}!")

    return redirect('view_measurement', pk=measurement.id)

@login_required
def delete_message(request, pk):
    from .models import MeasurementMessage

    message_obj = get_object_or_404(MeasurementMessage, pk=pk)
    measurement = message_obj.measurement

    if not (
        request.user.groups.filter(name="Manager").exists() or
        request.user.groups.filter(name="Director").exists()
    ):
        messages.error(request, "Você não tem permissão para excluir mensagens.")
        return redirect("view_measurement", pk=measurement.pk)

    message_obj.delete()
    messages.success(request, "Comentário excluído com sucesso.")
    return redirect("view_measurement", pk=measurement.pk)

