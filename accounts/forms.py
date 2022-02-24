from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(forms.Form):
    username = forms.CharField(
                 widget=forms.TextInput(attrs={'placeholder':'Username','id':'name', 
                                                    'class':'form-control form-control-prepended'}))
    password = forms.CharField(
                 widget=forms.PasswordInput(attrs={'placeholder':'Password','id':'password',
                                                   'class':'form-control form-control-prepended'}))
    """widgets={
              "username": forms.TextInput(attrs{'placeholder':'Username', 
              'id':'username', 'class':'form-control'}),
              "password":forms.PasswordInput(attrs{'placeholder':'Username', 
              'id':'username', 'class':'form-control'}),
    }
    """

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
                 widget=forms.TextInput(attrs={'placeholder':'Firstname', 
                                                    'class':'form-control form-control-prepended','id':'name'}))
    last_name = forms.CharField(
                 widget=forms.TextInput(attrs={'placeholder':'Surname', 
                                                    'class':'form-control form-control-prepended','id':'name'}))
    email = forms.EmailField(
                 widget=forms.TextInput(attrs={'placeholder':'Email','id':'email', 
                                                    'class':'form-control form-control-prepended'}))
    
    username = forms.CharField(
                 widget=forms.TextInput(attrs={'placeholder':'Username', 
                                                    'class':'form-control form-control-prepended'}))
    password1 = forms.CharField(
                 widget=forms.PasswordInput(attrs={'placeholder':'Password','id':'password',
                                                   'class':'form-control form-control-prepended'}))
    password2 = forms.CharField(
                 widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','id':'password', 
                                                    'class':'form-control form-control-prepended'}))
    
    class Meta:
        model = get_user_model()

        fields = ('username', 'first_name', 'last_name', 'email','is_admin','is_instructor','is_student')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'id':'firstname'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'id':'lastname'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'id':'emaile'})
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex', 
                 'phone', 
                 'bio', 
                 'country', 
                 'twitter_link',
                 'facebook_link', 
                  'date_of_birth')
                  
        widgets = {
            'date_of_birth': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['sex'].widget.attrs.update({'class' : 'form-control', 'id':'sex'})
        self.fields['phone'].widget.attrs.update({'class' : 'form-control', 'id':'phone'})
        self.fields['bio'].widget.attrs.update({'class' : 'form-control', 'id':'bio'})
        self.fields['country'].widget.attrs.update({'class' : 'form-control', 'id':'country'})
        self.fields['twitter_link'].widget.attrs.update({'class' : 'form-control', 'id':'twitter_link'})
        self.fields['facebook_link'].widget.attrs.update({'class' : 'form-control', 'id':'facebook_link'})
        self.fields['date_of_birth'].widget.attrs.update({'class' : 'form-control', 'id':'date_of_birth', 'type':'date'})
    

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)

    def __init__(self, *args, **kwargs):
        super(ProfilePhotoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class' : 'form-control', 'id':'photo'})
       

class ChangeUsernameForm(forms.Form):
    
    old_username = forms.CharField(max_length=150)
    new_username = forms.CharField(max_length=150)
    
    def __init__(self, *args, **kwargs):
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.fields['old_username'].widget.attrs.update({'class' : 'form-control', 'id':'old_username', 'placeholder':'Old username'})
        self.fields['new_username'].widget.attrs.update({'class' : 'form-control', 'id':'new_username', 'placeholder':'New username'})



class ChangePasswordForm(forms.Form):
    
    old_password = forms.CharField(max_length=150)
    new_password = forms.CharField(max_length=150)
    
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class' : 'form-control', 'id':'old_password', 'placeholder':'Old password'})
        self.fields['new_password'].widget.attrs.update({'class' : 'form-control', 'id':'new_password', 'placeholder':'New password'})
