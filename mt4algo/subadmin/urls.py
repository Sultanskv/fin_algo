"""
URL configuration for indalgo project.

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
from . import views

urlpatterns = [
    path('subbase/',views.subbase, name='subbase'),
    path('', views.subadmin_login, name='subadmin_login' ),
    path('subadmin_logout/', views.subadmin_logout, name='subadmin_logout' ),
    path('Registration/', views.subadmin_Registration, name='subadmin_Registration' ),
    path('dashboard/', views.dashboard, name='sub_dashboard' ),
    # path('subadmin_client_detail/',views.subadmin_client_detail , name='subadmin_client_detail'),
    path('subthistory/',views.sub_thistory , name='sub_thistory'),
    path('sub_client_status/',views.sub_client_status , name='sub_client_status'),
    path('subadmin_client_registration/',views.subadmin_client_registration , name='subadmin_client_registration'),
    path('subadmin_client_detail/', views.subadmin_client_detail, name='subadmin_client_detail'),
    path('edit_client/<str:user_id>/', views.edit_client, name='edit_client'),
    # # path('subadmin_edit_client/<str:clint_id>/', views.edit_client, name='subadmin_edit_client'),
    # path('create_api/', views.subadmin_create_api, name='subadmin_create_api'),
    # #  path('Creat_client_api/', views.Creat_client_api, name='Creat_client_api'),
    # path('subadmin_Creat_api/<str:pk>/', views.Creat_api, name='subadmin_Creat_api'),
  
  
    
    path('subadmin_offers/', views.subadmin_offers, name='subadmin_offers'),
    
    # path('subadmin/login/', views.SubAdminLoginView.as_view(), name='subadmin_login'),
    # path('subadmin/logout/', views.SubAdminLogoutView.as_view(), name='subadmin_logout'),
    path('payments/', views.payment_list, name='payment_list'),  # List all payments
    path('payments/add/', views.payment_add, name='payment_add'),  # Add a new payment
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),  # Edit a payment
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),  # Delete a payment
    path('revenue_earnings/',views.update_revenue_and_earnings,name='update_revenue_and_earnings'),
    path('earnings/', views.earning_list, name='earning_list'),

    path('subadmin/change-password/', views.subadmin_change_password, name='subadmin_change_password'),
    path('subadmin/forgot-password/', views.subadmin_forgot_password, name='subadmin_forgot_password'),
    path('subadmin/verify-reset/', views.subadmin_verify_reset, name='subadmin_verify_reset'),
 
    path('subadmin_download_pdf/', views.subadmin_download_pdf, name='subadmin_download_pdf'), #downloads agreement pdf
    path('subnext-step/', views.subadmin_upload_national_id, name='subadmin_upload_national_id'),  # First step: National ID upload
    path('subagreement_view/', views.subagreement_view, name='subagreement_view'),  # Step 2: Agreement

    path('subadmin_video_verification_view/', views.subadmin_video_verification_view, name='subadmin_video_verification_view'),
    # path('kyc/video-verification/', views.video_verification_view, name='video_verification'),  # Third step: Video verification
    path('subadmin_submit_kyc/', views.subadmin_submit_kyc, name='subadmin_submit_kyc'),  # Final step: Submit KYC    
]
