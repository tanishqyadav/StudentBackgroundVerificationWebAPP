from django import forms
from .models import *

class VerificationDocumentDetailsForm(forms.ModelForm):
     class Meta:
          model = VerificationDocumentDetails
          fields = ['recieved_reference_no', 'received_date', 'received_dept', 'doc_no_received_choice','doc_no_received']
          
          widgets = {
               'recieved_reference_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
               'received_date':forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type':'date'}),
               'received_dept':forms.TextInput(attrs={'class': 'form-control form-control-sm'}), 
               'doc_no_received_choice':forms.Select(attrs={'class': 'form-control form-control-sm'}),
               'doc_no_received':forms.TextInput(attrs={'class': 'form-control form-control-sm'}), 
          }        


class PerformVerificationForm(forms.Form):
     number = forms.CharField(required=True,max_length=100,error_messages={'required':'Please enter Number'},widget=forms.TextInput( attrs={'class': 'form-control form-control-sm mt-2 mb-1 ', 'placeholder':'Number'}))

class PerformVerification1Form(forms.Form):
     DOC_CHOICE = (
           ('','-Select Document-'),(1,'Roll No.'),(2,'Marksheet No.'), (3,'Certificate No.'),
     )
     documnet_type = forms.IntegerField(error_messages={'required':'Please select Document Type'},widget=forms.Select(choices=DOC_CHOICE,attrs={'class': 'form-control form-control-sm mt-2 mb-4', 'placeholder':'Document Type'}),required=True,initial=1)

class PerformVerification2Form(forms.Form):
     remark = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg mt-2 mb-4  required:required', 'placeholder':'Please Give Reasons "if not verifiable"'}))

class PerformVerification3Form(forms.Form):
     verification_assistant_choice = forms.ModelChoiceField(queryset=choice_verification_assistant.objects.all(), widget=forms.Select())

class RevisitForm(forms.Form):
     reference_no = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class': 'form-control orm-control-md mt-2 mb-4  required:required', 'placeholder':'Pls Enter reference number'}))
# class addToVerifiedForm(forms.Form):
#      remark = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class VerificationDispatchDetailsForm(forms.ModelForm):
     class Meta:
          model = VerificationDispatchDetails
          fields = ['dispatch_reference_no', 'dispatch_dept', 'dispatch_date', 'remark']

          widgets = {
               'dispatch_reference_no' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
               'dispatch_dept' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
               'dispatch_date' : forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'type':'date'}),
               'remark': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Please Add Remark "At least with the current status shown above"'}),
          }


from datetime import datetime

class searchDateRange(forms.Form):
     fromDate = forms.DateField(required=True, initial=1, widget=forms.DateInput(attrs={'class': 'form-control datepicker-input','type':'date'}))
     toDate = forms.DateField(required=True, initial=datetime.today().date(), widget=forms.DateInput(attrs={'class': 'form-control datepicker-input','type':'date'}))

class searchRefDeptForm(forms.Form):
     refno = forms.ModelChoiceField(required=False, queryset=VerificationDocumentDetails.objects.all() ,widget=forms.Select(attrs={'class': 'form-control'}))
     