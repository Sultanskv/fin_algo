from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

# class RegisterClientForm(UserCreationForm):
    
#     class Meta(UserCreationForm.Meta):
#         model = Account
#         fields=['user_id',]
#     def __init__(self, *args, **kwargs):
#         super(RegisterClientForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'

# class ClientSignalForm(forms.ModelForm):
#      class Meta:
#         model = ClientDetail
#         fields = ['user','admin','client_id','message_id','ids','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE','profit_loss','cumulative_pl','created_at']
        

from django import forms
from .models import ClientDetail

class ClientDetailForm(forms.ModelForm):
    class Meta:
        model = ClientDetail
        fields = '__all__'  # Includes all fields from the model


class ClientLogin(forms.Form):
    user_id = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(ClientLogin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class DateInput(forms.DateInput):
    input_type = 'date'
    
    


class Client_SYMBOL_QTYForm(forms.ModelForm):
    class Meta:
        model = Client_SYMBOL_QTY
        fields = '__all__'
        
        
# class ClientSignalForm(forms.ModelForm):
#     class Meta:
#         model = ClientSignal
#         fields = ['id','created_at','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE']        
    
    
class SymbolForm(forms.ModelForm):
    class Meta:
        model = SYMBOL
        fields = ['user','SYMBOL']
        
class GroupForm(forms.ModelForm):
    class Meta:
        model = GROUP
        fields = ['user','GROUP']

from .models import HelpMessage

class HelpMessageForm(forms.ModelForm):
    class Meta:
        model = HelpMessage
        fields = ['client_name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': 'Enter your message here...',
                'class': 'form-control',
            }),
        }


from django import forms
from .models import MT4Account

class MT4AccountForm(forms.ModelForm):
    class Meta:
        model = MT4Account
        fields = ['login', 'password', 'server']


from .models import GROUP, SYMBOL, Broker

from django import forms
from .models import GROUP, SYMBOL

class GroupForm(forms.ModelForm):
    symbols = forms.ModelMultipleChoiceField(
        queryset=SYMBOL.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
    )

    class Meta:
        model = GROUP
        fields = ['user', 'GROUP', 'symbols', 'min_quantity', 'max_quantity']


        
        
class BrokerForm(forms.ModelForm):
    # brokers = forms.ModelMultipleChoiceField(
    #     queryset=Broker.objects.all(),
    #     # widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
    # )

    class Meta:
        model = Broker
        fields = ['user', 'broker']  # Correct field name

from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField()


# =================================================================kyc==============================================

from django import forms
from .models import KYC

# class NationalIDForm(forms.ModelForm):
#     class Meta:
#         model = KYC
#         fields = ['national_id']
#         widgets = {
#             'national_id': forms.FileInput(attrs={'class': 'form-control'}),
#         }

from django import forms
from .models import KYC

class NationalIDForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['national_id', 'national_id_number', 'national_id_name', 'national_id_issue_date']
        widgets = {
            'national_id': forms.FileInput(attrs={'class': 'form-control'}),
            'national_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ID Number'}),
            'national_id_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on ID'}),
            'national_id_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }




class AgreementForm(forms.Form):
    agreement_signed = forms.BooleanField(label="I agree to the Agreement")
    terms_accepted = forms.BooleanField(label="I accept the Terms & Conditions")

    
class VideoVerificationForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['video_file']
    
    
class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['client', 'national_id', 'national_id_number', 'national_id_name', 
                  'national_id_issue_date', 'agreement_signed', 'agreement_file', 'terms_accepted', 
                  'video_file', 'reference_text']  # Include reference_text

from django import forms
from .models import MarketData

class MarketDataForm(forms.ModelForm):
    class Meta:
        model = MarketData
        fields = ['symbol', 'data']
        widgets = {
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., XAU/USD'}),
            'data': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Enter market data here...'}),
        }


# =========================================================================================
# =========================================================================================    
from myapp.models import *

from django import forms
from django.forms import ModelForm
from django.db.models import Subquery, OuterRef, Min
from subadmin.models import Subadmin_client_limit , sub_adminDT

from myapp.models import offers_subadmin

from django.forms import DateTimeInput

from django import forms
from subadmin.models import sub_adminDT
from django.forms.widgets import DateTimeInput

from django import forms
from subadmin.models import sub_adminDT
from django.forms.widgets import DateTimeInput

class SubadminForm(forms.ModelForm):
    class Meta:
        model = sub_adminDT
        fields = '__all__'
        widgets = {
            'subadmin_logo': forms.ClearableFileInput(),
            'subadmin_date_joined': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'subadmin_last_login': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class SubadminForm(forms.ModelForm):
    class Meta:
        model = sub_adminDT
        fields = '__all__'
        widgets = {
            'subadmin_id': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_name_first': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_name_last': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_email': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_password': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'subadmin_verify_code': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'subadmin_logo': forms.ClearableFileInput(),
            'subadmin_date_joined': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'subadmin_last_login': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        

# forms.py
from django import forms
from .models import offers_subadmin

class SubadminOffersForm(forms.ModelForm):
    class Meta:
        model = offers_subadmin
        fields = ['Title', 'Offer_Title', 'offer_price', 'revenue', 'offer_image']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Offer_Title': forms.TextInput(attrs={'class': 'form-control'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'revenue': forms.TextInput(attrs={'class': 'form-control'}),
            'offer_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
# forms.py
from django import forms

class ClientPaymetnsForm(forms.ModelForm):
    class Meta:
        model = ClientPaymetns
        fields = [
           'name_first', 'name_last', 'payer_email', 'payer_mobile',
            'payment_txn_id', 'payment_date', 'pay_amount', 'bill_no',
            'bill_date', 'plan_name', 'valid_plan_date', 'status'
        ]
        exclude = ['payment_date','bill_date','valid_plan_date']  # Exclude the non-editable field
        widgets = {
            # 'sub_admin_id': forms.TextInput(attrs={'class': 'form-control'}),
            
            'name_first': forms.TextInput(attrs={'class': 'form-control'}),
            'name_last': forms.TextInput(attrs={'class': 'form-control'}),
            'payer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'payer_mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_txn_id': forms.TextInput(attrs={'class': 'form-control'}),
            # 'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  
            'pay_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'bill_no': forms.TextInput(attrs={'class': 'form-control'}),
            # 'bill_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'valid_plan_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }     

    
from django import forms
from myapp.models import ClientDetail

class SubadminClientUpdateForm(forms.ModelForm):
    class Meta:
        model = ClientDetail
        fields = ['name_first', 'name_last', 'email', 'phone_number']  # Allowed fields
        widgets = {
            'name_first': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'name_last': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


    
