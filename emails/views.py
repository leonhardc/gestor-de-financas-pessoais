from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

def send_email(request):
    send_mail(
        'Assunto do Email',
        'Corpo do email',
        'backup.leonardo.001@gmail.com',
        ['costa.leonardorodrigues@gmail.com'],
    )
    # return render(request, 'emails/send_email.html')
    return HttpResponse('Email enviado com sucesso!')
