from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email', max_length=50)
    nickname = forms.CharField(label='Nickname', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return confirm_password

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password',)
