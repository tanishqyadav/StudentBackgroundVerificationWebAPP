from django import forms
from .models import docvUser
from django.contrib.auth.hashers import *

class SignupForm(forms.ModelForm):
     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder':'Confirm Password' ,'aria-label':'confirm password', 'aria-describedby':'basic-addon1'}))
     class Meta:
          model = docvUser
          fields = ['email', 'name', 'password', 'user_type' ]

          widgets = {
               'email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder':'Email' ,'aria-label':'email', 'aria-describedby':'basic-addon1'}),
               'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder':'Name' ,'aria-label':'name', 'aria-describedby':'basic-addon1'}),
               'user_type': forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder':'UserType' ,'aria-label':'user_type', 'aria-describedby':'basic-addon1'}),
               'password' : forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder':'Password' ,'aria-label':'password', 'aria-describedby':'basic-addon1'}),
          }
     def clean(self):
          cleaned_data = super(SignupForm, self).clean()
          password = cleaned_data.get('password')
          confirm_password = cleaned_data.get('confirm_password')
          if password != confirm_password:
               self.add_error('confirm_password', "Password does not match")

          return cleaned_data

     def clean_email(self):
        email = self.cleaned_data['email']
        users = docvUser.objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("User with this Email already exists")
        return email.lower()

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         users = docvUser.objects.filter(username__iexact=username)
#         if users:
#             raise forms.ValidationError("Custom text about username.")
#         return username

class LoginForm(forms.Form):
     email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg' ,'placeholder':'Email', 'aria-label':'email', 'aria-describedby':'basic-addon1'}))
     password = forms.CharField(max_length=254, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg','placeholder':'Password', 'aria-label':'password', 'aria-describedby':'basic-addon1'}))
     

     def clean(self):
          cleaned_data = super(LoginForm, self).clean()
          password = cleaned_data.get('password')
          email = cleaned_data.get('email')
          
          if not check_password(password, docvUser.objects.filter(email__iexact=email).first().password):
                    self.add_error('password', "Check Password")
          
          
          if not docvUser.objects.filter(email__iexact=email).exists():
               self.add_error('email', "Check Your Email")

          return cleaned_data