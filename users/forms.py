from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text-field'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-field'}))
    
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username','email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'text-field'})
        self.fields['email'].widget.attrs.update({'class':'text-field'})
        

class  ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=  ['image'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'file-ip'})


        