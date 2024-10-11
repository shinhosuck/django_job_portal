from django import forms 
from jobs.models import Message 


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]
