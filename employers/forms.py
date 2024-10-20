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

    def clean_company(self):
        company = self.cleaned_data.get('company')

        try:
            instance = Employer.objects.get(company__iexact=company)
        except Employer.DoesNotExist:
            instance = None 
        
        if instance:
            raise forms.ValidationError(f'Company name is taken.')
        
        return company

class JobsForm(forms.ModelForm):
    job_title = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}))
    class Meta:
        model = Job
        fields = [
            'job_title',
            'salary',
            'qualification'
        ]