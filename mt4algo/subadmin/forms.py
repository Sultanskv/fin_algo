
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms
from subadmin.models import sub_adminDT
from django.forms.widgets import DateTimeInput

class SubadminForm(forms.ModelForm):
    class Meta:
        model = sub_adminDT
        fields = '__all__'
        widgets = {
            'subadmin_logo': forms.ClearableFileInput(),  # File upload widget
            'subadmin_date_joined': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),  # DateTime widget
            'subadmin_last_login': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),  # DateTime widget
        }

    def __init__(self, *args, **kwargs):
        super(SubadminForm, self).__init__(*args, **kwargs)
        # Mark these fields as required
        self.fields['subadmin_name_first'].required = True
        self.fields['subadmin_name_last'].required = True
        self.fields['subadmin_email'].required = True
        self.fields['subadmin_password'].required = True
        self.fields['subadmin_phone_number'].required = True
        self.fields['subadmin_status'].required = True


from django import forms
from .models import Subadmin_client_limit

class SubadminLimitForm(forms.ModelForm):
    class Meta: 
        model = Subadmin_client_limit
        fields = ['Subadmin_limit', 'max_quantity', 'used_credit', 'withdraw', 'expired_limit', 'active_limit']  # Adjust this to include existing fields
        widgets = {
            'Subadmin_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'used_credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'withdraw': forms.NumberInput(attrs={'class': 'form-control'}),
            'expired_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'active_limit' : forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms
from subadmin.models import SUBKYC

class SUBAdminNationalIDForm(forms.ModelForm):
    class Meta:
        model = SUBKYC
        fields = ['subadmin_national_id', 'subadmin_national_id_name', 'subadmin_national_id_number', 'subadmin_national_id_issue_date']
        widgets = {
            'subadmin_national_id': forms.FileInput(attrs={'class': 'form-control'}),
            'subadmin_national_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ID Number'}),
            'subadmin_national_id_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on ID'}),
            'subadmin_national_id_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }  
        

    # Add any custom validation if required        
        
from django import forms

class SUBAdminAgreementForm(forms.Form):
    subadmin_agreement_signed = forms.BooleanField(
        required=True, label="Agreement Signed"
    )
    subadmin_terms_accepted = forms.BooleanField(
        required=True, label="Terms Accepted"
    )


# class SUBAdminAgreementForm(forms.Form):
#     agreement_signed = forms.BooleanField(required=True, label="I agree to the Agreement")
#     terms_accepted = forms.BooleanField(required=True, label="I accept the Terms & Conditions")
    
    
class SUBKYCVideoVerificationForm(forms.ModelForm):
    class Meta:
        model = SUBKYC
        fields = ['subadmin_video_file']
    
    
class SUBKYCForm(forms.ModelForm):
    class Meta:
        model = SUBKYC
        fields = ['subadmin_id', 'subadmin_national_id', 'subadmin_national_id_number', 'subadmin_national_id_name', 
                  'subadmin_national_id_issue_date', 'subadmin_agreement_signed', 'subadmin_agreement_signed', 'subadmin_agreement_file', 
                  'subadmin_terms_accepted','subadmin_reference_text','subadmin_video_file', 'subadmin_video_verification_done', 'reference_text']  # Include reference_text

