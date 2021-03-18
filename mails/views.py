from django.utils import timezone

from django.conf import settings

from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.urls import reverse_lazy

from django.template.loader import get_template

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from django.core.mail import EmailMultiAlternatives

from django.views.generic.detail import DetailView

from .models import Mail
from users.models import User
from user_mails.models import UserMail

from django.contrib.sites.shortcuts import get_current_site

from .forms import CreateMailForm

class MailListView(ListView):
    model = Mail
    template_name = 'mails/list.html'
    paginate_by = 10

class MailCreateView(CreateView):
    model = Mail
    template_name = 'mails/create.html'
    form_class = CreateMailForm

    def get_success_url(self):
        return reverse('mails:list')

class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mails:list')

class MailUpdateView(UpdateView):
    model = Mail
    form_class = CreateMailForm
    template_name = 'mails/update.html'

    def get_success_url(self):
        return reverse('mails:list')

class MailDetailView(DetailView):
    model = Mail
    template_name = 'mails/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  

def create_mail(subject, user, template_path='', context={}):
    template = get_template(template_path)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject,
        'PyWombat',
        settings.EMAIL_HOST_USER,
        [user.email]
    )

    message.attach_alternative(content, 'text/html')
    return message

def send_async():
    pass

def send(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    token_generator = PasswordResetTokenGenerator()

    url = reverse('footer')
    domain = get_current_site(request)

    for user in User.objects.exclude(usermail__mail=mail).filter(newsletter=True):
        
        token = token_generator.make_token(user)
        user_mail = UserMail.objects.create(user=user, mail=mail, token=token)

        context = { 'mail':mail, 
                    'user':user, 
                    'token': token, 
                    'domain': domain.domain, 
                    'url': url }
        
        email = create_mail(mail.subject, user, 'mails/base/base.html', context)
        email.send(fail_silently=False)

        user_mail.mail_sent_at = timezone.now()
        user_mail.save()

    return redirect('mails:detail', mail.id)

def admin(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    
    context = { 'mail': mail}
    
    context['users'] = UserMail.objects.filter(mail=mail).count()
    context['read_count'] = UserMail.objects.filter(mail=mail).filter(read=True).count()

    user_mail = UserMail.objects.filter(mail=mail).last()
    if user_mail:
        context['last_send_at'] = user_mail.sent_at

    context['user_mails'] = UserMail.objects.filter(mail=mail)

    return render(request, 'mails/admin.html', context)