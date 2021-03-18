from django.db import models
from django.utils import timezone

from users.models import User
from mails.models import Mail

class UserMail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    token = models.CharField(max_length=100, null=True, blank=True)
    sent_at =  models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.mail.subject} - {self.user.username}"

    def update_read(self):
        self.read = True
        self.last_read_at = timezone.now()
        
        self.save()

