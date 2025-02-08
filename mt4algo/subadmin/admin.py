from django.contrib import admin
# In subadmin/models.py
from subadmin.models import sub_adminDT,Subadmin_client_limit
from .models import *


@admin.register(sub_adminDT)
class sub_adminDTAdmin(admin.ModelAdmin):
    list_display = ('subadmin_id','subadmin_active','subadmin_name_first','subadmin_name_last','subadmin_email','subadmin_password','subadmin_phone_number','subadmin_verify_code','subadmin_keyword','subadmin_logo',  'created_at','last_modified','subadmin_client_limit','subadmin_status','subadmin_date_joined','subadmin_last_login','subadmin_account_type', 'sub_admin_active','subadmin_paid_paln','subadmin_Term_condition','subadmin_ip_address','total_revenue','earnings')  # Adjusted to valid fields
    search_fields = ['subadmin_id','subadmin_active','subadmin_name_first','subadmin_name_last','subadmin_email','subadmin_password','subadmin_phone_number','subadmin_verify_code','subadmin_keyword','subadmin_logo',  'created_at','last_modified','subadmin_client_limit','subadmin_status','subadmin_date_joined','subadmin_last_login','subadmin_account_type', 'sub_admin_active','subadmin_paid_paln','subadmin_Term_condition','subadmin_ip_address','total_revenue','earnings'] # Search by subadmin_id fields (adjust if necessary)
    list_per_page = 10

class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in sub_adminDT._meta.fields] 
    # list_display = ('subadmin_id', 'subadmin_name_first', 'total_revenue', 'earnings')
    readonly_fields = ('earnings',)  

@admin.register(Subadmin_client_limit)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Subadmin_client_limit._meta.fields]      
    
@admin.register(SUBKYC)
class SUBKYCAdmin(admin.ModelAdmin):
    list_display = ('subadmin_id','subadmin_national_id','subadmin_national_id_number','subadmin_national_id_name','subadmin_national_id_issue_date','subadmin_agreement_signed','subadmin_agreement_file','subadmin_terms_accepted','subadmin_reference_text','subadmin_kyc_completed','subadmin_video_file','subadmin_video_verification_done')  # Adjusted to valid fields
    search_fields = ['subadmin_id','subadmin_national_id','subadmin_national_id_number','subadmin_national_id_name','subadmin_national_id_issue_date','subadmin_agreement_signed','subadmin_agreement_file','subadmin_terms_accepted','subadmin_reference_text','subadmin_kyc_completed','subadmin_video_file','subadmin_video_verification_done'] # Search by subadmin_id fields (adjust if necessary)
    list_per_page = 10

