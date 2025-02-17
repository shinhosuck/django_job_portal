from django import forms 
from .models import (
    Message, 
    CandidateQualification,
    Education,
    Experience,
)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = [
            'email',
            'message'
        ]

        widgets = {
            'email':forms.EmailInput(attrs={'autofocus':True, 'placeholder':'yourname@mail.com'}),
            'message':forms.Textarea(attrs={'placeholder':'How can we help you?'})
        }


class CandidateQualificationForm(forms.ModelForm):
    class Meta:
        model = CandidateQualification
        fields = [
            'industry',
            'job_title',
            'resume',
            'skills',
        ]

        widgets = {
            'industry':forms.Select(attrs={'autofocus':True, 'autofocus': True}),
            # 'resume': forms.FileInput(attrs={'accept':'img/*', 'required':False})
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education 
        fields = [
            'major',
            'degree', 
            'institution', 
            'start_date',
            'completion_date',
        ]

        widgets = {
            'major': forms.TextInput(attrs={'autofocus': True}),
            'completion_date':forms.DateInput(attrs={'type':'date'})
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience 
        fields = [
            'company_name', 
            'position', 
            'start_date',
            'end_date'
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={'autofocus': True}),
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})
        }
