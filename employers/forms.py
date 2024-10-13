from django import forms 
from .models import Employer, Job 


class EmployerForm(forms.ModelForm):
    company = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}))
    class Meta:
        model = Employer
        fields = [
            'company',
            'description', 
            'website',
            'logo'
        ]


class JobsForm(forms.ModelForm):
    job_title = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}))
    class Meta:
        model = Job
        fields = [
            'job_title',
            'salary',
            'qualification'
        ]