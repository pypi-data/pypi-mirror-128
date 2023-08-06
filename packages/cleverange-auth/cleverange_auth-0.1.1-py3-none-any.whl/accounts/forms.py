from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

        def clean_email(self):
            email = self.cleaned_data["email"].lower()
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValueError(f'email {self.email} is Already used.')
        
        def clean_username(self):
            username = self.cleaned_data["username"]
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                return username
            raise forms.ValueError(f'email {self.username} is Already used.')
    