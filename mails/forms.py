from django.forms import ModelForm

from .models import Mail

class CreateMailForm(ModelForm):
    class Meta:
        model = Mail
        fields = ['subject', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject'
        })

        self.fields['content'].widget.attrs.update({
            'id': 'content',
            'class': 'form-control',
        })