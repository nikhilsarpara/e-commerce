from django import forms
from .models import *

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    con_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    class Meta:
        model = registration
        fields = ['firstname','lastname','email','phone','password']

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        con_password = cleaned_data.get('con_password')

        if password != con_password:
            raise forms.ValidationError("Password and Confirm Password not match.")

    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.fields['firstname'].widget.attrs['placeholder'] = "Firstname"
        self.fields['lastname'].widget.attrs['placeholder'] = "Lastname"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['phone'].widget.attrs['placeholder'] = "phone"

        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"

    
class AccountForm(forms.ModelForm):
    class Meta:
        model = registration
        fields = ['firstname','lastname','email','phone']

    def __init__(self,*args,**kwargs):
        super(AccountForm,self).__init__(*args,**kwargs)

        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"

class ProfileForm(forms.ModelForm):
    profile_image =  forms.ImageField(required=False,widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['profile_image',]

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)

        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"