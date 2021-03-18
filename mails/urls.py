from django.urls import path

from .views import send
from .views import admin

from .views import MailListView
from .views import MailCreateView
from .views import MailDeleteView
from .views import MailUpdateView
from .views import MailDetailView

app_name = 'mails'

urlpatterns = [
    path('', MailListView.as_view(), name='list'),
    path('create', MailCreateView.as_view(), name='create'),
    
    path('<int:pk>/detail', MailDetailView.as_view(), name='detail'),
    path('<int:pk>/update', MailUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', MailDeleteView.as_view(), name='delete'),

    path('<int:pk>/admin', admin, name='admin'),

    path('<int:pk>/send', send, name='send')
]
