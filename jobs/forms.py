from django import forms 
from jobs.models import Message 


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = [
            'first_name',
            'last_name',
            'email',
            'message'
        ]
