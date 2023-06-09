from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Tag

User = get_user_model()

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
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password',)

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def authenticate_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user
    
class NewPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post

    def save_m2m(self):
        post = self.instance
        tags = self.cleaned_data['tags']
        post.tags.set(tags)