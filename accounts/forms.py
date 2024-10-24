from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from django import forms

User = get_user_model()


# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User 
#         fields = ['username', 'email', 'password1', 'password2']

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         user = User.objects.filter(email=email)
#         if user.exists():
#             raise forms.ValidationError('Email is already taken.')
#         return email
    

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}),
                               required=True, max_length=50)
    email = forms.EmailField(required=True)
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'required':True})
        )
    password_confirmation = forms.CharField(
            widget=forms.PasswordInput(attrs={'required':True})
        )


    def clean_username(self):
        username = self.cleaned_data.get('username')

        user = User.objects.filter(username=username)

        if user.exists():
            raise forms.ValidationError('Username is taken.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        user = User.objects.filter(email=email)

        if user.exists():
            raise forms.ValidationError('Email is taken.')
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']
        
        if password != password_confirmation:
            self.add_error('password', 'Passwords did not match.')
    
    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

       


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}), required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = User.objects.filter(username=username)

        if not user.exists():
            raise forms.ValidationError('Username or password did not match.')
        
        else:
            valid= user.first().check_password(password)
            if not valid:
                raise forms.ValidationError('Username or password did not match.')
    
        return self.cleaned_data 


    