from typing import Any
from django import forms 
from .models import Message, CandidateJobProfile


class MessageForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus':True}))
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]


class CandidateJobProfileForm(forms.ModelForm):
    skills = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'placeholder':'e.g., skill 1, skill 2, skill 3'})
        )

    class Meta:
        model = CandidateJobProfile 
        fields = [
            'industry',
            'first_name',
            'last_name',
            'job_title',
            'skills',
            'resume',
            'social_link'
        ]
