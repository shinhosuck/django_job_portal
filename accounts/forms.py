from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from .models import Profile
from django import forms

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'required':True, 'autofocus':True}),
            'email': forms.EmailInput(attrs={'required':True}),
            'password1': forms.PasswordInput(attrs={'required':True}),
            'password2': forms.PasswordInput(attrs={'required':True}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('Email is already taken.')
        return email
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'first_name',
            'last_name',
            'address',
            'city',
            'state_or_province',
            'country',
            'post_code_or_zip_code',
            'email',
            'phone_number',
            'social_link',
            'portfolio_or_personal_website',
            'user_type'
        ]

        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+999999999999999'}),
            'social_link': forms.URLInput(
                attrs={'placeholder': 'https://www.sociallink.com', 'required':False}
            ),
            'portfolio_or_personal_website':forms.URLInput(
                attrs={'placeholder': 'https://www.personalsite.com', 'required':False}
            )
        }

        labels = {
            'portfolio_or_personal_website': 'Portfolio/personal website'
        }

    def clean_phone_number(self):
        nums = [str(num) for num in list(range(0, 10))]
        index = 0

        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:
            for item in phone_number:
                if index == 0 and item != '+':
                    raise forms.ValidationError('Phone number must start with +')
                elif index != 0 and item not in nums:
                    raise forms.ValidationError('Invalid phone number')
                elif len(phone_number) > 15:
                    raise forms.ValidationError('Too many digits.')
                index += 1

            return phone_number
        
        return None
    
    # def clean_social_link(self):
    #     social_link = self.cleaned_data.get('social_link')


    #     url = 'https://www.mysite.com'
    


# class RegisterForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True}),
#                                required=True, max_length=50)
#     email = forms.EmailField(required=True)
#     password = forms.CharField(
#             widget=forms.PasswordInput(attrs={'required':True})
#         )
#     password_confirmation = forms.CharField(
#             widget=forms.PasswordInput(attrs={'required':True})
#         )


#     def clean_username(self):
#         username = self.cleaned_data.get('username')

#         user = User.objects.filter(username=username)

#         if user.exists():
#             raise forms.ValidationError('Username is taken.')

#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
        
#         user = User.objects.filter(email=email)

#         if user.exists():
#             raise forms.ValidationError('Email is taken.')
        
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data['password']
#         password_confirmation = cleaned_data['password_confirmation']
        
#         if password != password_confirmation:
#             self.add_error('password', 'Passwords did not match.')
    
#     def save(self):
#         username = self.cleaned_data.get('username')
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')

#         return User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

       


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


    