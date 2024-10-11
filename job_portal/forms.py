from django import forms 
from job_portal.models import Message 


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]
