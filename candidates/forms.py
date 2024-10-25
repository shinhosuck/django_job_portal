from typing import Any
from django import forms 
from .models import Message, Candidate


class MessageForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus':True}))
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]


class CandidateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'autofocus':True}))
    class Meta:
        model = Candidate 
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'job_title',
            'resume',
            'social_link'
        ]


