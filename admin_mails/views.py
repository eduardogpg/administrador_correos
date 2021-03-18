from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse

from user_mails.models import UserMail

def index(request):
    return render(request, 'index.html', {})

def footer(request):

    if request.GET.get('token'):
        user_mail = UserMail.objects.filter(token=request.GET['token']).first()

        if user_mail:
            user_mail.update_read()

    with open(settings.IMAGE_DIR / 'legrape2.png', 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')