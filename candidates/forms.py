from django import forms 
from .models import Message, Candidate


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate 
        fields = [
            'first_name',
            'last_name',
            'job_title',
            'occupation',
            'resume',
        ]



