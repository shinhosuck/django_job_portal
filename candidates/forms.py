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
            'email':forms.EmailInput(attrs={'autofocus':True})
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
            'industry':forms.Select(attrs={'autofocus':True}),
            'resume': forms.FileInput(attrs={'accept':'img/*', 'required':False})
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
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})
        }
