from django import forms 
from .models import Employer, Job 


class EmployerForm(forms.ModelForm):
    employer_name = forms.CharField(
        label='Employer Name',
        widget=forms.TextInput(attrs={'autofocus':True})
    )

    class Meta:
        model = Employer
        fields = [
            'employer_name',
            'city',
            'state_or_province',
            'country',
            'about_employer', 
            'website',
            'logo'
        ]

        labels = {
            'about_employer':'About Employer'
        }


    def clean_company(self):
        company = self.cleaned_data.get('employer_name')

        try:
            instance = Employer.objects.get(company__iexact=company)
        except Employer.DoesNotExist:
            instance = None 
        
        if instance:
            raise forms.ValidationError(f'Employer name is taken.')
        
        return company

class JobForm(forms.ModelForm):
    job_title = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}))
    
    class Meta:
        model = Job
        fields = [
            'job_title',
            'salary',
            'qualification'
        ]