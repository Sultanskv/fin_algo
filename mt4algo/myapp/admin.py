from django.contrib import admin
# from .models import *
from .models import ClientDetail,ClientSymbolSetting,ClientSignal,HelpMessage,SYMBOL,ClientActivity,MT4Account,Trade,Broker , Client_SYMBOL_QTY, GROUP,OperationMessage,MT5OperationLog,KYC
from django.contrib import admin
from .models import TradeStatus,ClientStatus,mt5_server

from .models import TradeHistory
# Register your models here.

# admin.site.register(MAddress)
# admin.site.register(MCompany)
# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('user_id','is_client','is_client','email','date_joined','last_login','is_admin','is_active','is_staff','is_superuser')  # Adjusted to valid fields
#     search_fields = ['user_id','is_client','is_client','email','date_joined','last_login','is_admin','is_active','is_staff','is_superuser']
#     list_per_page = 10 
    
 
# @admin.register(ClientDetail)
# class ProductAdmin(admin.ModelAdmin):
@admin.register(mt5_server)
class mt5_serverAdmin(admin.ModelAdmin):
    list_display = ('mt5_server','created_at')  # Adjusted to valid fields
    search_fields = ['mt5_server','created_at']
    list_per_page = 10   
    
@admin.register(GROUP)
class GROUPAdmin(admin.ModelAdmin):
    list_display = ('GROUP','min_quantity','max_quantity','created_at')  # Adjusted to valid fields
    search_fields = ['GROUP','min_quantity','max_quantity','created_at']
    list_per_page = 10    


#     list_display = [field.name for field in ClientDetail._meta.fields] 
@admin.register(ClientDetail)
class ClientDetailAdmin(admin.ModelAdmin):
    list_display = ('user_id','user_active','name_first','name_last','email','password','phone_number','verify_code','date_joined','last_login','panel_last_login','clint_plane','client_Group','is_staff','clint_status','country','city','mt5_login','mt5_password','mt5_server','account_type','sub_admin_id','sub_admin_user_active','paid_paln','Term_condition','ip_address','updated_by','selected_option')  # Adjusted to valid fields
    search_fields = ['user_id','user_active','name_first','name_last','email','password','phone_number','verify_code','date_joined','last_login','panel_last_login','clint_plane','client_Group','is_staff','clint_status','country','city','mt5_login','mt5_password','mt5_server','account_type','sub_admin_id','sub_admin_user_active','paid_paln','Term_condition','ip_address','updated_by','selected_option']
    list_per_page = 10   


@admin.register(ClientSymbolSetting)
class ClientSymbolSettingAdmin(admin.ModelAdmin):
    list_display = ('client','symbol','quantity','trade_enabled')  # Adjusted to valid fields
    search_fields = ['client','symbol','quantity','trade_enabled']
    list_per_page = 10    

   
@admin.register(SYMBOL)
class SYMBOLAdmin(admin.ModelAdmin):
    list_display = ('user','SYMBOL','created_at')  # Adjusted to valid fields
    search_fields = ['user','SYMBOL','created_at']
    list_per_page = 10    


# @admin.register(ClientSignal)
# class ProductAdmin(admin.ModelAdmin):
   
#     list_display = [field.name for field in ClientSignal._meta.fields]     
   
@admin.register(ClientSignal)
class ClientSignalAdmin(admin.ModelAdmin):
    list_display = ('user','admin','client_id','message_id','ids','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE','profit_loss','cumulative_pl','created_at')  # Adjusted to valid fields
    search_fields = ['user','admin','client_id','message_id','ids','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE','profit_loss','cumulative_pl','created_at']
    list_per_page = 10         

# @admin.register(Client_SYMBOL_QTY)
# class ProductAdmin(admin.ModelAdmin):
   
#     list_display = [field.name for field in Client_SYMBOL_QTY._meta.fields]  
@admin.register(Client_SYMBOL_QTY)
class Client_SYMBOL_QTYAdmin(admin.ModelAdmin):
    list_display = ('client_id','SYMBOL','QUANTITY','trade','created_at')  # Adjusted to valid fields
    search_fields = ['client_id','SYMBOL','QUANTITY','trade','created_at']
    list_per_page = 10  

    
@admin.register(HelpMessage)
class HelpMessageAdmin(admin.ModelAdmin):
    list_display = ('user_id','client_name','message','timestamp')  # Adjusted to valid fields
    search_fields = ['user_id','client_name','message','timestamp']
    list_per_page = 10      
    

# @admin.register(GROUP)
# class GROUPAdmin(admin.ModelAdmin):
#     list_display = ('user','GROUP','symbols','min_quantity','max_quantity','created_at')  # Adjusted to valid fields
#     search_fields = ['user','GROUP','symbols','min_quantity','max_quantity','created_at']
#     list_per_page = 10    
          

@admin.register(MT4Account)
class MT4AccountAdmin(admin.ModelAdmin):
    list_display = ('login','password','server')  # Adjusted to valid fields
    search_fields = ['login','password','server']
    list_per_page = 10  


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('ticket','symbol','volume','price_open','price_current','sl','tp','profit','time','type')  # Adjusted to valid fields
    search_fields = ['ticket','symbol','volume','price_open','price_current','sl','tp','profit','time','type']
    list_per_page = 10  

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('user','broker','created_at')  # Adjusted to valid fields
    search_fields = ['user','broker','created_at']
    list_per_page = 10    


@admin.register(TradeHistory)
class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'signal_time', 'symbol', 'trade_type', 'quantity', 'entry_price', 'exit_price', 'p_l', 'cumulative_p_l')
    list_editable = ('entry_price', 'exit_price', 'p_l', 'cumulative_p_l')
    search_fields = ('symbol', 'trade_type')
    list_filter = ('symbol', 'trade_type', 'signal_time')
    

@admin.register(ClientActivity)
class ClientActivityAdmin(admin.ModelAdmin):
    list_display = ('user','time','ip_address','action','symbol','symbol','quantity','updated_by')  # Adjusted to valid fields
    search_fields = ['user','time','ip_address','action','symbol','symbol','quantity','updated_by']
    list_per_page = 10           
    
@admin.register(TradeStatus)
class TradeStatusAdmin(admin.ModelAdmin):
    list_display = ('client','symbol','quantity','status_message','timestamp')  # Adjusted to valid fields
    search_fields = ['client','symbol','quantity','status_message','timestamp']
    list_per_page = 10         
    
    
@admin.register(OperationMessage)
class OperationMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp','operation_type','message')  # Adjusted to valid fields
    search_fields = ['timestamp','operation_type','message']
    list_per_page = 10      
    
    
@admin.register(MT5OperationLog)
class MT5OperationLogAdmin(admin.ModelAdmin):
    list_display = ('operation_type','client_login','symbol','message','timestamp')  # Adjusted to valid fields
    search_fields = ['operation_type','client_login','symbol','message','timestamp']
    list_per_page = 10     
       

# @admin.register(KYC)
# class KYCAdmin(admin.ModelAdmin):
#     list_display = ('client','national_id','agreement_signed','terms_accepted','video_file','video_verification_done')  # Adjusted to valid fields
#     search_fields = ['client','national_id','agreement_signed','terms_accepted','video_file','video_verification_done']
#     list_per_page = 10    


from django.utils.html import format_html
from django.contrib import admin
from .models import KYC

# @admin.register(KYC)
# class KYCAdmin(admin.ModelAdmin):
#     list_display = ('client', 'national_id', 'agreement_signed', 'terms_accepted', 'video_preview', 'video_verification_done')  # Added 'video_preview'
#     search_fields = ['client__email', 'national_id', 'agreement_signed', 'terms_accepted', 'video_verification_done']
#     list_per_page = 10
    
#     # Create a method to display video preview
#     @admin.display(description='Video Preview')
#     def video_preview(self, obj):
#         if obj.video_file:
#             return format_html(
#                 '<video width="320" height="240" controls>'
#                 '<source src="{}" type="video/mp4">'
#                 'Your browser does not support the video tag.'
#                 '</video>', obj.video_file.url)
#         return "No video uploaded"


# admin.py
# admin.py
from django.utils.html import format_html
from django.contrib import admin
from .models import KYC

# @admin.register(KYC)
# class KYCAdmin(admin.ModelAdmin):
#     list_display = ('client', 'national_id', 'agreement_signed', 'terms_accepted', 'video_file_display', 'video_verification_done')
#     search_fields = ['client__email', 'national_id', 'agreement_signed', 'terms_accepted', 'video_file', 'video_verification_done']
#     list_per_page = 10

#     def video_file_display(self, obj):
#         if obj.video_file_url():
#             return format_html(
#                 '<div>'
#                 '<video width="200" controls>'
#                 '<source src="{}" type="video/mp4">'
#                 'Your browser does not support the video tag.'
#                 '</video><br>'
#                 '<a href="{}" download="video.mp4">Download Video</a>'
#                 '</div>',
#                 obj.video_file_url(),
#                 obj.video_file_url()
#             )
#         return "No video"

#     video_file_display.short_description = "Video File"



# from django.contrib import admin
# from .models import KYC

# @admin.register(KYC)
# class KYCAdmin(admin.ModelAdmin):
#     list_display = ('client', 'national_id', 'agreement_signed', 'terms_accepted', 'video_file_display', 'video_verification_done')
#     search_fields = ['client__email', 'national_id', 'agreement_signed', 'terms_accepted', 'video_file', 'video_verification_done']
#     list_per_page = 10

#     def video_file_display(self, obj):
#         if obj.video_file_url():
#             return format_html(
#                 '<video width="200" controls>'
#                 '<source src="{}" type="video/mp4">'
#                 'Your browser does not support the video tag.'
#                 '</video>',
#                 obj.video_file_url()
#             )
#         return "No video"

#     video_file_display.short_description = "Video File"




@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('sub_admin_id','clint_id','name','time','clint_email','clint_phone_number','service_name','quantity','strategy','login_date_time','panel_last_login','clint_plane','trading','ip_address','updated_by','client_status')  # Adjusted to valid fields
    search_fields = ['sub_admin_id','clint_id','name','time','clint_email','clint_phone_number','service_name','quantity','strategy','login_date_time','panel_last_login','clint_plane','trading','ip_address','updated_by','client_status']
    list_per_page = 10      

from django.contrib import admin
from .models import MarketData


class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date')  # Columns to display in the admin list view
    search_fields = ('symbol',)  # Enable search by symbol
    list_filter = ('symbol', 'date')  # Filters for easier navigation

admin.site.register(MarketData, MarketDataAdmin)


from django.contrib import admin
from .models import ClientMessage

@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'client', 'message_preview', 'advisory_type', 'created_at', 'read')
    list_filter = ('advisory_type', 'read', 'created_at')
    search_fields = ('client__clint_name_first', 'client__clint_name_last', 'message')
    ordering = ('-created_at',)

    def message_preview(self, obj):
        return obj.message[:50]  # Show first 50 characters of the message

    message_preview.short_description = 'Message Preview'


from django.contrib import admin
from .models import ClientPaymetns, offers_subadmin

# Register the ClientPayments model
@admin.register(ClientPaymetns)
class ClientPaymentsAdmin(admin.ModelAdmin):
    list_display = ('sub_admin_id', 'client', 'name_first', 'name_last', 'payment_txn_id', 'payment_date', 'pay_amount', 'status')
    search_fields = ('sub_admin_id', 'client__user_id', 'name_first', 'name_last', 'payment_txn_id')
    list_filter = ('status', 'payment_date', 'plan_name')
    ordering = ('-payment_date',)
    readonly_fields = ('payment_date', 'bill_date')

# Register the offers_subadmin model
@admin.register(offers_subadmin)
class OffersSubadminAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Offer_Title', 'offer_price', 'revenue')
    search_fields = ('Title', 'Offer_Title')
    list_filter = ('revenue',)



from django.contrib import admin
from .models import KYC

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'national_id_number', 'national_id_name', 
        'national_id_issue_date', 'agreement_signed', 
        'terms_accepted', 'kyc_completed', 'video_verification_done'
    )
    list_filter = ('kyc_completed', 'agreement_signed', 'video_verification_done')
    search_fields = ('client__email', 'national_id_number', 'national_id_name')
    readonly_fields = ('video_file_url',)

    def video_file_url(self, obj):
        if obj.video_file:
            return obj.video_file.url
        return "-"
    video_file_url.short_description = "Video File URL"    
    
from .models import ClientDetail, TradeDeleteLog    


@admin.register(TradeDeleteLog)
class TradeDeleteLogAdmin(admin.ModelAdmin):
    list_display = ('client', 'symbol', 'order_id', 'success', 'timestamp')
    list_filter = ('success', 'symbol', 'timestamp')
    search_fields = ('client__user__username', 'order_id', 'symbol')
    readonly_fields = ('client', 'symbol', 'order_id', 'success', 'error_reason', 'timestamp')