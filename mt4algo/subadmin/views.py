
# text/x-generic views.py ( Python script, ASCII text executable, with CRLF line terminators )
from django.shortcuts import render , HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
import logging
from myapp.models import *
# Create your views here.

def subbase(request):
    return render(request,'subadmin/subadmin_base.html')


# def subbase(request):
#     return render(request,'subadmin_base.html')

def sub_thistory(request):
    return render(request,'sub_admin_thistory.html')

# views.py
#subadmin/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import sub_adminDT , Subadmin_client_limit

def subadmin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            subadmin = sub_adminDT.objects.get(subadmin_email=email)                 
            # Check if the subadmin is active (subadmin_status is True)
            if not subadmin.sub_admin_active:
                messages.error(request, 'Your account is inactive. Please contact the administrator.')
                print(messages)
                return redirect('/sub/admin/')  # Redirect back to the login page
            
            if subadmin.subadmin_password == password:
                # Check if terms and conditions are accepted
                if not subadmin.subadmin_Term_condition:
                    messages.error(request, 'Please accept the terms and conditions before logging in.')
                    request.session['subadmin_email'] = email  # Store email in session for upload_national_id
                    return redirect('subadmin_upload_national_id')  # Redirect to the upload_national_id view

                if subadmin.subadmin_last_login and subadmin.subadmin_last_login.date() >= timezone.now().date():
                    # Store session data
                    request.session['subadmin_id'] = subadmin.subadmin_id
                    
                    return redirect('/sub/admin/dashboard/')  # Change 'home' to your desired redirect URL
                else:
                    messages.error(request, 'Your plan has expired.')
                    return redirect('/sub/admin/?msg=Your plan has expired.')
            else:
                messages.error(request, 'Invalid password')
        except sub_adminDT.DoesNotExist:
            messages.error(request, 'Invalid email')

    return render(request, 'subadmin/login.html')

def subadmin_logout(request):
    subadmin_id = request.session.get('subadmin_id')
    del request.session['subadmin_id']
    return redirect('subadmin_login')

from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    # print('test ssdd')
    # return HttpResponse('test')
    if 'subadmin_id' in request.session:
        subadmin_id = request.session.get('subadmin_id')
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        client_count = ClientDetail.objects.filter(sub_admin_id = subadmin_id).count()
        print(subadmin_code ,client_count )

        Panel_Login = ClientDetail.objects.filter(sub_admin_id = subadmin_id,clint_status = 'Panel Login').count()
        Panel_Logout = ClientDetail.objects.filter(sub_admin_id = subadmin_id,clint_status = 'Panel Log out').count()
        api_on = ClientDetail.objects.filter(sub_admin_id=subadmin_id, account_type='live').count()

        api_off = ClientDetail.objects.filter(sub_admin_id = subadmin_id ,account_type = 'Demo').count()
        paid = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = True).count()
        Demo = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = False).count()

        client_limit = subadmin_code.subadmin_client_limit.max_quantity 
        client_available = client_limit - client_count
        client_use = client_limit - client_available
        # print(client_limit, client_count)
        # if client_limit >= client_count:
        #     print(client_limit, client_count , 'yesy')
       

        #   # Get the current date
        current_date = timezone.now()
        # Filter clients who have expired (clint_last_login < current date)
        demo_expired_login = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = False ,last_login__lt=current_date).count()
        # Filter clients who are not expired (clint_last_login >= current date)
        demo_not_expired_login = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = False,last_login__gte=current_date).count()

        # Filter clients who have expired (clint_last_login < current date)
        paid_expired_login = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = True ,last_login__lt=current_date).count()
        # Filter clients who are not expired (clint_last_login >= current date)
        paid_not_expired_login = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = True,last_login__gte=current_date).count()

        # Expired_Paid_License  = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = True,clint_paid_paln_from_date__lt=current_date).count()
        # Valid_Paid_License = ClientDetail.objects.filter(sub_admin_id = subadmin_id,paid_paln = True,clint_paid_paln_from_date__gte=current_date).count()
        return render(request,'subadmin/subadmin_dashboard.html',{
                'subadmin_code':subadmin_code ,
                'client_count':client_count,
                

                'Panel_Login':Panel_Login,
                'Panel_Logout':Panel_Logout,
                'api_on':api_on,
                'api_off':api_off,
                'paid':paid,
                'Demo':Demo,
                'client_limit':client_limit,
                'client_available':client_available,
                'client_use':client_use,

                'demo_expired_login': demo_expired_login,
                'demo_not_expired_login': demo_not_expired_login,
                'paid_expired_login': paid_expired_login,
                'paid_not_expired_login': paid_not_expired_login,
                # 'Expired_Paid_License':Expired_Paid_License,
                # 'Valid_Paid_License':Valid_Paid_License
                       })
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login') 

# def dashboard(request):
#     period = timedelta(days=30)
#     current_date = timezone.now()

#     # Your existing counts
#     active_live_account = ClientDetail.objects.filter(clint_plane='Live', clint_last_login__gte=current_date - period).count()
#     client_count = ClientDetail.objects.filter(clint_plane='Live').count()  
#     total_demo_account = ClientDetail.objects.filter(clint_plane='Demo').count()
#     total_licence = ClientDetail.objects.filter(paid_paln=True).count()
#     total_2days_service = ClientDetail.objects.filter(service_name__icontains='2 days').count()

#     # Fetching subadmin client limits
#     client_limits = Subadmin_client_limit.objects.all()

#     # Pass the data to context
#     context = {
#         'clientcount': client_count,
#         'total_demo_account': total_demo_account,
#         'total_licence': total_licence,
#         'total_2days_service': total_2days_service,
#         'active_live_account': active_live_account,
#         'client_limits': client_limits,  # Add this line
#     }

#     return render(request, 'subadmin/subadmin_dashboard.html', context)



# def dashboard(request):
#     # print('test ssdd')
#     # return HttpResponse('test')
#     if 'subadmin_id' in request.session:
#         subadmin_id = request.session.get('subadmin_id')
#         subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
#         client_count = ClientDetail.objects.filter(sub_admin_id = subadmin_id).count()
#         client_limit = subadmin_code.subadmin_client_limit.max_quantity 
#         print(client_limit, client_count)
#         if client_limit >= client_count:
#             print(client_limit, client_count , 'yesy')
#         # return render(request,'subadmin/subadmin_dashboard.html')
#         return render(request,'subadmin/subadmin_dashboard.html',{'subadmin_code':subadmin_code , 'client_count':client_count})
#     else:
#         messages.error(request, 'Pls Login')
#         return redirect('subadmin_login') 
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import sub_adminDT
from myapp.models import ClientDetail

from django.db.models import Q
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def subadmin_client_detail(request):
    if 'subadmin_id' not in request.session:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')

    subadmin_id = request.session.get('subadmin_id')

    try:
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
    except sub_adminDT.DoesNotExist:
        messages.error(request, 'Sub-admin not found.')
        return redirect('subadmin_login')

    # Fetch all clients linked to the sub-admin
    clients = ClientDetail.objects.filter(sub_admin_id=subadmin_id)

    # Search and date range filters
    search_query = request.GET.get('search', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    if search_query:
        clients = clients.filter(
            Q(name_first__icontains=search_query) |
            Q(name_last__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if from_date and to_date:
        clients = clients.filter(created_at__range=[from_date, to_date])

    # PDF download
    if 'download_pdf' in request.GET:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.setFillColor(colors.green)
        pdf.drawString(100, height - 50, "Client List")

        # Table Header
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(colors.white)
        pdf.rect(50, height - 100, width - 100, 20, fill=1)
        pdf.setFillColor(colors.black)
        pdf.drawString(60, height - 90, "S.No")
        pdf.drawString(120, height - 90, "Full Name")  # Merged Full Name column
        pdf.drawString(320, height - 90, "Email")
        pdf.drawString(420, height - 90, "Phone Number")
        pdf.drawString(520, height - 90, "Status")

        y_position = height - 120  # Starting position for client rows

        # Table Content
        pdf.setFont("Helvetica", 10)
        for index, client in enumerate(clients, start=1):
            pdf.setFillColor(colors.black)
            pdf.drawString(60, y_position, str(index))

            # Merged Full Name Column
            full_name = f"{client.name_first} {client.name_last}"
            pdf.drawString(120, y_position, full_name)

            pdf.drawString(200, y_position, client.email)
            pdf.drawString(420, y_position, client.phone_number)
            pdf.drawString(520, y_position, client.account_type)
            y_position -= 20

            if y_position < 50:  # Start a new page if space runs out
                pdf.showPage()
                y_position = height - 50  # Reset y position for new page

        pdf.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'subadmin/subadmin_clients.html', {
        'clients': clients,
        'subadmin_code': subadmin_code,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date
    })



# ====================== edit_client =========================


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from myapp.forms import SubadminClientUpdateForm


def edit_client(request, user_id):
    if 'subadmin_id' in request.session:
        subadmin_id = request.session.get('subadmin_id')
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        
        # Fetch the client using user_id
        client = get_object_or_404(ClientDetail, user_id=user_id)
        
        if request.method == 'POST':
            form = SubadminClientUpdateForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, 'Client details updated successfully.')
                return redirect('subadmin_client_detail')
        else:
            form = SubadminClientUpdateForm(instance=client)
        
        return render(request, 'subadmin/edit_client.html', {'form': form, 'subadmin_code': subadmin_code})
    else:
        messages.error(request, 'Please Login')
        return redirect('subadmin_login')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import ClientDetail
from .models import sub_adminDT
from django.utils.timezone import now  # To get the current date and time

# def sub_client_status(request):
#     subadmin_id = request.session.get('subadmin_id')
#     if subadmin_id:
#         try:
#             subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
#             client = ClientDetail.objects.filter(sub_admin_id=subadmin_id)
#             st = ClientStatus.objects.filter(sub_admin_id=subadmin_id).order_by('-id')
#             today = now()  # Get the current date and time
#             return render(request, 'subadmin/client_status.html', {
#                 'client': client,
#                 'st': st,  
#                 'subadmin_code': subadmin_code,
#                 'today': today  # Pass current date to template
#             })
#         except sub_adminDT.DoesNotExist:
#             messages.error(request, 'Subadmin does not exist.')
#             return redirect('subadmin_login')
#     else:
#         messages.error(request, 'Please log in.')
#         return redirect('subadmin_login')
   
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO


def sub_client_status(request):
    subadmin_id = request.session.get('subadmin_id')
    if not subadmin_id:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')

    try:
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        client = ClientDetail.objects.filter(sub_admin_id=subadmin_id)
        st = ClientStatus.objects.filter(sub_admin_id=subadmin_id).order_by('-id')

        # Filters
        search_query = request.GET.get('search', '')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if search_query:
            st = st.filter(
                Q(name__icontains=search_query) |
                Q(clint_email__icontains=search_query) |
                Q(clint_phone_number__icontains=search_query)
            )

        if from_date and to_date:
            st = st.filter(time__range=[from_date, to_date])

        # PDF Download
        if 'download_pdf' in request.GET:
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            pdf.drawString(100, 800, "Filtered Client Status Report")
            y = 750

            for status in st:
                pdf.drawString(50, y, f"ID: {status.id}, Name: {status.name}, Email: {status.clint_email}, Phone: {status.clint_phone_number}")
                y -= 20
                if y < 50:  # Start a new page if space runs out
                    pdf.showPage()
                    y = 800

            pdf.save()
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf')

        today = now()
        return render(request, 'subadmin/client_status.html', {
            'client': client,
            'st': st,
            'subadmin_code': subadmin_code,
            'today': today,
            'search_query': search_query,
            'from_date': from_date,
            'to_date': to_date
        })
    except sub_adminDT.DoesNotExist:
        messages.error(request, 'Subadmin does not exist.')
        return redirect('subadmin_login')


def generate_pdf(st_queryset):
    # Generate a PDF from the filtered queryset
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, "Client Status Report")
    y = 750

    for status in st_queryset:
        pdf.drawString(50, y, f"ID: {status.id}, Name: {status.name}, Time: {status.time}")
        y -= 20
        if y < 50:  # Start a new page if space runs out
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Client_Status_Report.pdf"'
    return response 


# ==============================================================kyc=================================================

''' ============================ signup and KYC method start =============================  '''
''' ============================ signup and KYC method start =============================  '''
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import ClientDetail, GROUP
from .models import sub_adminDT
import random

def subadmin_client_registration(request):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        groups = GROUP.objects.all()
        strategies = Strategy.objects.all() 

        if request.method == "POST":
            # Fetch data from the form
            c_fname = request.POST.get('fname')
            c_lname = request.POST.get('lname')
            c_mno = request.POST.get('mobile')
            c_email = request.POST.get('email')
            password = request.POST.get('pwd')
            license_duration = int(request.POST.get('license_duration'))  # Get license duration as an integer
            # c_from_date = request.POST.get('fromdate')
            # c_last_date = request.POST.get('todate')

            # Generate a 6-digit OTP
            code = get_random_string(6, allowed_chars='0123456789')

            # Check client limit
            client_count = ClientDetail.objects.filter(sub_admin_id=subadmin_id).count()
            client_limit = subadmin_code.subadmin_client_limit.max_quantity

            if client_limit >= client_count:
                # Check if email is already registered
                if ClientDetail.objects.filter(email=c_email).exists():
                    return render(request, 'subadmin/subadmin_register.html', {
                        'msg': 'Email already registered',
                        'groups': groups,
                        'strategies': strategies,
                        'subadmin_code': subadmin_code
                    })
                    
                # Calculate the last_login based on the selected license duration
                current_date = datetime.now()
                last_login_date = current_date + timedelta(days=license_duration)    

                # Create and save the client instance
                client_instance = ClientDetail.objects.create(
                    # user_active=False,
                    name_first=c_fname,
                    name_last=c_lname,
                    email=c_email,
                    password=password,
                    phone_number=c_mno,
                    date_joined=current_date.strftime('%Y-%m-%d'),
                    last_login=last_login_date.strftime('%Y-%m-%d'),
                    verify_code=code,
                    sub_admin_id=subadmin_id 
                )

                # Send registration email with OTP and login details
                subject = 'Welcome to Algo Finoways - Your Login Details and OTP'
                message = f"""
Dear {c_fname} {c_lname},

Welcome to Algo Finoways! Below are your login details:

Login Email: {c_email}
Password: {password}

Your OTP for account verification is: {code}

Please enter this OTP on the verification page to complete your registration.

Login URL: https://algo.finoways.com/

Regards,  
Algo Finoways Team
"""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [c_email]

                try: 
                    send_mail(subject, message, email_from, recipient_list)
                    request.session['client_email'] = c_email  # Store email in session
                    return redirect('register_verify')  # Redirect to OTP verification page
                except Exception as e:
                    messages.error(request, 'Failed to send OTP email. Please try again.')
                    return redirect('subadmin_client_registration')
            else:
                return render(request, 'subadmin/subadmin_register.html', {
                    'msg': 'Client registration limit reached',
                    'groups': groups,
                    'strategies': strategies, 
                    'subadmin_code': subadmin_code
                })

        return render(request, 'subadmin/subadmin_register.html', {
            'groups': groups,
            'strategies': strategies,
            'subadmin_code': subadmin_code 
        })
    else:  
        messages.error(request, 'Please log in')
        return redirect('subadmin_login')

# ========================================================================================
# ==============================   subadmin kyc process   ================================
# ========================================================================================

''' =============================subadmin  Email verify ============================================='''

def register_verify(request):
    # return render(request,'register_verify.html',)
    subadmin_email = request.session.get('subadmin_email')
    print(f' otp = {subadmin_email}')
    try:
        subadmin_user = sub_adminDT.objects.get(subadmin_email=subadmin_email)
        if request.method == 'POST':     
            code = request.POST.get('code')
            print(code)
            if subadmin_user.verify_code == code:
             #   return HttpResponse('otp verfiy ')
                return redirect('upload_national_id')
            else:
                return render(request,'register_verify.html',{'msg':'The verification code in incorrect.'})
        #return redirect('/cpanel/?msg=Your email address is already registered')
        
    except ObjectDoesNotExist:  
        print('error')
        return render(request,'register_verify.html',{'msg':'user not in'})
      #  return redirect('/verify/')
    print('run last')
    return render(request,'register_verify.html',{'msg':f'The verification code in {subadmin_email}.'})



# def subadmin_client_registration(request):
#     subadmin_id = request.session.get('subadmin_id')  # Check if subadmin is logged in
#     if subadmin_id:
#         try:
#             subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
#         except sub_adminDT.DoesNotExist:
#             messages.error(request, "Invalid sub-admin ID.")
#             return redirect('home')  # Redirect to a safe page if subadmin is invalid

#         error = ""
#         groups = GROUP.objects.all()  # Fetch all groups
       

#         if request.method == 'POST':
#             name_first = request.POST.get('name_first')
#             name_last = request.POST.get('name_last')
#             phone_number = request.POST.get('number')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             country = request.POST.get('country')
#             city = request.POST.get('city')
#             subadmin_id = request.POST.get('subadmin_id')
#             code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate OTP

#             # Check if the email already exists
#             if ClientDetail.objects.filter(email=email).exists():
#                 messages.error(request, 'Email is already registered.')
#                 return redirect('signup')

#             # Create a new client record
#             client_detail = ClientDetail(
#                 user_id=uuid.uuid4().hex[:8],
#                 name_first=name_first,
#                 name_last=name_last,
#                 email=email,
#                 password=password,
#                 phone_number=phone_number,
#                 country=country,
#                 city=city,
#                 subadmin_id=subadmin_id,
#                 date_joined=timezone.now(),
#                 last_login=timezone.now(),
#                 verify_code=code
#             )

#             subject = 'Hello! Verify your account'
#             message = f'Your verification code is: {code}'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [email]  # Send verification to the registered email

#             try:
#                 # Send the email with the OTP
#                 send_mail(subject, message, email_from, recipient_list)
#                 client_detail.save()  # Save the client record only if email is sent successfully
#                 request.session['client_email'] = client_detail.email  # Store email in session
#                 return redirect('verify')  # Redirect to verification page

#             except Exception as e:
#                 messages.error(request, f'OTP sending failed: {str(e)}')
#                 return redirect('signup')  # Handle OTP sending failure

#         return render(request, 'signup.html', {'groups': groups})

#     messages.error(request, 'Sub-admin not logged in. Please log in first.')
#     return redirect('home')  # Redirect to a safe page if sub-admin is not logged in

    
''' ============================= Email verify ============================================='''

# def register_verify(request):
#     # return render(request,'register_verify.html',)
#     email = request.session.get('client_email')
#     print(f' otp = {email}')
#     try:
#         user = ClientDetail.objects.get(email=email)
#         if request.method == 'POST':     
#             code = request.POST.get('code')
#             print(code)
#             if user.verify_code == code:
#              #   return HttpResponse('otp verfiy ')
#                 return redirect('upload_national_id')
#             else:
#                 return render(request,'register_verify.html',{'msg':'The verification code in incorrect.'})
#         #return redirect('/cpanel/?msg=Your email address is already registered')
        
#     except ObjectDoesNotExist:
#         print('error')
#         return render(request,'register_verify.html',{'msg':'user not in'})
#       #  return redirect('/verify/')
#     print('run last')
#     return render(request,'register_verify.html',{'msg':f'The verification code in {email}.'})
    
##############################################################################################












# logger = logging.getLogger(__name__)
# @csrf_protect
# def subadmin_client_registration(request):
#     subadmin_id = request.session.get('subadmin_id')
#     if subadmin_id:
#         subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
#         error = ""
#         groups = GROUP.objects.all()
#         strategies = Strategy.objects.all()  # Fetch all strategies
#         # brokers = Broker.objects.all()
        
#         if request.method == "POST":
#             c_fname = request.POST.get('fname')
#             c_lname = request.POST.get('lname')
#             c_mno = request.POST.get('mobile')
#             c_email = request.POST.get('email')
#             c_from_date = request.POST.get('fromdate')
#             c_last_date = request.POST.get('todate')
#             password = request.POST.get('pwd')
#             group_id = request.POST.get('group')
#             account_type = request.POST.get('Acount_type')
#             broker_id = request.POST.get('Broker')
#             api_key = request.POST.get('api_key', '')
#             secret_key = request.POST.get('secret_key', '')
#             app_id = request.POST.get('app_id')
#             client_id = request.POST.get('user_id', '')
#             demate_user_id = request.POST.get('demate_user_id', '')  # Use .get() with a default value
#             password_brokar = request.POST.get('password', '')
#             selected_strategies = request.POST.getlist('strategies', '')  # Fetch selected strategy IDs
#             UserID = request.POST.get('UserID', '')
#             App_Name = request.POST.get('App_Name', '')
#             App_Source = request.POST.get('App_Source', '')
#             User_Key = request.POST.get('User_Key', '')
#             ENCRYPTION_KEY = request.POST.get('ENCRYPTION_KEY', '')
            
#             client_count = ClientDetail.objects.filter(sub_admin_id=subadmin_id).count()
#             client_limit = subadmin_code.subadmin_client_limit.max_quantity

#             if client_limit >= client_count:
#                 try:
#                     # Check if email is already registered
#                     if ClientDetail.objects.filter(clint_email=c_email).exists():
#                         return render(request, 'subadmin/subadmin_register.html', {'msg': 'Email already registered', 'groups': groups, 'strategies': strategies, 'subadmin_code': subadmin_code})
                    
#                     Group = None
#                     if group_id:
#                         try:
#                             Group = GROUP.objects.get(id=group_id)
#                         except GROUP.DoesNotExist:
#                             return render(request, 'subadmin/subadmin_register.html', {'msg': 'Selected group does not exist', 'groups': groups,'strategies': strategies, 'subadmin_code': subadmin_code})
                    
#                     # Broker = None
#                     # if broker_id:
#                     #     try:
#                     #         Broker = Broker.objects.get(broker_name=broker_id)
#                     #     except Broker.DoesNotExist:
#                     #         return render(request, 'subadmin/subadmin_register.html', {'msg': 'Selected broker does not exist', 'groups': groups, 'brokers': brokers, 'strategies': strategies, 'subadmin_code': subadmin_code})

#                     # Send registration email
#                     subject = f'Dear {c_fname} {c_lname}'
#                     message = f"""Dear {c_fname} {c_lname},

#                     Thank you for choosing Algo Finoways for the Algo Platform. We are pleased to inform you that the password of your
#                     Algo Platform has been reset as per details mentioned below:

#                     Login Details:
#                     Email ID / User ID: {c_email}
#                     Login Password: {password}

#                     Note: Please change your login password as per your choice.

#                     Login URL: https://algo.finoways.com/
#                     """
#                     email_from = settings.EMAIL_HOST_USER
#                     recipient_list = [c_email]
#                     send_mail(subject, message, email_from, recipient_list)
                    
#                     # Create a new client record
#                     client_instance = ClientDetail.objects.create(
#                         clint_name_first=c_fname,
#                         clint_name_last=c_lname,
#                         clint_email=c_email,
#                         clint_password=password,
#                         clint_phone_number=c_mno,
#                         clint_date_joined=c_from_date,
#                         clint_last_login=c_last_date,
#                         client_Group=Group,
#                         clint_plane=account_type,
#                         broker=Broker,
#                         api_key=api_key,
#                         secret_key=secret_key,
#                         app_id=app_id,
#                         demate_user_id=demate_user_id,  # Using the default value or fetched value
#                         sub_admin_id=subadmin_id,
#                         client_id=client_id,
#                         password=password_brokar,
#                         UserID = UserID,
#                         App_Name = App_Name,
#                         App_Source =App_Source,
#                         User_Key = User_Key,
#                         ENCRYPTION_KEY = ENCRYPTION_KEY,
#                     )

#                     # Set the strategies using .set() method
#                     client_instance.strategies.set(selected_strategies)

#                     return redirect('subadmin_client_detail')
#                 except Exception as e:
#                     logger.error(f"Client registration failed: {e}")
#                     return render(request, 'subadmin/subadmin_register.html', {'msg': f'Error: {e}', 'groups': groups, 'strategies': strategies, 'subadmin_code': subadmin_code})
#             else:
#                 msg = "Client registration limit reached"
#                 return render(request, 'subadmin/subadmin_register.html', {'msg': msg, 'groups': groups, 'strategies': strategies, 'subadmin_code': subadmin_code})
  
#         return render(request, 'subadmin/subadmin_register.html', {'groups': groups,'strategies': strategies, 'subadmin_code': subadmin_code})
#     else:
#         messages.error(request, 'Please log in')
#         return redirect('subadmin_login')



def update_by_Subadmin(request,user_id):
    if 'subadmin_id' in request.session:
        subadmin_id = request.session.get('subadmin_id')
        subadmin_code = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        client_user = ClientDetail.objects.get(clint_id=user_id)
        client_user.updated_by = 'update by Subadmin' 
        client_user.save()    

        
        ClientStatus.objects.create(
            sub_admin_id = client_user.sub_admin_id,
            clint_id = user_id,
            name = f"{client_user.name_first} {client_user.name_last}" ,
            service_name = client_user.service_name,
            quantity = None,
            strategy = client_user.strategies,
            client_status = client_user.clint_status,
            trading =client_user.clint_plane,
            ip_address = client_user.ip_address,
            updated_by = 'update by Subadmin' ,
        )    
      
# from .models import ind_subadminDT

def subadmin_Registration(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('subadmin_name_first')
        last_name = request.POST.get('subadmin_name_last')
        email = request.POST.get('subadmin_email')
        phone_number = request.POST.get('subadmin_phone_number')
        password = request.POST.get('subadmin_password')
        client_limit_id = 1
        print('client_limit_id',client_limit_id)
        if sub_adminDT.objects.filter(subadmin_email=email).exists():
            messages.error(request, 'Your Email already registered.')
            return redirect('/sub/admin/?msg=Your Email already registered.')
        # Save data to the database
        try:
            subadmin = sub_adminDT(
                subadmin_name_first=first_name,
                subadmin_name_last=last_name,
                subadmin_email=email,
                subadmin_phone_number=phone_number,
                subadmin_password=password
            )
            subadmin.save()
            client_limit_instance = Subadmin_client_limit.objects.get(id=client_limit_id)  # Assuming client_limit_id is known
            subadmin.subadmin_client_limit = client_limit_instance

            subadmin.save() 
               # Save the form if the email is unique
            subject = f'Dear {first_name} {last_name}'
            message = f"""Dear {first_name} {last_name},

                    Thank you for choosing algo.Finoways for Algo Platform. We are pleased to inform you that the password of your
                    Algo sub admin Platform has been reset as per details mentioned below:

                    Login Details:
                    Email ID / User ID: {email}
                    Login Password: {password}

                    Note: Please change your login password as per your choice.

                    Login URL: https://algo.finoways.com/sub/admin/
                    """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            messages.error(request, 'Your Registration complete.')
            return redirect('/sub/admin/?msg=Your Registration complete.')
        except Exception as e:
            messages.error(request, 'Error somethin wrong.')
            return redirect('/sub/admin/?msg=Error somethin wrong.')

    return render(request, 'subadmin/Registration.html')


def subadmin_clients(request):
    
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        client = ClientDetail.objects.filter(sub_admin_id = subadmin_id)

        return render(request, 'subadmin/subadmin_clients.html', {'client': client}) 
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')    
    


def subadmin_offers(request):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        # client = ClientDetail.objects.filter(sub_admin_id = subadmin_id)
        client = ClientDetail.objects.all()
        # user_id = request.session.get('clint_id')
        client_user = sub_adminDT.objects.all()
        offer = offers_subadmin.objects.all()
        context = {
            'client_user': client_user,
            'offer':offer
           
        }
        return render(request, 'subadmin/sub_offers.html', context)

    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')  




  
# ==========================================================================
# ==========================================================================      

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import ClientPaymetns
from myapp.forms import ClientPaymetnsForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from myapp.models import ClientPaymetns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def payment_list(request):
    subadmin_id = request.session.get('subadmin_id')
    if not subadmin_id:
        messages.error(request, 'Please log in to view the payments.')
        return redirect('subadmin_login')

    # Fetch payments for the sub-admin
    payments = ClientPaymetns.objects.filter(sub_admin_id=subadmin_id)

    # Filters
    search_query = request.GET.get('search', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    if search_query:
        payments = payments.filter(
            Q(name_first__icontains=search_query) |
            Q(name_last__icontains=search_query) |
            Q(payer_email__icontains=search_query) |
            Q(payment_txn_id__icontains=search_query)
        )

    if from_date and to_date:
        payments = payments.filter(payment_date__range=[from_date, to_date])

    # PDF Generation
    if 'download_pdf' in request.GET:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.setFillColor(colors.green)
        pdf.drawString(50, height - 50, "Payment List for Sub-Admin")

        # Table Header
        headers = [
            "Client Name", "Payer Email", "Payer Mobile", "Payment TXN ID",
            "Payment Date", "Pay Amount", "Offer Discount", "Bill No",
            "Bill Date", "Plan Name", "Valid Plan Date", "Status"
        ]
        x_positions = [50, 150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150]
        pdf.setFont("Helvetica-Bold", 10)
        pdf.setFillColor(colors.white)
        pdf.rect(50, height - 70, width - 100, 20, fill=1)
        pdf.setFillColor(colors.black)
        for i, header in enumerate(headers):
            pdf.drawString(x_positions[i], height - 60, header)

        # Table Rows
        y_position = height - 90
        pdf.setFont("Helvetica", 9)
        for payment in payments:
            data = [
                f"{payment.name_first} {payment.name_last}",
                payment.payer_email,
                payment.payer_mobile,
                payment.payment_txn_id,
                payment.payment_date.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_date else "N/A",
                str(payment.pay_amount),
                str(payment.offer_discount),
                payment.bill_no,
                payment.bill_date.strftime('%Y-%m-%d %H:%M:%S') if payment.bill_date else "N/A",
                payment.plan_name,
                payment.valid_plan_date.strftime('%Y-%m-%d %H:%M:%S') if payment.valid_plan_date else "N/A",
                payment.get_status_display(),  # Use `get_status_display` to fetch human-readable value
            ]

            for i, value in enumerate(data):
                pdf.drawString(x_positions[i], y_position, str(value)[:20])  # Truncate long values if necessary
            y_position -= 20

            if y_position < 50:
                pdf.showPage()
                y_position = height - 50
                pdf.setFont("Helvetica-Bold", 10)
                for i, header in enumerate(headers):
                    pdf.drawString(x_positions[i], height - 60, header)

        pdf.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'subadmin/subadmin_payment_list.html', {
        'payments': payments,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date
    })


# def payment_list(request):
#     # Retrieve the logged-in sub-admin ID from the session
#     subadmin_id = request.session.get('subadmin_id')
    
#     if subadmin_id:
#         # Fetch payments related to the logged-in sub-admin
#         payments = ClientPaymetns.objects.filter(sub_admin_id=subadmin_id)
#         return render(request, 'subadmin/subadmin_payment_list.html', {'payments': payments})
#     else:
#         messages.error(request, 'Please log in to view the payments.')
#         return redirect('subadmin_login')

 

    
def payment_add(request):
    if 'subadmin_id' not in request.session:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')
    subadmin_id = request.session.get('subadmin_id')
    
    if subadmin_id:
        if request.method == 'POST':
            form = ClientPaymetnsForm(request.POST, request.FILES)
            if form.is_valid():
                # form.save()
                customer = form.save(commit=False)
                print(subadmin_id)
                customer.sub_admin_id = subadmin_id
                customer.save()
                return redirect('payment_list')  # Redirect to the payment list view
        else:
            form = ClientPaymetnsForm()
        return render(request, 'subadmin/subadmin_payment_form.html', {'form': form, 'action': 'Add'})
    else:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')

def payment_edit(request, pk):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        payment = get_object_or_404(ClientPaymetns, pk=pk)
        if request.method == 'POST':
            form = ClientPaymetnsForm(request.POST, request.FILES, instance=payment)
            if form.is_valid():
                form.save()
                return redirect('payment_list')  # Redirect to the payment list view
        else:
            form = ClientPaymetnsForm(instance=payment)
        return render(request, 'subadmin/subadmin_payment_form.html', {'form': form, 'action': 'Edit'})
    else:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')

def payment_delete(request, pk):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        payment = get_object_or_404(ClientPaymetns, pk=pk)
        if request.method == 'POST':
            payment.delete()
            return redirect('payment_list')
        return render(request, 'subadmin/subadmin_payment_confirm_delete.html', {'payment': payment})
    else:
        messages.error(request, 'Please log in.')
        return redirect('subadmin_login')


def update_revenue_and_earnings(subadmin_id, revenue):
    try:
        subadmin = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        # Update total revenue
        subadmin.total_revenue += revenue
        # Update earnings
        subadmin.update_earnings()
    except sub_adminDT.DoesNotExist:
        print("Sub-admin not found")

from django.http import JsonResponse


def update_revenue_and_earnings_view(request):
    # Get parameters from the GET request
    subadmin_id = request.GET.get('subadmin_id')
    revenue = request.GET.get('revenue')

    # Validate inputs
    if not subadmin_id or not revenue:
        return JsonResponse({'error': 'subadmin_id and revenue are required'}, status=400)

    try:
        revenue = float(revenue)  # Ensure revenue is a valid number
        update_revenue_and_earnings(subadmin_id, revenue)
        return JsonResponse({'status': 'success', 'message': 'Revenue and earnings updated successfully'})
    except ValueError:
        return JsonResponse({'error': 'Invalid revenue value'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from weasyprint import HTML
from datetime import datetime
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages

def earning_list(request):
    # Retrieve the logged-in sub-admin ID
    subadmin_id = request.session.get('subadmin_id')

    if subadmin_id:  
        # Fetch related payments and sub-admin details
        subadmin = sub_adminDT.objects.filter(subadmin_id=subadmin_id).first()
        earnings = ClientPaymetns.objects.filter(sub_admin_id=subadmin_id)

        # Filter by date range if provided
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                earnings = earnings.filter(payment_date__range=(from_date, to_date))
            except ValueError:
                messages.error(request, "Invalid date format.")

        # Calculate total revenue for the filtered results
        total_revenue = sum(payment.pay_amount or 0 for payment in earnings)
        subadmin.total_revenue = total_revenue
        subadmin.update_earnings()

        if 'download_pdf' in request.GET:  # Handle PDF download
            html_content = render_to_string('subadmin/earnings_pdf_template.html', {
                'earnings': earnings,
                'subadmin': subadmin,
            })
            pdf_file = HTML(string=html_content).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="earnings.pdf"'
            return response

        return render(request, 'subadmin/subadmin_earnings_list.html', {
            'earnings': earnings,
            'subadmin': subadmin,   
            'from_date': request.GET.get('from_date', ''),
            'to_date': request.GET.get('to_date', ''),
        })
    else:
        messages.error(request, 'Please log in to view the earnings.')
        return redirect('subadmin_login')


from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail  # Required for forgot password email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import sub_adminDT
import uuid


def subadmin_change_password(request):
    try:
        subadmin_id = request.session.get('subadmin_id')
        if not subadmin_id:
            return redirect('subadmin_login')

        subadmin_user = sub_adminDT.objects.get(subadmin_id=subadmin_id)
        if request.method == "POST":
            current_password = request.POST['currentpassword']
            new_password = request.POST['newpassword']
            confirm_password = request.POST['confirmpassword']

            if subadmin_user.subadmin_password == current_password:
                if new_password == confirm_password:
                    subadmin_user.subadmin_password = new_password
                    subadmin_user.save()
                    messages.success(request, "Password changed successfully!")
                    return redirect('subadmin_logout')
                else:
                    messages.error(request, "New password and confirm password do not match!")
            else:
                messages.error(request, "Current password is incorrect!")

        return render(request, 'subadmin/subadmin_change_password.html', locals())
    except sub_adminDT.DoesNotExist:
        messages.error(request, "Sub-admin not found!")
        return redirect('subadmin_login')


def subadmin_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            subadmin_user = sub_adminDT.objects.get(subadmin_email=email)
            reset_code = str(uuid.uuid4().hex[:6])
            subadmin_user.subadmin_verify_code = reset_code
            subadmin_user.save()

            # Send reset code to email
            send_mail(
                'Password Reset Request',
                f'Your reset code is: {reset_code}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Reset code sent to your email!")
            return redirect('subadmin_verify_reset')
        except sub_adminDT.DoesNotExist:
            messages.error(request, "Email not registered!")
    
    return render(request, 'subadmin/subadmin_forgot_password.html')


def subadmin_verify_reset(request):
    if request.method == "POST":
        reset_code = request.POST.get('reset_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            subadmin_user = sub_adminDT.objects.get(subadmin_verify_code=reset_code)
            if new_password == confirm_password:
                subadmin_user.subadmin_password = new_password
                subadmin_user.subadmin_verify_code = None
                subadmin_user.save()
                messages.success(request, "Password reset successfully!")
                return redirect('subadmin_login')
            else:
                messages.error(request, "New password and confirm password do not match!")
        except sub_adminDT.DoesNotExist:
            messages.error(request, "Invalid reset code!")

    return render(request, 'subadmin/subadmin_verify_reset.html')
   



##############################################################################################


# '''  ===================================  Document verified ====================================='''

# last finl

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .models import sub_adminDT, SUBKYC
import pytesseract
import fitz  # PyMuPDF for handling PDF
from PIL import Image
from fuzzywuzzy import fuzz

# Tesseract path setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from PDF file
def pdf_to_images(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def extract_text_from_images(images):
    text = ""
    for img in images:
        extracted_text = pytesseract.image_to_string(img)
        text += extracted_text + "\n"
    return text

# Function to extract text from PDF directly
def extract_text_from_pdf(pdf_file):
    images = pdf_to_images(pdf_file)
    extracted_text = extract_text_from_images(images)
    return extracted_text

# Function to normalize extracted text
def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)  # Remove special characters
    return text.strip().lower()  # Convert to lower case and strip whitespace

def subadmin_upload_national_id(request):
    subadmin_email = request.session.get('subadmin_email')
    if not subadmin_email:
        messages.error(request, "Email is missing from the session. Please login again.")
        return redirect('/')

    subadmin_user, created = sub_adminDT.objects.get_or_create(
        subadmin_email=subadmin_email,
        defaults={'date_joined': timezone.now(), 'last_login': timezone.now()},
    )
    subkyc, created = SUBKYC.objects.get_or_create(subadmin_id=subadmin_user)

    if request.method == 'POST':
        form = SUBAdminNationalIDForm(request.POST, request.FILES, instance=subkyc)
        if form.is_valid():
            subadmin_national_id_file = form.cleaned_data.get('subadmin_national_id', None)

            # Check if the file is provided
            if subadmin_national_id_file:
                subadmin_national_id_name = form.cleaned_data['subadmin_national_id_name']
                subadmin_national_id_number = form.cleaned_data['subadmin_national_id_number']

                file_extension = subadmin_national_id_file.name.split('.')[-1].lower()
                extracted_text = ""

                # Check for supported file types
                if file_extension == 'pdf':
                    extracted_text = extract_text_from_pdf(subadmin_national_id_file)
                elif file_extension in ['jpeg', 'jpg', 'png']:
                    extracted_text = pytesseract.image_to_string(Image.open(subadmin_national_id_file))
                else:
                    messages.error(request, "Invalid file format. Please upload a PDF or an image.")
                    return render(request, 'subadmin/upload_national_id.html', {'form': form})

                # Normalize and match extracted text
                normalized_text = normalize_text(extracted_text)
                combined_input = f"{subadmin_national_id_name} {subadmin_national_id_number}".lower()
                match_ratio = fuzz.token_set_ratio(combined_input, normalized_text)

                # Check if the match ratio is sufficient
                if match_ratio >= 0:  # You can adjust this threshold
                    form.save()
                    messages.success(request, "ID uploaded successfully!")
                    return redirect('subagreement_view')  # Replace with the next URL
                else:
                    messages.error(request, f"ID does not match uploaded document. Match ratio: {match_ratio}%")
            else:
                messages.error(request, "No national ID file uploaded. Please upload a file.")
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = SUBAdminNationalIDForm()

    return render(request, 'subadmin/upload_national_id.html', {'form': form})


#####################################################################################################    
''' ============================= upload_national_id 2st============================================='''

#####################################################################################################  

##############################################################################################
''' ============================= agreement accept ==================================='''
# views.py
from .forms import SUBAdminAgreementForm
from xhtml2pdf import pisa

def subagreement_view(request):
    subadmin_email = request.session.get('subadmin_email')
    if not subadmin_email:
        return redirect('kyc_start')  # Redirect if email is missing

    try:
        subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
        subadmin_kyc = SUBKYC.objects.get(subadmin_id=subadmin_client)  # Corrected foreign key
    except ObjectDoesNotExist:
        return redirect('kyc_start')

    if request.method == 'POST':
        form = SUBAdminAgreementForm(request.POST)
        if form.is_valid():
            subadmin_kyc.subadmin_agreement_signed = form.cleaned_data['subadmin_agreement_signed']
            subadmin_kyc.subadmin_terms_accepted = form.cleaned_data['subadmin_terms_accepted']

            # Generate and save the PDF
            context = {'client': subadmin_client, 'kyc': subadmin_kyc}
            html = render_to_string('subadmin/agreement.html', context)
            pdf_file = ContentFile(b"")  # Create an empty content file
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)

            if not pisa_status.err:  # Save the PDF if no errors occurred
                file_name = f"agreement_{subadmin_client.id}.pdf"
                subadmin_kyc.subadmin_agreement_file.save(file_name, pdf_file)

            subadmin_kyc.save()
            return redirect('subadmin_video_verification_view')  # Redirect to the next step
    else:
        form = SUBAdminAgreementForm()

    context = {'form': form, 'client': subadmin_client}
    return render(request, 'subadmin/agreement.html', context)


# def subagreement_view(request):
#     subadmin_email = request.session.get('subadmin_email')
#     if not subadmin_email:
#         return redirect('kyc_start')  # Redirect if the email is missing

#     subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
#     subadmin_kyc = SUBKYC.objects.get(subadmin_client=subadmin_client)

#     if request.method == 'POST':
#         form = SUBAdminAgreementForm(request.POST)
#         if form.is_valid():
#             subadmin_kyc.subadmin_agreement_signed = form.cleaned_data['subadmin_agreement_signed']
#             subadmin_kyc.subadmin_terms_accepted = form.cleaned_data['subadmin_terms_accepted']

#             # Generate and save the PDF
#             context = {
#                 'client': subadmin_client,
#                 'kyc': subadmin_kyc,
#             }
#             html = render_to_string('subadmin/agreement.html', context)
#             pdf_file = ContentFile(b"")  # Create an empty content file
#             pisa_status = pisa.CreatePDF(html, dest=pdf_file)

#             if not pisa_status.err:  # Save the PDF if no errors occurred
#                 file_name = f"agreement_{subadmin_client.id}.pdf"
#                 subadmin_kyc.subadmin_agreement_file.save(file_name, pdf_file)

#             subadmin_kyc.save()
#             return redirect('video_verification')  # Redirect to the next step
#     else:
#         form = SUBAdminAgreementForm()

#     context = {
#         'form': form,
#         'client': subadmin_client,
#     }
#     return render(request, 'subadmin/agreement.html', context)

# import pdfkit
# from django.template.loader import render_to_string
# from django.http import HttpResponse
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import sub_adminDT, SUBKYC

def subadmin_download_pdf(request):
    # Configure pdfkit with the correct path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Get the subadmin email from the session
    subadmin_email = request.session.get('subadmin_email')
    if not subadmin_email:
        return HttpResponse('Subadmin email is not set in session', status=400)

    try: 
        # Get the subadmin client information
        subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)

        # Ensure that you are using the correct ForeignKey field in SUBKYC
        subadmin_kyc = SUBKYC.objects.get(subadmin_id=subadmin_client)  # Replace with the correct ForeignKey field

        # Build the context for rendering the HTML
        base_url = request.build_absolute_uri('/')[:-1]
        context = {
            'client': subadmin_client,
            'kyc': subadmin_kyc,
            'base_url': base_url,
        }

        # Render the HTML content
        html = render_to_string('subadmin/agreement.html', context)

        # Create an HTTP response with the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="agreement.pdf"'

        # Generate the PDF from the HTML
        pdf = pdfkit.from_string(
            html,
            output_path=False,
            configuration=config,
            options={
                'page-size': 'A4',
                'enable-local-file-access': 'True',  # Set to 'True' or remove this line
            },
        )

        # Write the PDF to the response
        response.write(pdf)
        return response

    except sub_adminDT.DoesNotExist:
        return HttpResponse('Subadmin not found', status=404)
    except SUBKYC.DoesNotExist:
        return HttpResponse('KYC not found for the subadmin', status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


# import pdfkit
# def subadmin_download_pdf(request):
#     # Configure pdfkit with the correct path to wkhtmltopdf
#     config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

#     subadmin_email = request.session.get('subadmin_email')
#     subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
#     subadmin_kyc = SUBKYC.objects.get(subadmin_client=subadmin_client)

#     base_url = request.build_absolute_uri('/')[:-1]

#     context = {
#         'client': subadmin_client,
#         'kyc': subadmin_kyc,
#         'base_url': base_url,
#     }

#     html = render_to_string('subadmin/agreement.html', context)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="agreement.pdf"'

#     pdf = pdfkit.from_string(
#         html,
#         output_path=False,
#         configuration=config,
#         options={
#             'page-size': 'A4',
#             'enable-local-file-access': None,
#         },
#     )
#     response.write(pdf)
#     return response

''' ============================= video uplod ==================================='''


import os
from django.shortcuts import render
from moviepy.editor import VideoFileClip  # Ensure this line is present
import speech_recognition as sr
from fuzzywuzzy import fuzz
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Before extracting audio
logging.info("Extracting audio from video...")
from moviepy.editor import VideoFileClip

KYC_TEXT = 'akshay ak'


''' ============================= video uplod ==================================='''

''' ============================= video uplod ==================================='''
from django.core.files.base import ContentFile
import subprocess
import tempfile
import base64
import json
from django.http import JsonResponse
from django.conf import settings
from speech_recognition import Recognizer, AudioFile
import speech_recognition as sr
from pydub import AudioSegment
import os
import moviepy.editor
from fuzzywuzzy import fuzz
from django.contrib import messages
from .models import sub_adminDT, SUBKYC

def subadmin_video_verification_view(request):
    subadmin_email = request.session.get('subadmin_email')
    if not subadmin_email:
        return JsonResponse({'success': False, 'error': 'Subadmin email not found in session.'})

    try:
        # Fetch subadmin details
        subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
        # Ensure KYC exists for the subadmin
        kyc_obj = SUBKYC.objects.get(subadmin_id=subadmin_client)
    except sub_adminDT.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Subadmin not found.'})
    except SUBKYC.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'KYC record not found for this subadmin.'})

    # Prepare the text to compare with
    text_to_compare = f"I, {subadmin_client.subadmin_name_first} {subadmin_client.subadmin_name_last}, confirm that I have read understood and accept all terms and conditions."

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_base64 = data.get('video')

            if video_base64:
                # Decode the video base64 data
                format, video_str = video_base64.split(';base64,')
                video_data = base64.b64decode(video_str)

                # Save the video temporarily
                with tempfile.NamedTemporaryFile(suffix='.webm', dir=settings.MEDIA_ROOT, delete=False) as temp_video_file:
                    temp_video_file.write(video_data)
                    video_path = temp_video_file.name

                # Save video to the database
                video_d = ContentFile(video_data, name=f'{subadmin_client.subadmin_name_first}_kyc_video.{format.split("/")[-1]}')
                kyc_obj.subadmin_video_file = video_d
                kyc_obj.subadmin_video_verification_done = False  # Initially set to False
                kyc_obj.save()

                # Extract audio from the video
                audio_path = extract_audio_from_video(video_path, subadmin_client.subadmin_name_first)
                if not audio_path:
                    return JsonResponse({'success': False, 'error': 'Error extracting audio from video.'})

                # Convert audio to text
                extracted_text = transcribe_audio_to_text(audio_path)

                # Compare extracted text with predefined text
                match_ratio = fuzz.token_set_ratio(extracted_text, text_to_compare)

                # If the match ratio is high enough, mark verification as successful
                if match_ratio > 10:  # Threshold for a successful match
                    kyc_obj.subadmin_video_verification_done = True
                    kyc_obj.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': 'Audio did not match the expected text.'})
            else:
                return JsonResponse({'success': False, 'error': 'Video data not found.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'subadmin/video_verification.html', {'text': text_to_compare})

# def video_verification_view(request):
#     subadmin_email = request.session.get('subadmin_email')
#     subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
#    # text_to_compare = 'I confirm that this is a KYC submission.'
#     text_to_compare = f"I, {subadmin_client.subadmin_name_first} {subadmin_client.subadmin_name_last}, confirm that I have read understood and accept all terms and conditions."


#     if request.method == 'POST':
#         try:
#             subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)
#             data = json.loads(request.body)
#             video_base64 = data.get('video')

#             if video_base64:

#                 f , video_s = video_base64.split(';base64,')
#                 e = f.split('/')[-1]
#                 video_d = ContentFile(base64.b64decode(video_s), name=f'{subadmin_client.subadmin_name_first}kyc_video{subadmin_client.subadmin_id}.{e}')
#                 video_p = os.path.join('path_to_save', video_d.name)  # Set the path to save the video
                
#                 # Save video to the database
#                 kyc_obj = SUBKYC.objects.get(client__user_id=subadmin_client.subadmin_id)
#                 kyc_obj.subadmin_video_file = video_d
#                 kyc_obj.subadmin_video_verification_done = False  # Initially set to False
#                 kyc_obj.save()
#                 # Decode the base64 video
#                 format, video_str = video_base64.split(';base64,')
#                 video_data = base64.b64decode(video_str)
                
#                 # Save the video temporarily in the MEDIA_ROOT directory
#                 with tempfile.NamedTemporaryFile(suffix='.webm', dir=settings.MEDIA_ROOT, delete=False) as temp_video_file:
#                     temp_video_file.write(video_data)
#                     video_path = temp_video_file.name

#                 # Step 1: Extract audio directly from WebM video using ffmpeg
#                 audio_path = extract_audio_from_video(video_path, subadmin_client.subadmin_name_first)
#                 if not audio_path:
#                     messages.success(request, "Error extracting audio from video.")

#                     return JsonResponse({'success': False, 'error': 'Error extracting audio from video.'})

#                 # Step 2: Convert the audio to text
#                 extracted_text = transcribe_audio_to_text(audio_path)
#                 print(f'Extracted Text: {extracted_text}')
#                 print(f'Text to Compare: {text_to_compare}')

#                 # Step 3: Compare extracted text with predefined text
#                 from fuzzywuzzy import fuzz
#                 match_ratio = fuzz.token_set_ratio(extracted_text, text_to_compare)
#                 print(f'Fuzzy match ratio: {match_ratio}')

#                 # Step 4: If match ratio is above a threshold (e.g., 90)
#                 if match_ratio > 5:
#                     # KYC verification successful
#                     kyc_obj = SUBKYC.objects.get(client__user_id=subadmin_client.subadmin_id)
#                     kyc_obj.subadmin_video_verification_done = True
#                     kyc_obj.save()

#                     return JsonResponse({'success': True})
#                 else:
#                     messages.success(request, "Audio did not match the expected text.")
#                     return JsonResponse({'success': False, 'error': 'Audio did not match the expected text.'})

#             else:
#                 messages.success(request, "Video data not found.")
#                 return JsonResponse({'success': False, 'error': 'Video data not found.'})
#         except Exception as e:
#             messages.success(request, "Error .")
#             return JsonResponse({'success': False, 'error': str(e)})

#     else:
#         return render(request, 'subadmin/video_verification.html', {'text': text_to_compare})


# Function to extract audio from a video and convert it to MP3 using moviepy
def extract_audio_from_video(video_path , name):
    # Normalize the path (handle backslashes and forward slashes)
    video_path = os.path.normpath(video_path)  # This will convert the path correctly based on the OS
    
    print(f' video_path = {video_path}')
    print(f' name = {name}')
    
    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist!")
        return None
    
    # Video ka extension check karna
    try:
        file_extension = os.path.splitext(video_path)[1]  # Extension extract karna
        directory = os.path.dirname(video_path)
        
        if file_extension != '.mp4':
            print(f'File extension is {file_extension}, converting to .mp4 is required')
            # Add conversion to mp4 logic here if needed
        else:
            print("Video is already in .mp4 format.")
        
        # Video se audio extract karna
        video = moviepy.editor.AudioFileClip(video_path)
        print(f'Video file loaded successfully: {video}')

        # Audio file ka path define karna
     #   audio_path = os.path.join(directory, f"{name}.mp3")
        audio_path = os.path.join(directory, f"{name}.wav")

        print('----start extracting audio----')
        video.write_audiofile(audio_path)
        print(f'Audio saved at: {audio_path}')
        print('----end----')

        return audio_path
    except Exception as e:
        # Print the exception for debugging
        print(f"Error occurred: {e}")
        return None




# Speech ko text mein convert karna
def transcribe_audio_to_text(audio_path):
    wav_file =audio_path # convert_mp3_to_wav(audio_path)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        print("Audio file load ho raha hai...")
        audio_data = recognizer.record(source)  # Puri file ko read karega
        print("Speech recognition process shuru ho raha hai...")
        try:
            text = recognizer.recognize_google(audio_data)  # Google speech recognition API ka use karte hain
            print("Text Conversion successful!")
            return text
        except sr.UnknownValueError:
            print("Speech ko samajhne mein error hai!")
        except sr.RequestError as e:
            print(f"Google API request mein problem hai: {e}")



############################################################################################################################
############################################################################################################################
############################################################################################################################

def subadmin_submit_kyc(request):
    subadmin_email = request.session.get('subadmin_email')

    # Redirect to the first step if the subadmin_email is missing
    subadmin_client = sub_adminDT.objects.get(subadmin_email=subadmin_email)

    try:
        subadmin_kyc = SUBKYC.objects.get(subadmin_id=subadmin_client)
    except SUBKYC.DoesNotExist:
        # Handle case where the SUBKYC record does not exist
        messages.error(request, "KYC record does not exist.")
        return redirect('video_verification')

    if subadmin_kyc.subadmin_agreement_signed and subadmin_kyc.subadmin_terms_accepted and subadmin_kyc.subadmin_video_verification_done:
        # KYC process completed, show a confirmation or send an email if required
        subadmin_client.subadmin_active = True
        subadmin_client.subadmin_Term_condition = True
        subadmin_client.save()

        subject = 'Hello send verify Completed!'
        message = f'Verification Completed'
        email_from = settings.EMAIL_HOST_USER
        subadmin_email = [subadmin_email]  # Add recipient email addresses here
        send_mail(subject, message, email_from, subadmin_email)

        messages.success(request, "KYC verified and Signup successfully!")
        return render(request, 'subadmin/kyc_completed.html')

    return redirect('video_verification')  # Redirect back to the start if KYC not completed



import logging
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib import messages
from .models import sub_adminDT  # Adjust your import path for the model

logger = logging.getLogger(__name__)

def update_login_info(request, subadmin_id, status):
    """
    Update the subadmin's IP address and login information.

    :param request: Django request object.
    :param subadmin_id: ID of the subadmin.
    :param status: Status to update.
    """
    try:
        # Get subadmin instance by ID
        subadmin = sub_adminDT.objects.get(subadmin_id=subadmin_id)

        # Update IP address using the get_client_ip function
        subadmin.subadmin_ip_address = get_client_ip(request)

        # Update additional fields
        subadmin.panel_last_login = now()  # Assuming you have this field in your model
        subadmin.subadmin_status = status
        subadmin.updated_by = request.user.username if request.user.is_authenticated else "System"

        # Save the updates to the database
        subadmin.save()

        logger.info(f"Updated login info for subadmin {subadmin_id}.")
        print('Update saved:', status)
    except sub_adminDT.DoesNotExist:
        logger.error(f"Subadmin with ID {subadmin_id} does not exist.")
    except Exception as e:
        logger.error(f"Error in update_login_info: {e}")
        print(f"Error in update_login_info: {e}")


def get_client_ip(request):
    """
    Get the IP address of the client making the request.

    :param request: Django request object.
    :return: IP address as a string.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    return ip    
