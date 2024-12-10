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
            'logo',
            'city',
            'state_or_province',
            'country',
            'zip_code_or_postal_code',
            'website',
            'about_employer'
        ]

        labels = {
            'about_employer':'About Employer',
            'state_or_province': 'State/province',
            'zip_code_or_postal_code':'Zip code/postal code',
        }


    def clean_employer_name(self):
        company = self.cleaned_data.get('employer_name')

        if not self.instance:
            try:
                instance = Employer.objects.get(employer_name__iexact=company)
            except Employer.DoesNotExist:
                instance = None 
            
            if instance:
                raise forms.ValidationError(f'Employer name is taken.')
            
        return company

    

class JobForm(forms.ModelForm):
 
    class Meta:
        model = Job
        fields = [
            'industry',
            'job_title',
            'job_type',
            'experience_level',
            'work_location',
            'payment_type',
            'currency',
            'salary',
            'currency_code',
            'job_description',
            'qualification'
        ]

        widgets = {
            'job_title': forms.TextInput(attrs={'autofocus':True}),
            'currency': forms.Select(attrs={'onchange':'addCurrencyCode(event)'}),
            'currency_code': forms.TextInput(attrs={'required':False})
        }