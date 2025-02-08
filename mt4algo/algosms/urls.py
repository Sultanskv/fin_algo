"""
URL configuration for algosms project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views  # Import views from the current directory

from django.contrib.auth import views as auth_views
from django.urls import path, include
# from .views import client_dashboard, multibank_login, multibank_login_api
from django.views.generic import RedirectView


from django.http import HttpResponse

def empty_favicon(request):
    return HttpResponse(status=204)   

urlpatterns = [
    path('admin/', admin.site.urls),
    ###################  other file urls ##################################   
    # path('',include('myapp.urls')), 
    path('sub/admin/',include('subadmin.urls')),
  
    ##################  myapi views url ####################################
    
    path('home/',views.index , name='index'),
    
   
    path('api/register/', views.registrationapi, name='registrationapi'),  #DRF
    # path('api/client_login/', views.client_login_api, name='client_login_api'),    #DRF
    
    # Your admin authenticate url is here
    path('admin_register/', views.create_superuser, name='create_superuser'),
    path('adminlogin/',views.admin_login, name='admin_login'),
    path('admin_change_password/',views.admin_change_password,name='admin_change_password'),
    path('client_base/',views.client_base,name='client_base'),
    
    
    # Your client authenticate url is here
    path('',views.client_login, name='client_login'),
    path('registration/',views.registration, name='registration'),
    path('clientlist',views.client_list, name='client_list'),
    path('client_view/<str:user_id>/', views.client_view, name='client_view'),
    path('update_client/<str:user_id>/', views.update_client, name='update_client'),
    path('delete_client/<str:user_id>/', views.delete_client, name='delete_client'),
    
    path('adminlogout/',views.logoutAdmin, name='logoutAdmin'),
    path('logout/',views.logoutUser, name='logoutUser'),
    # path('profile/', views.profile, name='profile'),
    path('changepassword/',views.change_password, name='change_password'),
    path('client_forgot_password/', views.client_forgot_password, name='client_forgot_password'),
    path('verify_reset/', views.client_verify_reset, name='verify_reset'),
    
    path('add_singnal_qty/',views.add_singnal_qty, name='add_singnal_qty'),
    path('symbol_inactive/',views.symbol_inactive, name='symbol_inactive'),
    
    
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_message/',views.admin_message, name='admin_message'),
    # path('admin_signals/',views.admin_signals, name='admin_signals'),
    path('admin_thistory/',views.admin_thistory, name='admin_thistory'),
    path('client_status_admin/',views.client_status_admin, name='client_status_admin'),
    # path('admin_client/',views.admin_client,name='admin_client'),
    path('admin_help_center/',views.admin_help_center,name='admin_help_center'),
    path('settings/',views.Settings,name='Settings'),
    
    path('dashboard/',views.client_dashboard, name='client_dashboard'),
    path('signals/',views.client_signals, name='client_signals'),
    path('tradehistory/',views.client_trade_history, name='client_trade_history'),
    path('tradingstatus/',views.client_tstatus, name='client_tstatus'),
    path('multibank/',views.multibank, name='multibank'),
    # path('broker-connect/', views.broker_connect, name='broker_connect'),
    # path('broker_connect/<str:user_id>/', views.broker_connect, name='broker_connect'),
    
    path('create_symbol_qty/',views.create_client_symbol_qty, name='create_client_symbol_qty'),
    path('symbol_qty_list/',views.client_symbol_qty_list, name='client_symbol_qty_list'),
    path('edit_symbol_qty/',views.edit_client_symbol_qty, name='edit_client_symbol_qty'),
    path('delete_symbol_qty/',views.delete_client_symbol_qty, name='delete_client_symbol_qty'),
  
    path('symbol_list/',views.symbol_list, name='symbol_list'),
    path('create_symbol/',views.create_symbol, name='create_symbol'),
    path('update_symbol/<int:symbol_id>/', views.update_symbol, name='update_symbol'),
    path('delete_symbol/<int:symbol_id>/', views.delete_symbol, name='delete_symbol'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='client_login'), name='logout'),
    path('', auth_views.LoginView.as_view(), name='client_login'),
    
    path('client_help_center/', views.client_help_center, name='client_help_center'),
    path('admin_help_center/', views.admin_help_center, name='admin_help_center'),

    path('Analysis/',views.Analysis, name='Analysis'),
    path('mt4-panel/', views.mt4_panel, name='mt4_panel'),
    # path('place_order/', views.place_order, name='place_order'),
    # path('get_price/', views.get_price, name='get_price'),
    # path('trade_history/', views.trade_history, name='trade_history'),
    # path('trade_history11/', views.trade_history11, name='trade_history11'), 
    path('ai_trading/', views.ai_trading, name='ai_trading'), 
    path('delete_trades/', views.delete_trades, name='delete_trades'),
    # path('close_all_orders/', views.close_all_orders, name='close_all_orders'),
    path('open_trades/', views.fetch_open_trades, name='open_trades'),

    # path('symbol-settings/', views.symbol_settings, name='symbol_settings'),
    # path('fetch-symbols/', views.fetch_symbols, name='fetch_symbols'),
    # path('close_orders/', views.close_orders_view, name='close_orders'),
    path('trade-history/', views.trade_history_view, name='trade_history'),
    path('client-trade-history/', views.client_trade_history_view, name='client_trade_history'),
    # path('api/live_price/<str:symbol>/', views.live_price, name='live_price'),

     
    # path('fetch_trade_data/', views.fetch_trade_data, name='fetch_trade_data'),

    # path('loginmt/', views.login_all_accounts, name='login_all_accounts'),
    # path('logoutmt/', views.logout_all_accounts, name='logout_all_accounts'),
    # path('accounts/', views.account_list, name='account_list'),
    # path('accounts/add/', views.account_add, name='account_add'),
    # path('accounts/delete/<int:account_id>/', views.account_delete, name='account_delete'),

    path('group_list/',views.group_list, name='group_list'),
    path('create_group/',views.create_group, name='create_group'),
    path('update_group/<int:group_id>/', views.update_group, name='update_group'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    # path('get_symbols/<int:group_id>/', views.get_symbols, name='get_symbols'),
    # path('trade_status/', views.trade_status_view, name='trade_status'),
    # # path('client/<str:client_id>/trade_status/', views.client_trade_status_view, name='client_trade_status'),
    # path('operation-messages/', views.operation_messages_view, name='operation_messages'),
    # path('logs/', views.view_mt5_logs, name='view_mt5_logs'),

    
    path('broker_list/',views.broker_list, name='broker_list'),
    path('create_broker/',views.create_broker, name='create_broker'),
    path('update_broker/<int:broker_id>/', views.update_broker, name='update_broker'),
    path('delete_broker/<int:broker_id>/', views.delete_broker, name='delete_broker'),

    path('upload-excel/', views.upload_excel, name='upload_excel'),
    # path('fetch_mt5_data/', views.fetch_mt5_data, name='fetch_mt5_data'),
    

    path('run_app/<path:broker_url>/', views.run_pyqt_app, name='run_pyqt_app'),  # Use <path:broker_url> to allow slashes

    

    path('signup/', views.signup_view, name='signup'),
    path('verify/', views.register_verify, name='verify'),

    path('download_pdf/', views.download_pdf, name='download_pdf'), #downloads agreement pdf
    path('next-step/', views.upload_national_id, name='upload_national_id'),  # First step: National ID upload
    path('kyc/agreement/', views.agreement_view, name='agreement'),  # Step 2: Agreement

    path('kyc/video-verification/', views.video_verification_view, name='video_verification'),  # Third step: Video verification
    path('kyc/submit/', views.submit_kyc, name='submit_kyc'),  # Final step: Submit KYC
    path('brokers/', views.broker_selection_view, name='broker_selection'),  # URL for broker selection
    path('favicon.ico', empty_favicon),


    
    # add google login url  href="{% url 'google_login' %}"  Templet
    path('google/login/', views.google_login, name='google_login'),
    path('accounts/google/callback/', views.google_callback, name='google_callback_login'),

    # add google login url
    path('facebook/login/', views.facebook_login, name='facebook_login'),
    path('facebook/callback/', views.facebook_callback, name='facebook_callback'),
    
    # twitter URL
    path('twitter/login/', views.twitter_login, name='twitter_login'),
    path('twitter/callback/', views.twitter_callback, name='twitter_callback'), 

    path('upload-data/', views.upload_data, name='upload_data'),
    path('client_advisory/', views.client_advisory, name='client_advisory'),
    path('mark-read/<int:message_id>/', views.mark_read, name='mark_read'),
    # path('mark_notifications_read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('fetch-new-messages/', views.fetch_new_messages, name='fetch_new_messages'),
    path('fetch-unread-messages/', views.fetch_unread_messages, name='fetch_unread_messages'),
    path('fetch-new-message/', views.fetch_new_message, name='fetch_new_message'),
    # path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('fetch-client-notifications/', views.fetch_client_notifications, name='fetch_client_notifications'),
    path('mark-client-notifications-read/', views.mark_client_notifications_read, name='mark_client_notifications_read'),
    path('register/', views.client_register, name='register'),

    path('subadmin_list/', views.subadmin_list, name='subadmin_list'),
    path('subadmin/create/', views.subadmin_create, name='subadmin_create'),
    path('subadmin/update/<str:pk>/', views.subadmin_update, name='subadmin_update'),   
    path('subadmin/delete/<str:pk>/', views.subadmin_delete, name='subadmin_delete'),
    # path('subadmin_view', views.subadmin_view, name='subadmin_view'),
        
    path('Subadmin_client_limit/', views.Subadmin_client_limit, name='Subadmin_client_limit'),
    
    path('subadmin_view/<str:clint_id>/', views.subadmin_view, name='subadmin_view'),  # Add this line
    path('limit/', views.Subadmin_client_limit_list, name='Subadmin_client_limit_list'),
    path('payment/', views.client_pay_payment, name='client_pay_payment'),

    
    path('subadmin_create_limit/', views.subadmin_create_limit, name='subadmin_create_limit'),
    path('subadmin/update/<int:pk>/', views.subadmin_update_limit, name='subadmin_update_limit'),
    path('subadmin/delete/<int:pk>/', views.subadmin_delete_limit, name='subadmin_delete_limit'),
    # path('subadmin_view', views.subadmin_view, name='subadmin_view'),
    
    path('kyc/', views.kyc_list, name='kyc_list'),
    path('kyc-pdf/', views.download_pdf_kyc, name='download_pdf_kyc'),
    # path('kyc/delete/<int:pk>/', views.kyc_delete, name='kyc_delete'),
    # path("locations/", views.location_list, name="location_list"),
    # path('usa/',views.usa_list, name='usa_list'),
    
    
    #subadmin offer
    path('offers/', views.subadmin_offers_list, name='subadmin_offers_list'),
    path('offers/add/', views.subadmin_offer_add, name='subadmin_offer_add'),
    path('offers/edit/<int:pk>/', views.subadmin_offer_edit, name='subadmin_offer_edit'),
    path('offers/delete/<int:pk>/', views.subadmin_offer_delete, name='subadmin_offer_delete'),
    path('edit_trade/<int:trade_id>/', views.edit_trade, name='edit_trade'),
    path('delete_trade/<int:trade_id>/', views.delete_trade, name='delete_trade'),
    # path('fetch-client-mt5/', views.fetch_client_mt5, name='fetch_client_mt5'),
    path('add_trade/', views.add_trade, name='add_trade'),
    path('download-trade-history-pdf/', views.download_trade_history_pdf, name='download_trade_history_pdf'),
    path('simplex_payment/', views.simplex_payment, name='simplex_payment'),
    

    #===================== Meta Api =================================

    path('metaapi_view/', views.metaapi_view, name='metaapi_view'),
    path('mataapi-profile/', views.mataapi_profile, name='mataapi_profile'),    

    path("trade", views.trade_form, name="trade_form"),
    path("place_trade", views.place_trade, name="place_trade"),
    path("get_market_price", views.get_market_price, name="get_market_price"),

    path('close-positions/', views.close_positions_by_symbol, name='close_positions_by_symbol'),
    path('close-trade-form/', views.close_trade_form, name='close_trade_form'),
    path('close-log-summary/', views.close_log_summary, name='close_log_summary'),
    path('close-log-details/', views.close_log_details, name='close_log_details'),
    
    path('chart/', views.render_chart, name='chart'),  # URL for the frontend chart
    path("orders/", views.client_orders_view, name="client_orders"),
    path('api/client_data/', views.client_data_api, name='client_data_api'),
    path('trade-summary/', views.trade_summary, name='trade_summary'),
    path('trade-logs/', views.trade_log_details, name='trade_log_details'),
    path('download-trade-history-pdf/', views.download_trade_history_pdf, name='download_trade_history_pdf'),
    # path('update-trade-history/', views.update_trade_history_view, name="update_trade_history"),
    path('update-trade-history/', views.run_update_trade_history, name='update_trade_history'),
    path('configure-trading-account/', views.configure_trading_account, name='configure_trading_account'),
    path('configure-account/', views.configure_account_page, name='configure_account_page'),
    path('simplex_payment/', views.simplex_payment, name='simplex_payment'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# For development only. In production, use a web server like Nginx to serve media files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Only serve static files when DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

