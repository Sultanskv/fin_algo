from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import ClientDetail, Client_SYMBOL_QTY, SYMBOL
from myapp.serializer import ClientDetailSerializer
from django.utils import timezone

from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

AudioSegment.converter = "C:\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"

@api_view(['POST'])
def registrationapi(request):
    if request.method == 'POST':
        serializer = ClientDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            client = serializer.save()

            # Send the email
            subject = 'Your Email and Password'
            message = f'Name: {client.name_first} {client.name_last}\nEmail: {client.email}\nPassword: {client.password}\nPhone: {client.phone_number}'
            email_from = settings.EMAIL_HOST_USER
            client_email = [client.email]

            try:
                send_mail(subject, message, email_from, client_email)
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Registration successful and email sent!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def client_login_api(request):
#     serializer = ClientLoginSerializer(data=request.data)
    
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
        
#         try:
#             # Fetch the user by email
#             user = ClientDetail.objects.get(email=email)
            
#             # Check if the provided password matches the user's password
#             if password == user.password:
#                 request.session['user_id'] = user.user_id
#                 if user.user_active:
#                     # Set the session user_id
#                     request.session['user_id'] = user.user_id

#                     # Check if the last login date is today or later
#                     if user.last_login and user.last_login.date() >= timezone.now().date():
#                         # Initialize symbols for the user
#                         initialize_client_symbols(user)

#                         # Fetch all symbols
#                         alls = SYMBOL.objects.all()

#                         for s in alls:
#                             # Check if the symbol already exists for the user
#                             signals, created = Client_SYMBOL_QTY.objects.get_or_create(
#                                 client_id=user.user_id,
#                                 SYMBOL=s.SYMBOL,
#                                 defaults={'QUANTITY': 0}
#                             )

#                         return Response({'message': 'Login successful', 'redirect': '/Analysis/'}, status=status.HTTP_200_OK)
#                     else:
#                         return Response({'message': 'Your plan has expired', 'redirect': '/'}, status=status.HTTP_403_FORBIDDEN)  
#                 else:
#                     # Redirect with an expiry message if the plan has expired
#                     request.session['client_email'] = user.email
#                     return Response({'message': 'Account not active, please upload your national ID'}, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({'message': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        
#         except ClientDetail.DoesNotExist:
#             return Response({'message': 'Email not registered'}, status=status.HTTP_404_NOT_FOUND)
        
#         except Exception as e:
#             # Log the exception and respond with a generic error message
#             print(e)
#             return Response({'message': 'An error occurred. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     # If the serializer is not valid, return the errors
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.shortcuts import render,redirect , HttpResponse
from .forms import ClientLogin,ClientDetailForm
from .forms import *
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from myapp.models import ClientDetail , ClientSignal
from django.utils import timezone    
import datetime
from django.contrib import messages
from algosms import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.dateparse import parse_date
import pandas as pd

# Create your views here.
my_global_variable = None
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def logoutAdmin(request):
    if 'cadmin_id' in request.session:
        del request.session['cadmin_id']
    logout(request)
    return redirect('admin_login')

def logoutUser(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        client_user = ClientDetail.objects.filter(user_id=user_id).first()
        # Call your panel_login function
        panel_login(request, user_id, 'Algo off')
        # Update login information with logout details
        update_login_info(request, user_id, 'Client Log out')
        # Perform any client-specific updates
        update_by_client(request)
        del request.session['user_id']
    else:
        client_user = None

    logout(request)
    # You can pass client_user to the template if needed, but typically on logout you just redirect.
    return redirect('client_login')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')  # Replace with your desired redirect
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')

def client_base(request):
    user_id = request.session.get('user_id')
    if user_id:
        client_user = ClientDetail.objects.filter(user_id=user_id).first()
        if client_user:
            return render(request, 'client_base.html', {'client_user': client_user})
        else:
            # Handle the case where the client user is not found
            return redirect('client_login')
    else:   
        return redirect('client_login')



from django.contrib.auth.decorators import login_required

# @login_required
# def client_dashboard(request):
#     # Your view logic here
#     return render(request, 'client_dashboard.html')

# from django.utils import timezone

# from django.shortcuts import render, redirect
# from .models import ClientDetail, Client_SYMBOL_QTY, SYMBOL
# from django.utils import timezone
# from django.contrib import messages

# def client_login(request):
#     msg = request.GET.get('msg', None)
    
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             user = ClientDetail.objects.get(email=email)
            
#             if password == user.password:
#                 if user.user_active:
#                     request.session['user_id'] = user.user_id
                    
#                     # Log panel status and update login info
#                     panel_login(request, user.user_id, 'Algo on')
#                     update_login_info(request, user.user_id, 'Client Log in')
#                     update_by_client(request)

#                     if user.last_login and user.last_login.date() >= timezone.now().date():
#                         initialize_client_symbols(user)

#                         alls = SYMBOL.objects.all()
#                         for s in alls:
#                             Client_SYMBOL_QTY.objects.get_or_create(
#                                 client_id=user.user_id,
#                                 SYMBOL=s.SYMBOL,
#                                 defaults={'QUANTITY': 0}
#                             )

#                         return redirect('/Analysis/')
#                     else:
#                         return redirect('/?msg=Your plan has expired')  

#                 else:
#                     request.session['client_email'] = user.email
#                     return redirect('upload_national_id')

#             else:
#                 return redirect('/?msg=Wrong password')

#         except ClientDetail.DoesNotExist:
#             return redirect('/?msg=Email not registered')
#         except Exception as e:
#             print(f"Error during login: {e}")
#             return redirect('/?msg=An error occurred. Please try again.')
    
#     return render(request, 'client_login.html', {'msg': msg})

from django.utils import timezone

from django.shortcuts import render, redirect
from .models import ClientDetail, Client_SYMBOL_QTY, SYMBOL
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import ClientDetail, Client_SYMBOL_QTY, SYMBOL
from django.utils import timezone
from django.contrib import messages

def client_login(request):
    msg = request.GET.get('msg', None)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = ClientDetail.objects.get(email=email)
            
            if password == user.password:
                # Check if the sub_admin_user_activate is True
                if user.sub_admin_user_active:  # Check if sub-admin has activated the user
                    if user.user_active:
                        request.session['user_id'] = user.user_id
                    
                    
                        # Log panel status and update login info
                        panel_login(request, user.user_id, 'Algo on')
                        update_login_info(request, user.user_id, 'Client Log in')
                        update_by_client(request)

                        if user.last_login and user.last_login.date() >= timezone.now().date():
                            initialize_client_symbols(user)

                            alls = SYMBOL.objects.all()
                            for s in alls:
                                Client_SYMBOL_QTY.objects.get_or_create(
                                    client_id=user.user_id,
                                    SYMBOL=s.SYMBOL,
                                    defaults={'QUANTITY': 0}
                                )

                            return redirect('/Analysis/')
                        else:
                            return redirect('/?msg=Your plan has expired')  
                   
                    else:
                        request.session['client_email'] = user.email
                        return redirect('upload_national_id')
            
                else:
                        return redirect('/?msg=Your account is not activated by the admin.') 
            else:
                return redirect('/?msg=Wrong password') 

        except ClientDetail.DoesNotExist:
            return redirect('/?msg=Email not registered')
        except Exception as e:
            print(f"Error during login: {e}")
            return redirect('/?msg=An error occurred. Please try again.')
    
    return render(request, 'client_login.html', {'msg': msg})


# def client_login(request):
#     # Handle any message passed in the URL (e.g., from a redirect)
#     msg = request.GET.get('msg', None)

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             # Fetch the user by email
#             user = ClientDetail.objects.get(email=email)
            
#             # Check if the provided password matches the user's password
#             if password == user.password:
#                 # Set the session user_id
#                 if user.user_active == True:
#                     request.session['user_id'] = user.user_id
                   
#                     # Log panel status and update login info
#                     panel_login(request, user.user_id, 'Panel on')
#                     update_login_info(request, user.user_id, 'Client Log in')
#                     update_by_client(request)
#                     # Check if last login date is today or later
#                     if user.last_login and user.last_login.date() >= timezone.now().date():
                       
#                         # Initialize symbols for the user
#                         initialize_client_symbols(user)

#                         # Fetch all symbols
#                         alls = SYMBOL.objects.all()

#                         for s in alls:
#                             # Check if the symbol already exists for the user
#                             signals, created = Client_SYMBOL_QTY.objects.get_or_create(
#                                 client_id=user.user_id,
#                                 SYMBOL=s.SYMBOL,
#                                 defaults={'QUANTITY': 0}
#                             )

#                         return redirect('/Analysis/')
#                     else:
#                         return redirect('/?msg=Your plan has expired')  

                        
#                 else:
#                     # Redirect with an expiry message if the plan has expired
#                     request.session['client_email'] = user.email
#                     return redirect('upload_national_id')
#             else:
#                 # Redirect with a wrong password message if the password doesn't match
#                 return redirect('/?msg=Wrong password') 
#         except ClientDetail.DoesNotExist:
#             # Redirect with an error message if the email is not registered
#             return redirect('/?msg=Email not registered')    
#         except Exception as e:
#             # Log the exception and redirect with a generic error message
#             print(e)
#             return redirect('/?msg=An error occurred. Please try again.')

#     # Render the login page with any messages
#     return render(request, 'client_login.html', {'msg': msg})



# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time

# MAX_CONCURRENT_LOGINS = 3  # Limit the number of concurrent logins

# def login_mt5_account(login, password, server):
#     if not mt5.initialize():
#         return f"Client {login}: initialize() failed, error code = {mt5.last_error()}"

#     if not mt5.login(login=login, password=password, server=server):
#         error_code = mt5.last_error()
#         mt5.shutdown()
#         return f"Client {login}: Login failed, error code: {error_code}"

#     # Keep the connection alive or handle your trading logic here
#     # mt5.shutdown() # Uncomment if you want to logout after each operation

#     return f"Client {login}: Login successful"

# def batch_login(accounts):
#     login_results = []

#     with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_LOGINS) as executor:
#         futures = []

#         for account in accounts:
#             login, password, server = account['login'], account['password'], account['server']
#             futures.append(executor.submit(login_mt5_account, login, password, server))
#             time.sleep(0.1)  # Introduce a slight delay between login attempts

#         for future in as_completed(futures):
#             result = future.result()
#             login_results.append(result)
#             print(result)

#     return login_results

# def login_multiple_accounts(request):
#     clients = ClientDetail.objects.filter(mt5_login__isnull=False)
    
#     accounts = [
#         {"login": client.mt5_login, "password": client.mt5_password, "server": client.mt5_server}
#         for client in clients
#     ]
    
#     # Process logins in batches
#     login_results = batch_login(accounts)

#     # Return results or render a template to display login statuses
#     return render(request, 'login_results.html', {'login_results': login_results})

@login_required
def admin_dashboard(request):
    # For cards on dashboard
    clientcount = ClientDetail.objects.all().count()
    
    # For recent order tables
    total_live_account = ClientDetail.objects.filter(clint_status='live').count()
    total_demo_account = ClientDetail.objects.filter(clint_status='demo').count()
    total_licence = ClientDetail.objects.filter(clint_status='licence').count()
    total_2days_service = ClientDetail.objects.filter(clint_status='2days_service').count()
    
    active_live_account = ClientDetail.objects.filter(clint_status='active_live').count()
    active_demo_account = ClientDetail.objects.filter(clint_status='active_demo').count()
    remaining_licence = ClientDetail.objects.filter(clint_status='remaining_licence').count()
    active_2days_service = ClientDetail.objects.filter(clint_status='active_2days_service').count()
    
    expired_total_account = ClientDetail.objects.filter(clint_status='expired_live').count()
    expired_demo_account = ClientDetail.objects.filter(clint_status='expired_demo').count()
    used_licence = ClientDetail.objects.filter(clint_status='used_licence').count()
    total_converted_accounts = ClientDetail.objects.filter(clint_status='converted').count()

    mydict = {
        'clientcount': clientcount,
        'total_live_account': total_live_account,
        'total_demo_account': total_demo_account,
        'total_licence': total_licence,
        'total_2days_service': total_2days_service,
        'active_live_account': active_live_account,
        'active_demo_account': active_demo_account,
        'remaining_licence': remaining_licence,
        'active_2days_service': active_2days_service,
        'expired_total_account': expired_total_account,
        'expired_demo_account': expired_demo_account,
        'used_licence': used_licence,
        'total_converted_accounts': total_converted_accounts,
    }
    
    return render(request, 'admin_dashboard.html', context=mydict)


       

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils import timezone
scheduler = BackgroundScheduler()

# Function to create attendance records for employees
@transaction.atomic
def symbol_inactive():
    timezone.activate('Asia/Kolkata')
    ss = Client_SYMBOL_QTY.objects.all()
    for s in ss:
        s.trade = None
        s.save()       
# Set the job to run every day at 12:00 AM
# scheduler.add_job(symbol_inactive, 'cron', hour=0, minute=1)
# scheduler.start()


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"  
        except:
            error = "yes"          
    return render(request,'admin_login.html', locals()) 


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def create_superuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                User.objects.create_superuser(username=username, email=email, password=password1)
                return redirect('admin_login')
                # return HttpResponse('Superuser created successfully!')
            except:
                return HttpResponse('Error creating superuser. Please try again.')
        else:
            return HttpResponse('Passwords do not match. Please try again.')
    else:
        return render(request, 'admin_register.html')
    
    
def admin_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return render(request, 'change_password.html', {'msg': 'Password updated successfully', 'error': 'no'})
            else:
                return render(request, 'change_password.html', {'msg': 'New Password and Confirm Password fields do not match', 'error': 'yes'})
        else:
            return render(request, 'change_password.html', {'msg': 'Your current password is wrong', 'error': 'not'})
    else:
        return render(request, 'change_password.html', {})    


# =====================================================================================

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import ClientDetail

@login_required
def registration(request):
    if request.method == "POST":
        # Fetch basic fields
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pwd = request.POST.get('pwd')
        from_date = request.POST.get('fromdate')
        to_date = request.POST.get('todate')

        # Fetch optional fields
        selected_option = request.POST.get('selected_option', 'M')
        forex_option = request.POST.get('forex_option') == 'True'
        comex_option = request.POST.get('comex_option') == 'True'
        singapore = request.POST.get('Singapore') == 'True'
        bursa_malaysia = request.POST.get('Bursa_Malaysia') == 'True'
        us30 = request.POST.get('US30') == 'True'
        hk100 = request.POST.get('HK100') == 'True'
        
        # Optional MT5 fields (can be blank)
        MataApi_ACCOUNT_ID = request.POST.get('MataApi_ACCOUNT_ID', None)
        MataApi_TOKEN = request.POST.get('MataApi_TOKEN', None)
        MataApi_account_link = request.POST.get('MataApi_account_link', None)         
        user_active = request.POST.get('user_active', None)      

        try:
            # Check if email already exists
            if ClientDetail.objects.filter(email=email).exists():
                return render(request, 'register.html', {'msg': 'Email already registered'})

            # Create the client record
            ClientDetail.objects.create(
                name_first=fname,
                name_last=lname,
                email=email,
                password=pwd,
                phone_number=phone,
                date_joined=from_date,
                last_login=to_date,
                selected_option=selected_option,
                forex_option=forex_option,
                comex_option=comex_option,
                Singapore=singapore,
                Bursa_Malaysia=bursa_malaysia,
                US30=us30,
                HK100=hk100,
                MataApi_ACCOUNT_ID=MataApi_ACCOUNT_ID if MataApi_ACCOUNT_ID else None,
                MataApi_TOKEN=MataApi_TOKEN if MataApi_TOKEN else None,
                MataApi_account_link=MataApi_account_link if MataApi_account_link else None,
                user_active=user_active if user_active else None,
                
            )

            # Send confirmation email
            subject = 'Account Registration Successful'
            message = f'Dear {fname},\n\nYour account has been successfully registered.'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [email])

            return redirect('/')
        except Exception as e:
            return render(request, 'register.html', {'msg': f'Error: {e}'})

    # Pass OPTIONS to the template
    context = {
        'ClientDetail_OPTIONS': ClientDetail.OPTIONS,
    }
    return render(request, 'register.html', context)


from xhtml2pdf import pisa
from datetime import datetime

def client_list(request):
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    search_query = request.GET.get('search_query', '')

    filtered_clients = ClientDetail.objects.all()

    if search_query:
        filtered_clients = filtered_clients.filter(
            Q(name_first__icontains=search_query) |
            Q(name_last__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if from_date and to_date:
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
        filtered_clients = filtered_clients.filter(date_joined__range=[from_date_obj, to_date_obj])

    if not filtered_clients.exists():
        # Handle case where no clients match the filters
        return HttpResponse("No clients found matching the given criteria.")

    return render(request, 'client_list.html', {
        'clientdetail': filtered_clients,
        'from_date': from_date,
        'to_date': to_date,
        'search_query': search_query
    })

def client_list_pdf(request):
    # Get filter parameters
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    search_query = request.GET.get('search_query', '')

    # Query all clients initially
    filtered_clients = ClientDetail.objects.all()

    # Apply search query filter (if any)
    if search_query:
        filtered_clients = filtered_clients.filter(
            Q(name_first__icontains=search_query) |
            Q(name_last__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    # Apply date range filter (if both dates are provided)
    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            filtered_clients = filtered_clients.filter(date_joined__range=[from_date_obj, to_date_obj])
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD format.")

    # Check if any clients match the filter
    if not filtered_clients.exists():
        return HttpResponse("No clients found matching the given criteria.")

    # Render PDF
    template_path = 'client_pdf.html'
    context = {'clientdetail': filtered_clients}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors with generating the PDF.')
    return response


def update_client(request, user_id):
    # Retrieve the symbol object from the database
    clientdetail = get_object_or_404(ClientDetail, user_id=user_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = ClientDetailForm(request.POST, instance=clientdetail)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('client_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = ClientDetailForm(instance=clientdetail)
    
    return render(request, 'update_clientdetail.html', {'form': form, 'clientdetail': clientdetail})


def delete_client(request, user_id):
    clientdetail = ClientDetail.objects.get(user_id=user_id)
    if request.method == 'POST':
        clientdetail.delete()
        return redirect('client_list')  # Redirect to the symbol list page after deletion
    return render(request, 'delete_clientdetail.html', {'clientdetail': clientdetail})


#  ====================== client_view =========================
def client_view(request,user_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
        return redirect('/admin/?msg=Login')
    request.session['user_id'] = user_id
    return redirect('Analysis')
# ============================================Admin  ==========================================
# =============================================================================================

# Function to handle admin messages
import random
import string


def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import ClientMessage, ClientDetail, Notification
import requests

@login_required
def admin_message(request):
    """
    Admin sends an advisory message to clients based on selected options (Forex or Comex).
    """
    error = ""

    if request.method == "POST":
        # Get the advisory message and selected options from POST data
        advisory_message = request.POST.get('message')
        forex_selected = 'forex' in request.POST  # Check if Forex is selected
        comex_selected = 'comex' in request.POST
        Singapore = 'singapore' in request.POST
        Bursa_Malaysia = 'busra malaysia' in request.POST
        US30 = 'us30' in request.POST
        HK100 = 'hk100' in request.POST

        # Determine advisory type
        advisory_type = None
        if forex_selected:
            advisory_type = 'Forex'
        elif comex_selected:
            advisory_type = 'Comex'
        elif Singapore:
            advisory_type = 'Singapore'
        elif Bursa_Malaysia:
            advisory_type = 'Bursa Malaysia'
        elif US30:
            advisory_type = 'US30'
        elif HK100:
            advisory_type = 'HK100'

        # Fetch all active clients
        clients = ClientDetail.objects.filter(user_active=True)

        # Filter clients by selected options
        if forex_selected:
            clients = clients.filter(forex_option=True)
        if comex_selected:
            clients = clients.filter(comex_option=True)

        if clients.exists():
            # Telegram Bot Configuration
            TELEGRAM_BOT_TOKEN = "7962728912:AAGhrXga50OhMbnBvx4Jw_YUTKi79seFdoI"
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

            for client in clients:
                # Save the advisory message in the database
                ClientMessage.objects.create(
                    user=request.user,
                    client=client,
                    message=advisory_message,
                    advisory_type=advisory_type
                )

                Notification.objects.create(
                    client=client,
                    message=advisory_message
                )

                # Prepare message text
                msg_text = f"Advice: {advisory_message} (Type: {advisory_type})"

                # Send Email
                # if client.email:
                #     try:
                #         send_mail(
                #             subject="New Advisory Message",
                #             message=msg_text,
                #             from_email=settings.EMAIL_HOST_USER,
                #             recipient_list=[client.email],
                #             fail_silently=True
                #         )
                #     except Exception as e:
                #         print(f"Email error for {client.email}: {e}")

                # Send Telegram Message
                if hasattr(client, 'telegram_chat_id') and client.telegram_chat_id:
                    telegram_data = {
                        "chat_id": client.telegram_chat_id,  # Client's Telegram chat ID
                        "text": msg_text
                    }
                    try:
                        response = requests.post(telegram_url, json=telegram_data)
                        if response.status_code != 200:
                            print(f"Telegram error for {client.telegram_chat_id}: {response.text}")
                    except Exception as e:
                        print(f"Telegram error for {client.telegram_chat_id}: {e}")

            # Success message
            error = f"Advisory message sent to all active clients successfully!"
        else:
            error = f"No active clients found for the selected options."

    return render(request, 'admin_messages.html', {'error': error})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notification, ClientDetail, ClientMessage
from datetime import date

def client_advisory(request):
    """
    Display advisory messages for the client, even if they are not logged in.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please log in to view your advisory messages.")
        return redirect('client_login')

    try:
        client_user = ClientDetail.objects.get(user_id=user_id)
    except ClientDetail.DoesNotExist:
        messages.error(request, "Client not found. Please log in again.")
        return redirect('client_login')

    # Get the current date
    today = date.today()

    # Filter messages for the current date and client selected_option
    advisory_messages = ClientMessage.objects.filter(
        client=client_user,
        created_at__date=today
    ).order_by('-created_at')

    # Get unread notifications count only if the user is authenticated
    unread_notifications_count = 0
    if request.session.get('user_id'):
        try:
            client = ClientDetail.objects.get(user_id=request.session['user_id'])
            unread_notifications_count = Notification.objects.filter(client=client, is_read=False).count()
        except ClientDetail.DoesNotExist:
            unread_notifications_count = 0


    return render(request, 'client_advisory.html', {
        'client_user': client_user,
        'messages': advisory_messages,
        'unread_notifications_count': unread_notifications_count
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClientMessage

@csrf_exempt
def mark_read(request, message_id):
    """
    Mark a specific message as read.
    """
    if request.method == "POST" and request.session.get('user_id'):
        try:
            # Fetch the message for the logged-in client
            message = ClientMessage.objects.get(
                id=message_id,
                client__user_id=request.session.get('user_id')
            )
            # Update the message's read status
            message.read = True
            message.save()
            return JsonResponse({"success": True})
        except ClientMessage.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)
    return JsonResponse({"error": "Unauthorized"}, status=401)

from django.utils.timezone import now
from django.http import JsonResponse
from .models import Notification, ClientDetail

def fetch_client_notifications(request):
    """
    Fetch today's notifications for the logged-in client.
    """
    # Check if the client is logged in using `request.session`
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        # Verify the client exists
        client = ClientDetail.objects.get(user_id=user_id)

        # Filter notifications for the client and today's date
        today = now().date()
        notifications = Notification.objects.filter(
            client=client,  # Use the `client` field instead of `user`
            created_at__date=today  # Only today's notifications
        ).order_by('-created_at')

        # Prepare data for JSON response
        notifications_data = [
            {
                'id': notification.id,
                'message': notification.message,
                'is_read': notification.is_read,
                'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for notification in notifications
        ]
        return JsonResponse({'notifications': notifications_data})
    except ClientDetail.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)


def mark_client_notifications_read(request):
    """
    Mark all notifications for the logged-in client as read.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        client = ClientDetail.objects.get(user_id=user_id)
        Notification.objects.filter(client=client, is_read=False).update(is_read=True)  # Use `client`
        return JsonResponse({'success': True})
    except ClientDetail.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)

from django.http import JsonResponse
from django.utils.timezone import now
from .models import ClientMessage

def fetch_new_messages(request):
    """
    Fetch unread advisory messages for the current day and the logged-in client.
    """
    if request.session.get('user_id'):
        try:
            client_id = request.session.get('user_id')
            today = now().date()  # Get today's date
            # Fetch unread messages for the current client and created today
            messages = ClientMessage.objects.filter(
                client__user_id=client_id,
                created_at__date=today,  # Filter for today's date
                read=False  # Only unread messages
            ).order_by('-created_at')

            # Serialize messages
            messages_data = [
                {
                    'id': msg.id,
                    'message': msg.message,
                    'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'advisory_type': msg.advisory_type,
                }
                for msg in messages
            ]
            return JsonResponse({'messages': messages_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Unauthorized'}, status=401)

from django.http import JsonResponse
from django.utils.timezone import localtime

def fetch_new_message(request):
    if request.session.get('user_id'):
        try:
            client_id = request.session.get('user_id')
            unread_message = ClientMessage.objects.filter(client__user_id=client_id, read=False).order_by('-created_at').first()
            if unread_message:
                localized_time = localtime(unread_message.created_at).strftime('%Y-%m-%d %H:%M:%S')
                message_data = {
                    'id': unread_message.id,
                    'message': unread_message.message,
                    'created_at': localized_time,
                }
                return JsonResponse({'message': message_data})
            return JsonResponse({'message': None})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Unauthorized'}, status=401)

from django.http import JsonResponse
from .models import ClientMessage
from django.utils.timezone import now

def fetch_unread_messages(request):
    """
    Fetch unread advisory messages for the logged-in client.
    """
    if request.session.get('user_id'):
        try:
            client_id = request.session.get('user_id')
            # Fetch unread messages for the client
            unread_messages = ClientMessage.objects.filter(client__user_id=client_id, read=False).order_by('-created_at')
            messages_data = [
                {
                    'id': msg.id,
                    'message': msg.message,
                    'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for msg in unread_messages
            ]
            return JsonResponse({'messages': messages_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Unauthorized'}, status=401)



# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import TradeHistory, ClientDetail
from django.db.models import Q
from django.core.paginator import Paginator  # Correct import
from datetime import datetime

def admin_thistory(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    # Filter logic
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    client_id = request.GET.get('client_id', '')

    # Fetch trades and apply ordering
    trades = TradeHistory.objects.all().order_by('-signal_time')  # Descending order

    if client_id:
        trades = trades.filter(client__id=client_id)

    if search_query:
        trades = trades.filter(
            Q(client__name_first__icontains=search_query) |
            Q(client__name_last__icontains=search_query) |
            Q(symbol__icontains=search_query)
        )

    if start_date:
        trades = trades.filter(signal_time__date__gte=start_date)
    if end_date:
        trades = trades.filter(signal_time__date__lte=end_date)

    # Export to PDF logic
    if request.GET.get('export_pdf') == 'true':
        html_content = render_to_string('trade_history_pdf.html', {'trades': trades})
        pdf = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="trade_history.pdf"'
        return response

    # Paginate the trades queryset
    paginator = Paginator(trades, 10)  # Show 10 trades per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all clients for dropdown
    clients = ClientDetail.objects.all()

    return render(request, 'admin_thistory.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'clients': clients,
        'selected_client': client_id
    })

from django.shortcuts import render, redirect
from .models import TradeHistory, ClientDetail

def add_trade(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        signal_time = request.POST.get('signal_time')
        symbol = request.POST.get('symbol')
        trade_type = request.POST.get('trade_type')
        quantity = request.POST.get('quantity')
        entry_price = request.POST.get('entry_price')
        exit_time = request.POST.get('exit_time')
        exit_price = request.POST.get('exit_price')
        p_l = request.POST.get('p_l')

        # Create a new trade object
        TradeHistory.objects.create(
            client=ClientDetail.objects.get(id=client_id),
            signal_time=signal_time,
            symbol=symbol,
            trade_type=trade_type,
            quantity=quantity,
            entry_price=entry_price,
            exit_time=exit_time,
            exit_price=exit_price,
            p_l=p_l
        )

        return redirect('admin_thistory')

    return render(request, 'add_trade.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import TradeHistory

def edit_trade(request, trade_id):
    trade = get_object_or_404(TradeHistory, id=trade_id)

    if request.method == 'POST':
        # Update fields based on form data
        trade.signal_time = request.POST.get('signal_time')
        trade.exit_time = request.POST.get('exit_time')
        trade.symbol = request.POST.get('symbol')
        trade.trade_type = request.POST.get('trade_type')
        trade.quantity = request.POST.get('quantity')
        trade.entry_price = request.POST.get('entry_price')
        trade.exit_price = request.POST.get('exit_price')
        trade.p_l = request.POST.get('p_l')  # Update P & L
        trade.save()
        return redirect('admin_thistory')  # Redirect back to trade history

    return HttpResponseBadRequest("Invalid request method")

def delete_trade(request, trade_id):
    trade = get_object_or_404(TradeHistory, id=trade_id)
    if request.method == 'POST':
        trade.delete()
        return redirect('admin_thistory')
    return redirect('admin_thistory')

# def admin_tstatus(request):
#     return render(request,'admin_tstatus.html')
# -------------------------------------admin Status --------------------------------------------    
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ClientStatus
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def client_status_admin(request):
    # Retrieve parameters
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    export_pdf = request.GET.get('export_pdf', '')
    page_number = request.GET.get('page', 1)

    # Base queryset
    client_all = ClientStatus.objects.all()

    # Filter by search query across all fields
    if search_query:
        client_all = client_all.filter(
            Q(clint_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(clint_email__icontains=search_query) |
            Q(clint_phone_number__icontains=search_query) |
            Q(clint_plane__icontains=search_query) |
            Q(strategy__icontains=search_query) |
            Q(trading__icontains=search_query) |
            Q(ip_address__icontains=search_query) |
            Q(updated_by__icontains=search_query)
        )

    # Filter by date range if both start and end dates are provided
    if start_date and end_date:
        try:
            start_date_parsed = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_parsed = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            client_all = client_all.filter(time__range=[start_date_parsed, end_date_parsed])
        except ValueError:
            # Handle invalid date format
            start_date_parsed = None
            end_date_parsed = None

    # Export PDF if requested
    if export_pdf:
        return generate_pdf(client_all)

    # Paginate the clients queryset
    paginator = Paginator(client_all, 10)  # Show 10 clients per page
    page_obj = paginator.get_page(page_number)

    # Context for template rendering
    context = {
        'client_all': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'panel_on_clients': client_all.filter(panel_last_login__isnull=False),
        'broker_on_clients': client_all.filter(login_date_time__isnull=False),
        'page_obj': page_obj
    }
    
    return render(request, 'client_status_admin.html', context)

def generate_pdf(client_all):
    # Load the template
    template_path = 'client_status_pdf.html'
    context = {'client_all': client_all}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_status.pdf"'

    # Render the template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Return PDF
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def admin_client(request):
    return render(request,'admin_client.html')

# def admin_help_center(request):
#     return render(request,'admin_help_center.html')

from django.shortcuts import render, redirect
from .models import ClientDetail, Client_SYMBOL_QTY
from django.utils import timezone




# from django.shortcuts import render, redirect
# from .models import Client_SYMBOL_QTY, ClientDetail

# from django.contrib import messages

# def fetch_symbols(request):
#     if request.method == "POST":
#         if not mt5.initialize():
#             messages.error(request, "Failed to initialize MT5.")
#             return redirect('fetch_symbols')

#         symbols = mt5.symbols_get()
#         mt5.shutdown()

#         # Fetch all clients
#         all_clients = ClientDetail.objects.all()

#         for client in all_clients:
#             for symbol in symbols:
#                 # Check if the symbol exists for the client
#                 obj, created = Client_SYMBOL_QTY.objects.get_or_create(
#                     client_id=client.user_id,
#                     SYMBOL=symbol.name,
#                     defaults={
#                         'QUANTITY': 0.01,  # default quantity
#                         'trade': 'off'  # default trade flag
#                     }
#                 )

#                 # If the symbol is already created, we don't modify the QUANTITY or trade fields
#                 if not created:
#                     continue  # Skip if the symbol exists, to avoid overwriting updates

#         messages.success(request, "Symbols fetched and updated successfully for all clients!")
#         return redirect('client_dashboard')

#     return render(request, 'fetch_symbols.html')


from django.shortcuts import render, redirect
from .models import Client_SYMBOL_QTY, ClientDetail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def client_dashboard(request):
    # Get user_id from session
    user_id = request.session.get('user_id')
    
    # Check if the user_id is available in the session
    if not user_id:
        messages.error(request, "You are not logged in. Please log in first.")
        return redirect('client_login')  # Redirect to the login page if user_id is not found

    try:
        # Fetch the ClientDetail object for the logged-in user
        client_user = ClientDetail.objects.get(user_id=user_id)
    except ClientDetail.DoesNotExist:
        messages.error(request, "Client details not found. Please complete your registration.")
        return redirect('register')  # Redirect to a registration or error page

    # Ensure that the client has all the symbols initialized
    initialize_client_symbols(client_user)

    # Fetch symbols from the model for the specific client
    symbols = Client_SYMBOL_QTY.objects.filter(client_id=client_user.user_id).order_by('id')

    if request.method == "POST":
        for symbol in symbols:
            quantity = request.POST.get(f"QUANTITY{symbol.id}")
            trade_status = request.POST.get(f"TRADE{symbol.id}")  # Check if the trade checkbox is checked
            
            if quantity:
                symbol.QUANTITY = float(quantity)
            
            if trade_status:
                symbol.trade = 'on'
            else:
                symbol.trade = 'off'
            
            symbol.save()
            # Call your additional update functions after processing the form data
            # panel_login(request, client_user.user_id, 'Algo on')  # Log the panel login
            update_login_info(request, client_user.user_id, 'Client Update Qty or Trade')  # Update login information
            update_by_client(request)  # Perform any additional updates for the client

        messages.success(request, "Lot sizes and trading statuses updated successfully!")
        return redirect('client_dashboard')

    return render(request, 'client_dashboard.html', {'symbols': symbols, 'client_user': client_user})

def initialize_client_symbols(client_user):
    # List of predefined symbols
    prioritized_symbols = [
        "XAUUSDm", "USOILm", "EURUSDm", "EURGBPm", "GBPUSDm", 
        "USDJPYm", "CADUSDm", "AUDUSDm", "GBPAUDm", "BTCUSDm",
        "EURJPYm", "AUDNZDm", "GBPNZDm", "USDCHFm", "GBPCADm",
        "EURAUDm", "NZDUSDm", "USDCADm", "GBPJPYm", "AUDJPYm",
    ]

    for symbol in prioritized_symbols:
        # Only create the symbol if it doesn't exist already
        Client_SYMBOL_QTY.objects.get_or_create(
            client_id=client_user.user_id,
            SYMBOL=symbol,
            defaults={
                'QUANTITY': 0.01,  # Default quantity for new symbols
                'trade': 'off'  # Default trade flag
            }
        )



def add_singnal_qty(request):
    Client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    value = my_global_variable
    try:
        client_signal = ClientSignal.objects.get(ids= value) 
        for q in Client_symbol_qty:
            print('for tes qq', q.SYMBOL)
            print('for tes cc',client_signal.SYMBOL)
            print('for')
            if q.trade == 'on':
                print('on')    
                if str(q.SYMBOL) == str(client_signal.SYMBOL):
                    print('symbol')
                    print(q.SYMBOL)
                    print(client_signal.SYMBOL)
                    print('creat singnal')
                    creat = ClientSignal.objects.create(
                        user=client_signal.user,
                        SYMBOL=client_signal.SYMBOL,
                        TYPE=client_signal.TYPE,
                        ENTRY_PRICE=client_signal.ENTRY_PRICE,
                        ids = 'No',
                        QUANTITY=q.QUANTITY,
                        message_id = client_signal.message_id,
                        client_id = q.client_id,
                        created_at = timezone.now()
                    )

                    
        return HttpResponse('pass function')    
    except Exception as e:
        error = str(e)
        print(error)   
        return HttpResponse(f'error = {e}') 

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ClientSignal
from django.contrib import messages
from datetime import datetime, date
from django.http import HttpResponseNotFound

# client_signals client get method          
def client_signals(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        dt = {  
            "client_user": client_user ,        
            "s": signals_today,
        
        }
        return render(request, 'client_signals.html', dt)
    except:
        return redirect('client_login')
        
    
   
    
from django.db.models import Sum

def client_trade_history(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('created_at')
        # signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        # Calculate total profit and loss for today
        total_cumulative_pl = signals_today.aggregate(total_pl=Sum('cumulative_pl'))['total_pl']

        dt = {
            "client_user":client_user,
            "s": signals_today,
            "total_cumulative_pl": total_cumulative_pl
        }
        return render(request, 'client_thistory.html', dt)
    except:
        return redirect('client_login')




def change_password(request):
    try:
        #    print('test form' ) 
        user_id = request.session.get('user_id')
    
        client_user = ClientDetail.objects.get(user_id=user_id)
        if request.method == "POST":
            c = request.POST['currentpassword']
            n = request.POST['newpassword']
            f = request.POST['confirmpassword']

            if c == client_user.password and n == f:
                client_user.password = n
                client_user.save()
                return redirect('/?msg=chenge password')  
            else:
                return render(request,'client_change_password.html',{'msg':'samthing wrong'})    
        return render(request,'client_change_password.html',locals(),)       
    except:
        return redirect('client_login')        

  
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ClientDetail

# Forgot Password View
# Forgot Password View
def client_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            # Use 'email' instead of 'client_email'
            client_user = ClientDetail.objects.get(email=email)
            reset_code = str(uuid.uuid4().hex[:6])  # Generate a 6-digit reset code
            client_user.verify_code = reset_code  # Save reset code
            client_user.save()

            # Send reset code to email
            send_mail(
                'Password Reset Request',
                f'Your reset code is: {reset_code}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Reset code sent to your email!")
            return redirect('verify_reset')  # Redirect to verify reset page
        except ClientDetail.DoesNotExist:
            messages.error(request, "Email not registered!")
    
    return render(request, 'client_forgot_password.html')



# Verify Reset Code and Change Password View
# Verify Reset Code and Change Password View
def client_verify_reset(request):
    if request.method == "POST":
        verify_code = request.POST.get('reset_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            # Use 'verify_code' instead of 'client_verify_code'
            client_user = ClientDetail.objects.get(verify_code=verify_code)
            if new_password == confirm_password:
                client_user.password = new_password  # Update the password
                client_user.verify_code = None  # Clear the verify code after successful change
                client_user.save()
                messages.success(request, "Password reset successfully!")
                return redirect('client_login')  # Redirect to login page after password change
            else:
                messages.error(request, "New password and confirm password do not match!")
        except ClientDetail.DoesNotExist:
            messages.error(request, "Invalid reset code!")

    return render(request, 'client_verify_reset.html')


def admin_change_password(request):
    if not request.user.is_authenticated:
        return redirect('client_login')
    error = ""
    user = request.user
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"  
            else:
                error = "not"    
        except:
            error = "yes"
    return render(request,'admin_change_password.html',locals(),{'error': error}) 

@login_required
def Settings(request):
    return render(request,'settings.html')

# ===============================Symbolic qty =============================
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client_SYMBOL_QTY
from .forms import Client_SYMBOL_QTYForm

def create_client_symbol_qty(request):
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')  # Redirect to the list view
    else:
        form = Client_SYMBOL_QTYForm()
    return render(request, 'create_client_symbol_qty.html', {'form': form})

def client_symbol_qty_list(request):
    client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    return render(request, 'client_symbol_qty_list.html', {'client_symbol_qty': client_symbol_qty})

def edit_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST, instance=client_symbol_qty)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')
    else:
        form = Client_SYMBOL_QTYForm(instance=client_symbol_qty)
    return render(request, 'edit_client_symbol_qty.html', {'form': form})

def delete_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        client_symbol_qty.delete()
        return redirect('client_symbol_qty_list')
    return render(request, 'delete_client_symbol_qty.html', {'client_symbol_qty': client_symbol_qty})


# ========================== SYMBOL ====================================================

# =======================================================================================
from .forms import SymbolForm

def symbol_list(request):
    symbols = SYMBOL.objects.all()
    return render(request, 'symbol_list.html', {'symbols': symbols})

def create_symbol(request):
    if request.method == 'POST':
        form = SymbolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('symbol_list')
    else:
        form = SymbolForm()
    return render(request, 'create_symbol.html', {'form': form})

def update_symbol(request, symbol_id):
    # Retrieve the symbol object from the database
    symbol = get_object_or_404(SYMBOL, id=symbol_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = SymbolForm(request.POST, instance=symbol)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('symbol_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = SymbolForm(instance=symbol)
    
    return render(request, 'update_symbol.html', {'form': form, 'symbol': symbol})



def delete_symbol(request, symbol_id):
    symbol = SYMBOL.objects.get(id=symbol_id)
    if request.method == 'POST':
        symbol.delete()
        return redirect('symbol_list')  # Redirect to the symbol list page after deletion
    return render(request, 'delete_symbol.html', {'symbol': symbol})



# ==================================  Feedback=============================================

# =============================================================================== =======

from django.shortcuts import render, redirect
from .models import HelpMessage
from .forms import HelpMessageForm


def client_help_center(request):
    user_id = request.session.get('user_id')
    client_user = ClientDetail.objects.get(user_id=user_id)
    if not user_id:
        return redirect('client_login')  # Redirect to login if user_id is not in session

    try:
        client_detail = ClientDetail.objects.get(user_id=user_id)
    except ClientDetail.DoesNotExist:
        return redirect('client_login')  # Redirect to login if the client does not exist

    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            help_message = form.save(commit=False)
            help_message.user_id = client_detail  # Set the user_id field to the client_detail instance
            help_message.save()
            return redirect('client_help_center')  # Redirect to the same page or a thank you page
    else:
        form = HelpMessageForm()

    messages = HelpMessage.objects.filter(user_id=client_detail)

    return render(request, 'client_help_center.html', {'form': form, 'messages': messages,'client_user':client_user})

def admin_help_center(request):
    # Get the user_id from the session
    user_id = request.session.get('user_id')
    
    # If user_id is not found in the session, redirect to the admin login page
    if not user_id:
        return redirect('admin_login')
    
    # Check if the user is an admin (you might have a way to distinguish admins from clients)
    # For example, if admins have a specific role in your system:
    if not request.user.is_superuser:
        return redirect('admin_login')

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            # If form is valid, save the form data without associating it with any client
            help_message = form.save(commit=False)
            help_message.save()
            return redirect('admin_help_center')  # Redirect to the same page after form submission
    else:
        # If the request method is not POST, instantiate a new form
        form = HelpMessageForm()

    # Retrieve all HelpMessage objects (for admins, not associated with any client) in descending order by timestamp
    messages = HelpMessage.objects.all().order_by('-timestamp')

    # Render the admin_help_center.html template with the form and messages
    return render(request, 'admin_help_center.html', {'form': form, 'messages': messages})


# def client_tstatus(request):
#     return render(request,'client_tstatus.html')
import logging
logger = logging.getLogger(__name__)

def update_login_info(request,user_id,status):
   
    try:
        client = ClientDetail.objects.get(clint_id = user_id)
        client.ip_address = ClientDetail(request)
        # Set the last login and panel login timestamps to the current time
        client.panel_last_login = timezone.now()
        client.clint_status = status
        client.updated_by = status
        client.save()
        print('save update',status) 
    except Exception as e:
        print(f"Error in update_login_info: {e}")

def get_client_ip(request):
    # Check for IP address from different headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('HTTP_X_REAL_IP')
        if not ip:
            ip = request.META.get('REMOTE_ADDR')
    return ip

def panel_login(request, user_id, status):
    try:
        # Log the attempt
        logger.info(f"Attempting to update panel login for user_id: {user_id} with status: {status}")

        # Retrieve the client using the correct field (user_id)
        client = ClientDetail.objects.get(user_id=user_id)
        
        # Get client IP address
        client.ip_address = get_client_ip(request)
        logger.info(f"Client IP: {client.ip_address}")

        # Set the last login and panel login timestamps to the current time
        # client.last_login = timezone.now()
        client.panel_last_login = timezone.now()
        client.updated_by = status
        # Update client status
        client.clint_status = status

        # Save the updated client info to the database
        client.save()

        logger.info(f"Client {user_id} updated with status: {status}")
        print(f"Client {user_id} updated with status: {status}")

    except ClientDetail.DoesNotExist:
        logger.error(f"Client with user_id {user_id} not found")
        print(f"Client with user_id {user_id} not found")
    except Exception as e:
        logger.error(f"Error in panel_login: {e}")
        print(f"Error in panel_login: {e}")
        
        

def update_by_client(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)
        # symbol_qty = Client_SYMBOL_QTY.objects.get(client_id=user_id)
   

        ClientStatus.objects.create(
            sub_admin_id = client_user.sub_admin_id,
            clint_id = user_id,
            name = f"{client_user.name_first} {client_user.name_last}" ,
            clint_email = client_user.email,
            clint_phone_number =client_user.phone_number,
            quantity = None,
            panel_last_login = client_user.panel_last_login,
            strategy = client_user.selected_option,
            trading =client_user.clint_plane,
            ip_address = client_user.ip_address,
            updated_by =  client_user.updated_by ,
            client_status = client_user.clint_status,
        )
        print("")     
      

import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import ClientDetail, Client_SYMBOL_QTY, ClientStatus  # Import your models

logger = logging.getLogger(__name__)

def client_tstatus(request):
    # Check if user_id exists in session
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        logger.info(f"Client ID from session: {user_id}")
        
        try:
            # Fetch ClientDetail for the current user
            logger.info(f"Fetching ClientDetail for user ID {user_id}")
            client_user = ClientDetail.objects.get(user_id=user_id)
            logger.info(f"ClientDetail fetched: {client_user}")
            
            # Fetch all clients for the current user (assuming filtering by user_id)
            clients = ClientDetail.objects.filter(user_id=user_id)
            logger.info(f"Clients fetched for user ID {user_id}: {clients}")
            
            # Fetch Client_SYMBOL_QTY (assuming it's linked by client_id, adjust if necessary)
            logger.info(f"Fetching Client_SYMBOL_QTY for client ID {client_user.id}")
            client_symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=client_user.id).first()
            logger.info(f"Client_SYMBOL_QTY fetched: {client_symbol_qty}")
            
            # Fetch ClientStatus data for today only
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1) - timedelta(seconds=1)
            logger.info(f"Fetching ClientStatus for user ID {client_user.user_id} for today")
            st = ClientStatus.objects.filter(clint_id=client_user.user_id, time__range=(today_start, today_end)).order_by('-id')
            logger.info(f"ClientStatus fetched: {st}")
            
            # Check if ClientStatus exists
            if not st.exists():
                logger.warning(f"No ClientStatus found for user ID {user_id}")
                messages.error(request, 'No status data found for today.')
                return redirect('/')
            
            # Pass all data to the template
            context = {
                'client': clients,
                'client_user': client_user,
                'client_symbol_qty': client_symbol_qty,
                'st': st,
                'today': timezone.now().date()  # Today's date
            }
            logger.info("Rendering client_tstatus.html template")
            return render(request, 'client_tstatus.html', context)
        
        # Handle the case where the ClientDetail does not exist
        except ClientDetail.DoesNotExist:
            logger.error(f"ClientDetail.DoesNotExist for user ID {user_id}")
            messages.error(request, 'Client does not exist.')
            return redirect('/')
        
        # Catch any other exceptions and log full details
        except Exception as e:
            logger.error(f"Error in client_tstatus: {e}", exc_info=True)  # Log full stack trace
            messages.error(request, f"An error occurred: {str(e)}")  # Display the error for debugging
            return redirect('/')
    
    else:
        messages.error(request, 'Please log in.')
        return redirect('/')



def multibank(request):

    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                user_id = ClientDetail.objects.get(email=user.email)
                # Check if last login date is today or later
                if user.last_login.date() >= timezone.now().date():
                    request.session['user_id'] = user_id.user_id

                    alls = SYMBOL.objects.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.user_id , SYMBOL = s.SYMBOL)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.user_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.user_id,
                                SYMBOL = s.SYMBOL,
                                QUANTITY = q
                            )
                            

                    return redirect('/dashboard/')
                else:
                    return redirect('/?msg=your plane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
         #   return HttpResponse('email no register')
            return redirect('/?msg=Email no register') 
     
    return render(request,'multibank.html', {'msg':msg})


def client_report(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Get the start and end dates from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Default to today's date if no date is provided
        if not start_date:
            start_date = date.today().isoformat()
        if not end_date:
            end_date = date.today().isoformat()

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        # Filter signals within the date range and order them by created_at in descending order
        signals = ClientSignal.objects.filter(client_id=user_id, created_at__date__range=[start_date, end_date]).order_by('-created_at')

        # Calculate total profit and loss for the date range
        total_cumulative_pl = signals.aggregate(total_pl=Sum('cumulative_pl'))['total_pl']

        dt = {
            "s": signals,
            "total_cumulative_pl": total_cumulative_pl,
            "start_date": start_date,
            "end_date": end_date
        }
        return render(request, 'client_report.html', dt)
    except Exception as e:
        print(e)
        return redirect('client_login')

def Analysis(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        dt = {  
            "client_user": client_user ,  
        }
        return render(request, 'Analysis.html',dt)
    except:
        return redirect('client_login')

from django.shortcuts import render

def mt4_panel(request):
    return render(request, 'mt4.html')




from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import datetime



# from django.shortcuts import render
# from .models import ClientDetail  # Import your ClientDetail model
# import pandas as pd

# mt5_path = r"C:\\Program Files\\MetaTrader 5\\terminal64.exe"

# def fetch_symbols_from_mt5(login, password, server):
#     if not mt5.initialize():
#         return None, f"Client {login}: initialize() failed, error code = {mt5.last_error()}"
    
#     if not mt5.login(login=login, password=password, server=server):
#         error_code = mt5.last_error()
#         mt5.shutdown()
#         return None, f"Client {login}: Login failed, error code: {error_code}"
    
#     symbols = mt5.symbols_get()
#     mt5.shutdown()
    
#     if symbols is None:
#         return None, f"Client {login}: Failed to fetch symbols, error code = {mt5.last_error()}"
    
#     # Return the list of symbol names
#     return [symbol.name for symbol in symbols], None



from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from .models import ClientDetail  # Import your ClientDetail model
import time

# mt5_path = r"C:\\Program Files\\MetaTrader 5\\terminal64.exe"

from concurrent.futures import ThreadPoolExecutor
from .models import Client_SYMBOL_QTY, ClientDetail



# from concurrent.futures import ThreadPoolExecutor

# def execute_order_mt5(login, password, server, symbol, lot, order_type, price, stop_loss, take_profit):
#     # Ensure MT5 is initialized
#     if not mt5.initialize():
#         return f"Client {login}: initialize() failed, error code = {mt5.last_error()}"

#     # Attempt to login to MT5
#     if not mt5.login(login=login, password=password, server=server):
#         error_code = mt5.last_error()
#         mt5.shutdown()
#         return f"Client {login}: Login failed, error code: {error_code}"

#     # Try selecting the symbol
#     if not mt5.symbol_select(symbol, True):
#         # If symbol select fails, try reinitializing MT5 and retrying
#         mt5.shutdown()
#         if not mt5.initialize():
#             return f"Client {login}: Reinitialization failed, error code = {mt5.last_error()}"

#         if not mt5.login(login=login, password=password, server=server):
#             error_code = mt5.last_error()
#             mt5.shutdown()
#             return f"Client {login}: Re-login failed, error code: {error_code}"

#         if not mt5.symbol_select(symbol, True):
#             mt5.shutdown()
#             return f"Client {login}: symbol_select({symbol}) failed, error code = {mt5.last_error()}"

#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY if order_type == 'BUY' else mt5.ORDER_TYPE_SELL,
#         "price": price,
#         "sl": stop_loss,
#         "tp": take_profit,
#         "deviation": 0,
#         "magic": 234000,
#         "comment": "FinoFxAlgo",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC,
#     }

#     result = mt5.order_send(request)
#     mt5.shutdown()

#     return f"Client {login}: {'Success' if result.retcode == mt5.TRADE_RETCODE_DONE else 'Failed'}, Order ID: {result.order if result.retcode == mt5.TRADE_RETCODE_DONE else result.comment}"

from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Client_SYMBOL_QTY, ClientDetail


# def place_order_parallel(symbol, order_type, price, stop_loss, take_profit):
#     clients = ClientDetail.objects.filter(mt5_login__isnull=False)
    
#     order_messages = []

#     with ThreadPoolExecutor(max_workers=len(clients)) as executor:
#         futures = []
#         for client in clients:
#             client_symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=client.user_id, SYMBOL=symbol).first()
#             if client_symbol_qty and client_symbol_qty.trade == 'on':
#                 lot_size = client_symbol_qty.QUANTITY
#                 futures.append(executor.submit(
#                     place_order_mt5,  # Ensure this calls the function with logging
#                     client,
#                     symbol,
#                     lot_size,
#                     order_type,
#                     price,
#                     stop_loss,
#                     take_profit
#                 ))

#         for future in futures:
#             result = future.result()
#             order_messages.append(result)

#     return order_messages

# from django.http import JsonResponse

# def live_price(request, symbol):
#     # Fetch the live price for the symbol from MT5
#     price = fetch_live_price_from_mt5(symbol)  # Implement this function to get the price
#     return JsonResponse({'price': price})




# def fetch_live_price_from_mt5(symbol):
#     # Initialize the MT5 connection
#     if not mt5.initialize():
#         print("initialize() failed, error code =", mt5.last_error())
#         return None

#     # Request the latest price for the specified symbol
#     tick = mt5.symbol_info_tick(symbol)
    
#     if tick is None:
#         print(f"Failed to get tick info for {symbol}, error code =", mt5.last_error())
#         mt5.shutdown()
#         return None
    
#     # Extract the bid and ask prices
#     bid_price = tick.bid
#     ask_price = tick.ask
    
#     # Optionally, you can return the average of bid and ask as the live price
#     live_price = (bid_price + ask_price) / 2
    
#     # Shutdown the MT5 connection
#     mt5.shutdown()
    
#     return live_price

# @login_required
# def place_order(request):
#     clients = ClientDetail.objects.filter(mt5_login__isnull=False)

#     if clients.exists():
#         first_client = clients.first()
#         symbols, error = fetch_symbols_from_mt5(first_client.mt5_login, first_client.mt5_password, first_client.mt5_server)
#     else:
#         symbols = []
#         error = "No clients available."

#     if request.method == 'POST':
#         symbol = request.POST.get('symbol')
#         order_type = request.POST.get('order_type')
#         price = float(request.POST.get('price'))
#         stop_loss = float(request.POST.get('stop_loss'))
#         take_profit = float(request.POST.get('take_profit'))

#         # Place order logic
#         order_messages = place_order_parallel(symbol, order_type, price, stop_loss, take_profit)

#         return render(request, 'place_order.html', {
#             'symbols': symbols, 
#             'open_trades': [], 
#             'trade_history': [],
#             'order_messages': order_messages,
#         })

#     return render(request, 'place_order.html', {
#         'symbols': symbols,
#         'open_trades': [], 
#         'trade_history': [],
#         'order_messages': []
#     })


# from django.shortcuts import render, redirect
# from .models import ClientSymbolSetting, ClientDetail


# from django.shortcuts import render, redirect
# from .models import ClientDetail, ClientSymbolSetting


# def get_symbols_for_client(client):
#     if not mt5.initialize():
#         return []
    
#     if not mt5.login(login=client.mt5_login, password=client.mt5_password, server=client.mt5_server):
#         return []

#     symbols = mt5.symbols_get()
#     mt5.shutdown()
#     return [symbol.name for symbol in symbols]

# from .models import ClientDetail, ClientSymbolSetting  

# from django.shortcuts import render, get_object_or_404
# from .models import ClientDetail, ClientSymbolSetting
# 

# def symbol_settings(request):
#     # Fetch the ClientDetail using the new relationship field django_user
#     client = get_object_or_404(ClientDetail, django_user=request.user)
#     symbols = get_symbols_for_client(client)
#     symbol_settings = ClientSymbolSetting.objects.filter(client=client)

#     if request.method == 'POST':
#         for symbol in symbols:
#             quantity = request.POST.get(f'quantity_{symbol}', 0)
#             trade_enabled = request.POST.get(f'trade_enabled_{symbol}', 'off') == 'on'

#             setting, created = ClientSymbolSetting.objects.get_or_create(client=client, symbol=symbol)
#             setting.quantity = quantity
#             setting.trade_enabled = trade_enabled
#             setting.save()

#         return redirect('symbol_settings')

#     context = {
#         'symbols': symbols,
#         'symbol_settings': symbol_settings,
#     }
#     return render(request, 'symbol_settings.html', context)

# def execute_trades_for_client(client):
#     settings = ClientSymbolSetting.objects.filter(client=client, trade_enabled=True)

#     for setting in settings:
#         symbol = setting.symbol
#         quantity = setting.quantity

#         # Example trade execution logic
#         order_type = 'BUY'  # or dynamically determine
#         price = mt5.symbol_info_tick(symbol).ask  # Example price
#         stop_loss = 0  # Example stop loss
#         take_profit = 0  # Example take profit

#         # Execute trade using your existing order placement logic
#         result = execute_order_mt5(client.mt5_login, client.mt5_password, client.mt5_server, symbol, quantity, order_type, price, stop_loss, take_profit)

#         print(result)

# Use this function to trigger trades based on client settings, e.g., via a button or a scheduled task


# import subprocess
# import pandas as pd
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# mt5_path = r"C:\\Program Files\\MetaTrader 5\\terminal64.exe"

# @csrf_exempt  # If you need to allow POST requests from external sources
# def close_all_orders(request):
#     if request.method == 'POST':
#         clients = pd.DataFrame(list(ClientDetail.objects.filter().exclude(mt5_login=None).values()))

#         for i in range(len(clients)):
#             try:
#                 result = subprocess.check_output(
#                     ["python", r"C:\live\mt4algo\myapp\close_all_orders.py", 
#                      mt5_path, str(clients.iloc[i]['mt5_login']), 
#                      clients.iloc[i]['mt5_server'], 
#                      clients.iloc[i]['mt5_password']],
#                     stderr=subprocess.STDOUT
#                 )
#                 print(result.decode("utf-8"))
#             except subprocess.CalledProcessError as e:
#                 error_output = e.output.decode("utf-8")
#                 print(f"Error closing orders for client {clients.iloc[i]['mt5_login']}: {error_output}")
#                 return JsonResponse({'status': 'error', 'message': f'Failed to close orders for client {clients.iloc[i]["mt5_login"]}: {error_output}'})

#         return JsonResponse({'status': 'success', 'message': 'All orders closed successfully'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# def get_symbols(client):
#     """Function to get symbols using the client's credentials."""
#     try:
#         result = subprocess.check_output(
#             ["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\get_symbols.py", 
#              mt5_path, str(client['mt5_login']), 
#              client['mt5_server'], 
#              client['mt5_password']],
#             stderr=subprocess.STDOUT
#         )
#         symbols = result.decode("utf-8").replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(",")
#         return symbols
#     except subprocess.CalledProcessError as e:
#         error_output = e.output.decode("utf-8")
#         return []


# @csrf_exempt
# def get_price(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)
#         symbol = data['symbol']
#         clients= pd.DataFrame(list(ClientDetail.objects.filter().exclude(mt5_login=None).values()))
#         #info = get_symbol_info(mt5_path, clients.iloc[0]['mt5_login'], clients.iloc[0]['mt5_server'], clients.iloc[0]['mt5_password'], symbol)
#         result = subprocess.check_output(["python", r"C:\live\mt4algo\myapp\get_symbol_info.py", mt5_path, str(clients.iloc[0]['mt5_login']), clients.iloc[0]['mt5_server'], clients.iloc[0]['mt5_password'], symbol])
#         price = result.decode("utf-8")
#         return JsonResponse({'price': price})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


import datetime
import subprocess
import pickle
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import ClientDetail

# @csrf_exempt
# def trade_history11(request):
#     now = datetime.datetime.now()
#     start_time = now - datetime.timedelta(days=30)  # Adjust as needed
#     user_id = request.session.get('user_id')
#     clients= pd.DataFrame(list(ClientDetail.objects.filter(user_id=user_id).exclude(mt5_login=None).values()))
#     #open_trades_list = get_open_trades(mt5_path, clients)
#     #history_list = get_trade_history(mt5_path, start_time, now, clients)
#     open_trades_list = []
#     history_list = []
    
#     for i in range(0, len(clients)):
#         result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\get_open_trades.py", mt5_path, str(clients.iloc[i]['mt5_login']), clients.iloc[i]['mt5_server'], clients.iloc[i]['mt5_password']])
#         with open(r"C:\Users\pc\Documents\sahil\algosms\myapp\open_trades.pkl", 'rb') as f:
#             open_trades = pickle.load(f)
#         """
#         open_trades = result.decode("utf-8")
#         open_trades = open_trades.replace('[', '')
#         open_trades = open_trades.replace(']', '')
#         open_trades = list(open_trades.split(","))
#         #print(open_trades)
#         """
#         open_trades_list.extend(open_trades)
#         #print(open_trades_list)
    
    
#     for i in range(0, len(clients)):
#         result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\get_history.py", mt5_path, str(clients.iloc[i]['mt5_login']), clients.iloc[i]['mt5_server'], clients.iloc[i]['mt5_password']])
#         result = result.decode("utf-8")
#         with open(r"C:\Users\pc\Documents\sahil\algosms\myapp\history.pkl", 'rb') as f:
#             history = pickle.load(f)
#         """
#         history = history.replace('[', '')
#         history = history.replace(']', '')
#         history = list(history.split(","))
#         """
#         history_list.extend(history)
#         #print(history_list)

#     return JsonResponse({'status': 'success', 'open_trades': open_trades_list, 'history': history_list})


from django.http import JsonResponse
from .models import TradeHistory, ClientDetail

def fetch_open_trades(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

    client_user = ClientDetail.objects.get(user_id=user_id)
    open_trades = TradeHistory.objects.filter(client=client_user, trade_type='OPEN')

    open_trades_list = []
    for trade in open_trades:
        open_trades_list.append({
            'ticket': trade.ticket,
            'time': trade.time.timestamp(),
            'symbol': trade.symbol,
            'volume': trade.volume,
            'price_open': trade.price_open,
            'price_current': trade.price_current,
            'sl': trade.sl,
            'tp': trade.tp,
            'profit': trade.profit
        })

    return JsonResponse({'status': 'success', 'trades': open_trades_list})


# from django.http import JsonResponse
# from .models import TradeHistory, ClientDetail
# from django.utils import timezone

# @csrf_exempt
# def fetch_trade_data(request):
#     now = timezone.now()
#     start_time = now - datetime.timedelta(days=30)
#     user_id = request.session.get('user_id')
#     clients = pd.DataFrame(list(ClientDetail.objects.filter(user_id=user_id).exclude(mt5_login=None).values()))
#     clients.to_pickle(r"C:\live\mt4algo\myapp\clients.pickle")

#     for i in range(0, len(clients)):
#         client = clients.iloc[i]
#         result = subprocess.check_output(["python", r"C:\live\mt4algo\myapp\get_open_trades.py", mt5_path, str(client['mt5_login']), client['mt5_server'], client['mt5_password']])
        
#         with open(r"C:\live\mt4algo\myapp\open_trades.pkl", 'rb') as f:
#             open_trades = pickle.load(f)
        
#         for trade in open_trades:
#             TradeHistory.objects.update_or_create(
#                 ticket=trade['ticket'],
#                 defaults={
#                     'client': ClientDetail.objects.get(user_id=client['user_id']),
#                     'time': timezone.datetime.fromtimestamp(trade['time']),
#                     'symbol': trade['symbol'],
#                     'volume': trade['volume'],
#                     'price_open': trade['price_open'],
#                     'price_current': trade['price_current'],
#                     'sl': trade['sl'],
#                     'tp': trade['tp'],
#                     'profit': trade['profit'],
#                     'trade_type': 'OPEN'
#                 }
#             )

#     for i in range(0, len(clients)):
#         client = clients.iloc[i]
#         result = subprocess.check_output(["python", r"C:\live\mt4algo\myapp\get_history.py", mt5_path, str(client['mt5_login']), client['mt5_server'], client['mt5_password']])
        
#         with open(r"C:\live\mt4algo\myapp\history.pkl", 'rb') as f:
#             history = pickle.load(f)
        
#         for trade in history:
#             TradeHistory.objects.update_or_create(
#                 ticket=trade['ticket'],
#                 defaults={
#                     'client': ClientDetail.objects.get(user_id=client['user_id']),
#                     'time': timezone.datetime.fromtimestamp(trade['time']),
#                     'symbol': trade['symbol'],
#                     'volume': trade['volume'],
#                     'price': trade['price'],
#                     'sl': trade['sl'],
#                     'tp': trade['tp'],
#                     'profit': trade['profit'],
#                     'trade_type': trade['type']
#                 }
#             )

#     return JsonResponse({'status': 'success', 'message': 'Trade data fetched and saved successfully'})



# def trade_history(request):
#     try:
#         user_id = request.session.get('user_id')
#         client_user = ClientDetail.objects.get(user_id=user_id)
#         # dt = {  
#         #     "client_user": client_user ,  
#         # }
#         return render(request, 'trade_history.html',{'client_user':client_user})
#     except Exception:
#         return redirect(request,'client_login')


from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import ClientDetail
import openai
import yfinance as yf
import requests
import re
from datetime import datetime, timedelta

# Use API key from environment or settings
openai.api_key = settings.OPENAI_API_KEY

# Predefined set of valid symbols (expand as needed)
valid_symbols = set([
    'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'NZDUSD', 'USDCHF', 'USDCAD',
    'BTCUSD', 'ETHUSD', 'LTCUSD', 'XRPUSD',
    'XAUUSD', 'XAGUSD', 'GOLD',
    'USOIL', 'WTI', 'CRUDEOIL',
    'AAPL', 'TSLA', 'GOOG', 'AMZN',
    # Add more symbols as needed
])

# Common English words to exclude
common_words = set([
    'THE', 'IS', 'IN', 'AT', 'OF', 'ON', 'AND', 'A', 'AN',
    'FOR', 'TO', 'WITH', 'BY', 'FROM', 'AS', 'THIS', 'THAT',
    'THESE', 'THOSE', 'YOUR', 'MY', 'OUR', 'US', 'IT', 'YOU',
    # Add more common words as needed
])

# Keywords indicating real-time data request
real_time_keywords = [
    'price', 'trend', 'rate', 'current', 'live', 'real-time', 'today',
    'update', 'data', 'analysis', 'target', 'forecast', 'prediction',
    'market', 'quote', 'value', 'info', 'information', 'sl', 'stop-loss', 'level'
]

def extract_symbols(message):
    """
    Extract potential financial symbols from the user's message.
    """
    message_upper = message.upper()
    symbols = []

    # First, check for multi-word symbols
    multi_word_symbols = {
        'US OIL': 'USOIL',
        'WEST TEXAS INTERMEDIATE': 'WTI',
        # Add more multi-word symbols if needed
    }
    for multi_word, symbol in multi_word_symbols.items():
        if multi_word in message_upper:
            symbols.append(symbol)

    # Then, use regex to find single-word symbols
    pattern = r'\b[A-Z]{2,6}\b'  # Adjust as needed
    potential_symbols = re.findall(pattern, message_upper)

    # Filter out common English words and include only valid symbols
    symbols += [s for s in potential_symbols if s not in common_words and s in valid_symbols]

    # Remove duplicates
    symbols = list(set(symbols))

    return symbols

def map_symbol_to_yfinance(symbol):
    """
    Map the extracted symbol to a format recognized by yfinance or other APIs.
    """
    symbol = symbol.upper()
    if symbol in ['BTCUSD', 'ETHUSD', 'LTCUSD', 'XRPUSD']:
        # For cryptocurrencies
        return symbol.replace('USD', '-USD')
    elif symbol in ['XAUUSD', 'GOLD']:
        return 'GC=F'  # Gold Futures
    elif symbol in ['XAGUSD', 'SILVER']:
        return 'SI=F'  # Silver Futures
    elif symbol in ['USOIL', 'WTI', 'CRUDEOIL']:
        return 'CL=F'  # Crude Oil Futures
    elif symbol.endswith('USD') and len(symbol) == 6:
        # For currency pairs (Forex)
        return symbol + '=X'
    else:
        return symbol  # Stocks and other symbols

def get_market_data(symbol):
    """
    Fetch the latest price for the given symbol using yfinance or alternative APIs.
    """
    # Handle cryptocurrencies separately using CoinGecko API
    crypto_symbols = {
        'BTC-USD': 'bitcoin',
        'ETH-USD': 'ethereum',
        'LTC-USD': 'litecoin',
        'XRP-USD': 'ripple',
        # Add more cryptocurrencies as needed
    }

    if symbol in crypto_symbols:
        # Fetch data from CoinGecko API
        coin_id = crypto_symbols[symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd'
        }
        response = requests.get(url, params=params)
        data = response.json()
        if coin_id in data and 'usd' in data[coin_id]:
            price = data[coin_id]['usd']
            return price
        else:
            return None
    else:
        # Fetch data from yfinance
        try:
            data = yf.Ticker(symbol)
            hist = data.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                return round(price, 2)
            else:
                return None
        except Exception as e:
            print(f"Error fetching market data for {symbol}: {e}")
            return None

def get_trend_info(symbol):
    """
    Fetch historical data for the symbol and analyze the trend over the past 5 trading days.
    Returns a string indicating the trend.
    """
    try:
        data = yf.Ticker(symbol)
        # Calculate start and end dates
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=10)  # Extended to cover weekends

        # Fetch historical data for the custom date range
        hist = data.history(start=start_date, end=end_date)
        if hist.empty or len(hist) < 5:
            return None  # Not enough data to analyze trend

        # Use the last 5 available trading days
        hist = hist.tail(5)

        # Calculate the percentage change over the period
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100

        # Determine the trend based on percentage change
        if percent_change > 0.5:
            trend = f"an upward trend, increasing by {percent_change:.2f}% over the past {len(hist)} days"
        elif percent_change < -0.5:
            trend = f"a downward trend, decreasing by {percent_change:.2f}% over the past {len(hist)} days"
        else:
            trend = f"relatively stable, changing by {percent_change:.2f}% over the past {len(hist)} days"

        return trend
    except Exception as e:
        print(f"Error fetching trend data for {symbol}: {e}")
        return None

def ai_trading(request):
    # Get the user and their chat history
    user_id = request.session.get('user_id')
    client_user = get_object_or_404(ClientDetail, user_id=user_id)
    chat_history = request.session.get('chat_history', [])

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()

        # Append the user's message
        chat_history.append({"role": "user", "content": user_message})

        # Check if the user is asking for real-time data
        is_real_time_query = any(keyword in user_message.lower() for keyword in real_time_keywords)

        # Extract symbols from the user's message
        detected_symbols = extract_symbols(user_message)

        try:
            if detected_symbols:
                responses = []
                for symbol in detected_symbols:
                    yf_symbol = map_symbol_to_yfinance(symbol)

                    # Initialize variables
                    latest_price = None
                    trend_info = None

                    # Fetch data as needed
                    latest_price = get_market_data(yf_symbol)
                    trend_info = get_trend_info(yf_symbol)

                    # Build the response
                    response_parts = []
                    if latest_price is not None:
                        response_parts.append(f"The latest price for {symbol} is ${latest_price}.")
                    else:
                        response_parts.append(f"Real-time data for {symbol} is not available at the moment.")

                    if trend_info:
                        response_parts.append(f"The recent trend for {symbol} shows {trend_info}.")

                    responses.append(" ".join(response_parts))

                combined_response = " ".join(responses)

                # Construct the prompt for OpenAI
                prompt = (
                    f"You are a financial assistant AI. "
                    f"Use the following data to answer the user's question:\n"
                    f"{combined_response}\n"
                    f"User's Query: {user_message}"
                )
            else:
                # Handle general queries
                prompt = f"You are a helpful assistant. Please assist with the following query:\n{user_message}"

            # Get AI response
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-4 if available
                messages=[
                    {"role": "system", "content": "You are a helpful and knowledgeable financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            bot_response = response.choices[0].message['content'].strip()

        except Exception as e:
            print(f"Error: {e}")
            bot_response = (
                "I'm sorry, but I couldn't process your request at this time. "
                "Please try again later or check your query and try again."
            )

        # Append the assistant's response
        chat_history.append({"role": "assistant", "content": bot_response})

        # Save chat history in session
        request.session['chat_history'] = chat_history

        return render(request, 'ai_trading.html', {'chat_history': chat_history})

    # Reset or initialize chat history on GET
    return render(request, 'ai_trading.html', {'chat_history': []})

from django.shortcuts import render, redirect
from .forms import MarketDataForm

def upload_data(request):
    if request.method == 'POST':
        form = MarketDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ai_trading')  # Redirect to the AI trading page after submission
    else:
        form = MarketDataForm()
    
    return render(request, 'upload_data.html', {'form': form})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trade
import json


@csrf_exempt
def delete_trades(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tickets = data.get('tickets', [])
        Trade.objects.filter(ticket__in=tickets).delete()
        return JsonResponse({'status': 'success', 'message': f'Deleted {len(tickets)} trades.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# ------------------------------------------- GROPU -------------------------------------
# =======================================================================================
from .forms import GroupForm

def group_list(request):
    groups = GROUP.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

def update_group(request, group_id):
    # Retrieve the symbol object from the database
    group = get_object_or_404(GROUP, id=group_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('group_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = GroupForm(instance=group)
    
    return render(request, 'update_group.html', {'form': form, 'group': group})



def delete_group(request, group_id):
    group = GROUP.objects.get(id=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')  # Redirect to the group list page after deletion
    return render(request, 'delete_group.html', {'group': group})




# ------------------------------------------- Broker -------------------------------------
# =======================================================================================
from .forms import BrokerForm

def broker_list(request):
    broker = Broker.objects.all()
    return render(request, 'group_list.html', {'broker': broker})

def create_broker(request):
    if request.method == 'POST':
        form = BrokerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('broker_list')
    else:
        form = BrokerForm()
    return render(request, 'create_broker.html', {'form': form})

def update_broker(request, broker_id):
    # Retrieve the symbol object from the database
    broker = get_object_or_404(Broker, id=broker_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = BrokerForm(request.POST, instance=broker)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('broker_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = BrokerForm(instance=broker)
    
    return render(request, 'update_broker.html', {'form': form, 'broker': broker})



def delete_broker(request, broker_id):
    broker = Broker.objects.get(id=broker_id)
    if request.method == 'POST':
        broker.delete()
        return redirect('broker_list')  # Redirect to the group list page after deletion
    return render(request, 'delete_broker.html', {'broker': broker})



# ==
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def close_orders_view(request):
#     if request.method == "POST":
#         symbol = request.POST.get("symbol")
#         close_messages = close_orders_for_symbol(symbol)
#         messages.success(request, f"Orders for symbol {symbol} closed. Details:")
#         return render(request, 'place_order.html', {'close_messages': close_messages})

#     return redirect('place_order')


# from concurrent.futures import ThreadPoolExecutor, as_completed
# from .models import ClientDetail
# import time

# def connect_to_mt5(client, retries=3, delay=2):
#     for attempt in range(retries):
#         if not mt5.initialize():
#             print(f"Client {client.mt5_login}: Failed to initialize MT5 on attempt {attempt + 1}, retrying...")
#             time.sleep(delay)
#             continue

#         if not mt5.login(login=client.mt5_login, password=client.mt5_password, server=client.mt5_server):
#             error_code = mt5.last_error()
#             print(f"Client {client.mt5_login}: Login failed, error code: {error_code}. Attempt {attempt + 1} of {retries}")
#             mt5.shutdown()
#             time.sleep(delay)
#             continue

#         # Successful connection
#         print(f"Client {client.mt5_login}: Successfully logged in on attempt {attempt + 1}")
#         return True

#     # Final attempt failed
#     print(f"Client {client.mt5_login}: All login attempts failed.")
#     return False


# from .models import ClientDetail
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def close_order_mt5(login, password, server, position_id, symbol, retry_count=3):
#     attempt = 0
#     while attempt < retry_count:
#         attempt += 1
#         if not mt5.initialize():
#             message = f"Client {login}: initialize() failed, error code = {mt5.last_error()}"
#             logger.error(message)
#             log_mt5_operation("Close Order", login, symbol, message)
#             continue

#         if not mt5.login(login=login, password=password, server=server):
#             error_code = mt5.last_error()
#             message = f"Client {login}: Login failed, error code: {error_code}"
#             logger.error(message)
#             log_mt5_operation("Close Order", login, symbol, message)
#             mt5.shutdown()
#             continue

#         # Fetch the position details
#         position = mt5.positions_get(ticket=position_id)
#         if not position:
#             message = f"Client {login}: Position {position_id} not found, unable to close."
#             logger.error(message)
#             log_mt5_operation("Close Order", login, symbol, message)
#             mt5.shutdown()
#             continue

#         # Fetch symbol info for contract size and tick value
#         symbol_info = mt5.symbol_info(symbol)
#         if not symbol_info:
#             message = f"Client {login}: Symbol {symbol} not found, unable to fetch contract size and tick value."
#             logger.error(message)
#             mt5.shutdown()
#             continue

#         # contract_size = symbol_info.trade_contract_size  # e.g., 100 for Forex
#         # tick_value = symbol_info.trade_tick_value  # Monetary value of a single tick

#         entry_price = Decimal(position[0].price_open)  # Convert entry price to Decimal
#         volume = Decimal(position[0].volume) 

#         # Prepare the close order request
#         request = {
#             "action": mt5.TRADE_ACTION_DEAL,
#             "symbol": symbol,
#             "volume": position[0].volume,
#             "type": mt5.ORDER_TYPE_SELL if position[0].type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
#             "position": position_id,
#             "price": mt5.symbol_info_tick(symbol).bid if position[0].type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
#             "deviation": 10,
#         }

#         result = mt5.order_send(request)
#         mt5.shutdown()

#         if result.retcode == mt5.TRADE_RETCODE_DONE:
#             exit_price = Decimal(request['price'])

#             order_type = 'BUY' if position[0].type == mt5.ORDER_TYPE_BUY else 'SELL'
#             # Calculate the P&L based on the symbol
#             prloss = calculate_pnl(entry_price, exit_price, volume, symbol, order_type)

#             # Update TradeHistory
#             trade_history = TradeHistory.objects.filter(client__mt5_login=login, symbol=symbol, exit_price__isnull=True).first()
#             if trade_history:
#                 trade_history.exit_price = exit_price
#                 trade_history.exit_time = timezone.now()
#                 trade_history.p_l = prloss
#                 trade_history.save()

#                 message = f"Client {login}: Successfully closed order {position_id}"
#                 log_mt5_operation("Close Order", login, symbol, message)
#                 return message
#             else:
#                 message = f"Client {login}: No matching trade found for order {position_id}"
#                 log_mt5_operation("Close Order", login, symbol, message)
#         else:
#             message = f"Client {login}: Failed to close order {position_id}, {result.comment}"
#             log_mt5_operation("Close Order", login, symbol, message)

#     return f"Client {login}: Unable to close order {position_id} after {retry_count} attempts"

# from django.http import HttpResponse
# from .utils import start_monitoring  # फंक्शन को utils.py या उसी फाइल से इम्पोर्ट करें

# # यह सामान्य Django view है जो यूजर को स्टार्टिंग के लिए कॉल करने पर शुरू करता है।
# def start_background_monitoring(request):
#     # मॉनिटरिंग स्टार्ट करें
#     start_monitoring()

#     return HttpResponse("SL/TP monitoring started in the background.")


from decimal import Decimal

def calculate_pnl(entry_price, exit_price, qty, symbol_name, order_type):
    """
    Calculate P&L based on the symbol name and order type (BUY or SELL).
    
    Parameters:
        entry_price (Decimal): The price at which the order was opened.
        exit_price (Decimal): The price at which the order was closed.
        qty (Decimal): The quantity traded.
        symbol_name (str): The symbol of the trade (e.g., XAUUSDm, EURUSDm).
        order_type (str): 'BUY' or 'SELL' to determine the P&L calculation.
    
    Returns:
        Decimal: The calculated P&L.
    """
    # Determine the P&L calculation based on the order type (BUY or SELL)
    if order_type == 'BUY':
        # For BUY orders, profit/loss is (Exit Price - Entry Price)
        price_difference = exit_price - entry_price
    elif order_type == 'SELL':
        # For SELL orders, profit/loss is (Entry Price - Exit Price)
        price_difference = entry_price - exit_price
    else:
        raise ValueError("Invalid order type. Expected 'BUY' or 'SELL'.")

    # Calculate P&L based on the symbol
    if symbol_name in ['XAUUSDm', 'USTEC', 'NAS100']:
        # For XAUUSDm, USTEC, NAS100: Contract size = 100
        prloss = price_difference * qty * Decimal('100')
    
    elif symbol_name in ['USOILm', 'EURUSDm', 'GBPUSDm', 'AUDNZDm', 'GBPNZDm', 'USDCHFm', 'GBPCADm', 'EURAUDm', 'EURGBPm', 'NZDUSDm', 'USDCADm', 'AUDUSDm']:
        # For Forex Pairs (USOILm, EURUSDm, etc.): Contract size = 100, multiplier = 10
        prloss = price_difference * Decimal('100') * Decimal('10') * qty
    
    elif symbol_name in ['USDJPYm', 'EURJPYm', 'GBPJPYm', 'AUDJPYm']:
        # For JPY pairs: Contract size = 100, multiplier = 6.39
        prloss = price_difference * Decimal('100') * Decimal('6.39') * qty
    
    else:
        # Default case if the symbol is not in the predefined list
        prloss = price_difference * qty

    return prloss


# def close_orders_for_symbol(symbol):
#     clients = ClientDetail.objects.filter(mt5_login__isnull=False)
#     close_messages = []

#     for client in clients:
#         if not mt5.initialize():
#             message = f"Client {client.mt5_login}: initialize() failed, error code = {mt5.last_error()}"
#             logger.error(message)
#             close_messages.append(message)
#             continue

#         if not mt5.login(login=client.mt5_login, password=client.mt5_password, server=client.mt5_server):
#             error_code = mt5.last_error()
#             message = f"Client {client.mt5_login}: Login failed, error code: {error_code}"
#             logger.error(message)
#             close_messages.append(message)
#             mt5.shutdown()
#             continue

#         # Fetch open positions for the specific symbol
#         positions = mt5.positions_get(symbol=symbol)
#         if positions is None or len(positions) == 0:
#             message = f"Client {client.mt5_login}: No open positions found for symbol {symbol}"
#             logger.info(message)
#             close_messages.append(message)
#             mt5.shutdown()
#             continue

#         for position in positions:
#             result_message = close_order_mt5(client.mt5_login, client.mt5_password, client.mt5_server, position.ticket, symbol)
#             close_messages.append(result_message)
#             logger.info(result_message)

#         mt5.shutdown()

#     return close_messages


# def place_order_mt5(client, symbol, lot, order_type, price, stop_loss, take_profit):
#     if not mt5.initialize():
#         message = f"Client {client.mt5_login}: initialize() failed, error code = {mt5.last_error()}"
#         logger.error(message)
#         log_mt5_operation("Place Order", client.mt5_login, symbol, message)
#         return message

#     if not mt5.login(login=client.mt5_login, password=client.mt5_password, server=client.mt5_server):
#         error_code = mt5.last_error()
#         message = f"Client {client.mt5_login}: Login failed, error code: {error_code}"
#         logger.error(message)
#         log_mt5_operation("Place Order", client.mt5_login, symbol, message)
#         mt5.shutdown()
#         return message

#     if not mt5.symbol_select(symbol, True):
#         message = f"Client {client.mt5_login}: symbol_select({symbol}) failed, error code = {mt5.last_error()}"
#         logger.error(message)
#         log_mt5_operation("Place Order", client.mt5_login, symbol, message)
#         mt5.shutdown()
#         return message

#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY if order_type == 'BUY' else mt5.ORDER_TYPE_SELL,
#         "price": price,
#         "sl": stop_loss,
#         "tp": take_profit,
#         "deviation": 0,
#         "magic": 234000,
#         "comment": "FinoFxAlgo",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC,
#     }

#     result = mt5.order_send(request)
#     mt5.shutdown()

#     if result.retcode == mt5.TRADE_RETCODE_DONE:
#         # Capture the price at which the order was executed
#         executed_price = result.price if result.price != 0.0 else price
#         ticket_id = str(result.order)
#         TradeHistory.objects.create(
#             client=client,
#             symbol=symbol,
#             trade_type=order_type,
#             quantity=lot,
#             entry_price=executed_price,
#             ticket_id=ticket_id
#         )
#         message = f"Client {client.mt5_login}: Order placed successfully, Order ID {result.order}"
#         log_mt5_operation("Place Order", client.mt5_login, symbol, message)
        
#         if result.price == stop_loss:
#             # Stop Loss Triggered
#             message = f"Client {client.mt5_login}: Stop loss triggered for {symbol}"
#             trade_history = TradeHistory.objects.filter(client=client, symbol=symbol, exit_price__isnull=True).first()
#             if trade_history:
#                 trade_history.exit_price = stop_loss
#                 trade_history.p_l = (executed_price - stop_loss) * lot
#                 trade_history.save()

#         if result.price == take_profit:
#             # Take Profit Triggered
#             message = f"Client {client.mt5_login}: Take profit triggered for {symbol}"
#             trade_history = TradeHistory.objects.filter(client=client, symbol=symbol, exit_price__isnull=True).first()
#             if trade_history:
#                 trade_history.exit_price = take_profit
#                 trade_history.p_l = (take_profit - executed_price) * lot
#                 trade_history.save()
                
#         return message
#     else:
#         message = f"Client {client.mt5_login}: Trade failed, {result.comment}"
#         log_mt5_operation("Place Order", client.mt5_login, symbol, message)
#         return message

# def place_order_view(request):
#     if request.method == 'POST':
#         symbol = request.POST.get('symbol')
#         order_type = request.POST.get('order_type')
#         price = float(request.POST.get('price'))
#         stop_loss = float(request.POST.get('stop_loss'))
#         take_profit = float(request.POST.get('take_profit'))
        
#         clients = ClientDetail.objects.filter(mt5_login__isnull=False)
#         order_messages = []

#         with ThreadPoolExecutor(max_workers=len(clients)) as executor:
#             futures = [
#                 executor.submit(place_order_mt5, client, symbol, client.lot_size, order_type, price, stop_loss, take_profit)
#                 for client in clients
#             ]

#             for future in as_completed(futures):
#                 result = future.result()
#                 order_messages.append(result)
#                 print(result)

#         return render(request, 'place_order.html', {
#             'order_messages': order_messages,
#             'symbols': symbol,  # Make sure this is defined and passed correctly
#             'open_trades': [],  # Populate this with actual open trades if necessary
#             'trade_history': [],  # Populate this with actual trade history if necessary
#         })

#     return render(request, 'place_order.html', {
#         'symbols': symbol,  # Ensure this is defined
#         'open_trades': [],
#         'trade_history': [],
#         'order_messages': [],
#     })

# import logging
# from .models import MT5OperationLog

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def log_mt5_operation(operation_type, client_login, symbol, message):
#     MT5OperationLog.objects.create(
#         operation_type=operation_type,
#         client_login=client_login,
#         symbol=symbol,
#         message=message
#     )


# from django.shortcuts import render
# from .models import MT5OperationLog

# def view_mt5_logs(request):
#     logs = MT5OperationLog.objects.all().order_by('-timestamp')
#     return render(request, 'mt5_logs.html', {'logs': logs})

from django.shortcuts import render
from .models import TradeHistory

def trade_history_view(request):
    trades = TradeHistory.objects.all().order_by('signal_time')

    # Calculate the total cumulative P&L, handling None values
    total_cumulative_p_l = sum(trade.cumulative_p_l for trade in trades if trade.cumulative_p_l is not None)

    return render(request, 'trade_history.html', {
        'trades': trades,
        'total_cumulative_p_l': total_cumulative_p_l,
    })



from django.shortcuts import render
from .models import TradeHistory, ClientDetail
from django.utils import timezone
import datetime  # Ensure the datetime module is correctly imported

def client_trade_history_view(request):
    client_id = request.session.get('user_id')

    # Fetch the client details
    client = ClientDetail.objects.get(user_id=client_id)

    # Get the selected start and end dates from the request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # If no filter is applied (i.e., no start_date or end_date is provided), show today's history
    if not start_date_str and not end_date_str:
        start_date = timezone.now().date()
        end_date = start_date
    else:
        # Determine the start and end dates from the filters
        start_date = datetime.datetime.fromisoformat(start_date_str).date() if start_date_str else timezone.now().date()
        end_date = datetime.datetime.fromisoformat(end_date_str).date() if end_date_str else timezone.now().date()

    # Calculate the start and end of the selected date range
    start_datetime = timezone.make_aware(datetime.datetime.combine(start_date, datetime.datetime.min.time()))
    end_datetime = timezone.make_aware(datetime.datetime.combine(end_date, datetime.datetime.max.time()))

    # If the account type is 'live', filter trades from the client's join date
    if client.account_type == 'live' and start_date < client.date_joined.date():
        start_datetime = timezone.make_aware(datetime.datetime.combine(client.date_joined.date(), datetime.datetime.min.time()))

    # Filter trades for the logged-in client within the selected date range
    trades = TradeHistory.objects.filter(
        client__user_id=client_id,
        signal_time__range=(start_datetime, end_datetime)
    ).order_by('signal_time')

    cumulative_p_l = 0  # Initialize cumulative P&L
    for trade in trades:
        trade.p_l = trade.p_l if trade.p_l else 0  # Make sure P&L is never None
        cumulative_p_l += trade.p_l  # Add current trade's P&L to cumulative total
        trade.cumulative_p_l = cumulative_p_l  # Set cumulative P&L for the trade
    
    # Calculate the total cumulative P&L for the selected date range
    total_cumulative_p_l = cumulative_p_l if trades.exists() else 0
    
    return render(request, 'client_trade_history.html', {
        'trades': trades,
        'total_cumulative_p_l': total_cumulative_p_l,
        'start_date': start_date,
        'end_date': end_date,
        'client_user': client,
    })



# from django.shortcuts import render
# from .models import TradeHistory
# from django.utils import timezone
# from datetime import datetime

# def client_trade_history_view(request):
#     client_id = request.session.get('user_id')

#     # Fetch the client details
#     client = ClientDetail.objects.get(user_id=client_id)

#     # Get the selected start and end dates from the request
#     start_date_str = request.GET.get('start_date')
#     end_date_str = request.GET.get('end_date')

#     # If no filter is applied (i.e., no start_date or end_date is provided), show today's history
#     if not start_date_str and not end_date_str:
#         start_date = timezone.now().date()
#         end_date = start_date
#     else:
#         # Determine the start and end dates from the filters
#         start_date = datetime.fromisoformat(start_date_str).date() if start_date_str else timezone.now().date()
#         end_date = datetime.fromisoformat(end_date_str).date() if end_date_str else timezone.now().date()

#     # Calculate the start and end of the selected date range
#     start_datetime = timezone.make_aware(timezone.datetime.combine(start_date, datetime.min.time()))
#     end_datetime = timezone.make_aware(timezone.datetime.combine(end_date, datetime.max.time()))

#     # If the account type is 'live', filter trades from the client's join date
#     if client.account_type == 'live' and start_date < client.date_joined.date():
#         start_datetime = timezone.make_aware(timezone.datetime.combine(client.date_joined.date(), datetime.min.time()))

#     # Filter trades for the logged-in client within the selected date range
#     trades = TradeHistory.objects.filter(
#         client__user_id=client_id,
#         signal_time__range=(start_datetime, end_datetime)
#     ).order_by('signal_time')

#     cumulative_p_l = 0  # Initialize cumulative P&L
#     for trade in trades:
#         trade.p_l = trade.p_l if trade.p_l else 0  # Make sure P&L is never None
#         cumulative_p_l += trade.p_l  # Add current trade's P&L to cumulative total
#         trade.cumulative_p_l = cumulative_p_l  # Set cumulative P&L for the trade
#     # Calculate the total cumulative P&L for the selected date range
#     total_cumulative_p_l = cumulative_p_l if trades.exists() else 0
    
#     return render(request, 'client_trade_history.html', {
#         'trades': trades,
#         'total_cumulative_p_l': total_cumulative_p_l,
#         'start_date': start_date,
#         'end_date': end_date,
#         'client_user': client,
#     })



import pandas as pd
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import TradeHistory, ClientDetail
from django.utils import timezone
from django.contrib import messages
from datetime import datetime

def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            # Iterate over each row and save it to the TradeHistory model for all clients
            for index, row in df.iterrows():
                # Get all clients
                clients = ClientDetail.objects.all()

                # Process signal_time and exit_time
                try:
                    signal_time = row['signal_time']
                    if pd.notnull(signal_time):
                        if isinstance(signal_time, str):
                            signal_time = datetime.fromisoformat(signal_time)
                        signal_time = timezone.make_aware(signal_time) if timezone.is_naive(signal_time) else signal_time
                    else:
                        signal_time = timezone.now()

                    exit_time = row.get('exit_time')
                    if pd.notnull(exit_time):
                        if isinstance(exit_time, str):
                            exit_time = datetime.fromisoformat(exit_time)
                        exit_time = timezone.make_aware(exit_time) if timezone.is_naive(exit_time) else exit_time
                    else:
                        exit_time = None
                except Exception as e:
                    print(f"Error processing dates for row {index}: {e}")
                    continue

                for client in clients:
                    try:
                        # Create and save TradeHistory object for each client
                        trade_history = TradeHistory(
                            client=client,
                            signal_time=signal_time,
                            symbol=row['symbol'],
                            trade_type=row['trade_type'],
                            quantity=row['quantity'],
                            entry_price=row.get('entry_price', None),
                            exit_price=row.get('exit_price', None),
                            exit_time=exit_time,
                            p_l=row.get('p_l', None),
                            cumulative_p_l=row.get('cumulative_p_l', None)
                        )
                        trade_history.save()
                    except Exception as e:
                        print(f"Error saving trade history for client {client.id}: {e}")
                        continue  # Skip to the next row if there's an error

            # Add success message
            messages.success(request, "Excel file uploaded and data saved for all clients successfully!")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_excel.html', {'form': form})


# # views.py
# from .mt5_fetcher import initialize_mt5, fetch_live_positions, fetch_trade_history
# from .models import ClientDetail

# def fetch_mt5_data(request):
#     # Example of fetching a client
#     client = ClientDetail.objects.first()

#     # Initialize MetaTrader5
#     if not initialize_mt5(login_number=client.mt5_login, password=client.mt5_password, server=client.mt5_server):
#         return render(request, 'error.html', {'message': 'MT5 initialization failed'})

#     # Fetch live positions
#     fetch_live_positions(client)

#     # Fetch closed trade history
#     fetch_trade_history(client)

#     return render(request, 'success.html', {'message': 'Data fetched successfully!'})

# views.py

from django.http import JsonResponse
import subprocess
import os

def run_pyqt_app(request, broker_url):
    """
    This view will trigger the PyQt5 application without redirecting the browser.
    It runs the PyQt5 window in the background using a subprocess.
    """
    script_path = os.path.abspath(r"C:\Users\pc\Documents\sahil\algosms\broker_app.py")  # Adjust this path to your broker_app.py

    try:
        # Launch the PyQt5 app in the background
        subprocess.Popen(["python", script_path, broker_url], shell=True)

        return JsonResponse({"status": "success", "message": "PyQt5 window opened"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

from django.shortcuts import render, redirect
from .models import ClientDetail

# def broker_selection_view(request):
#     # Handle window close detection and session management for 'Next Step' button
#     if 'window_closed' not in request.GET:
#         request.session['show_next_step'] = False  # Ensure 'Next Step' button is hidden on initial load

#     # Check if the window has been closed based on the query parameter
#     if request.GET.get('window_closed') == 'true':
#         request.session['show_next_step'] = True

#     show_next_step = request.session.get('show_next_step', False)

#     # Handle the broker selection process
#     if request.method == 'POST':
#         selected_broker = request.POST.get('broker')
#         client_email = request.POST.get('email')
#         # Save the selected broker and email to the session
#         request.session['client_email'] = client_email
#         client, created = ClientDetail.objects.get_or_create(
#             email=client_email,
#             defaults={'broker': selected_broker}
#         )
#         if not created:
#             client.broker = selected_broker
#             client.save()

#         # Redirect to KYC step 1 (National ID Upload)
#         return redirect('upload_national_id')

#     return render(request, 'broker_selection.html', {'show_next_step': show_next_step})
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import ClientDetail
import uuid
from datetime import timedelta

def client_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate form inputs
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('register')

        # Check if the email is already registered
        if ClientDetail.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Generate a unique user_id
        user_id = uuid.uuid4().hex[:8]

        # Set date_joined to now and last_login to two days from now
        date_joined = timezone.now()
        last_login = date_joined + timedelta(days=2)

        # Create the ClientDetail instance with user_active set to True
        try:
            user = ClientDetail.objects.create(
                user_id=user_id,
                email=email,
                password=password,  # Store password as entered
                date_joined=date_joined,
                last_login=last_login,
                user_active=True,  # Set user_active to True
            )
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Replace 'login' with your login URL name
        except Exception as e:
            print(f"Error during registration: {e}")
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('register')

    return render(request, 'client_register.html')


# ==============================================================kyc=================================================

# ==============================================================kyc=================================================
''' ============================ signup and KYC method start =============================  '''
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ClientDetail
from django.utils import timezone
import uuid
def signup_view(request):
    if request.method == 'POST':
        name_first = request.POST['name_first']
        name_last = request.POST['name_last']
        phone_number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        country = request.POST['country']
        city = request.POST['city']
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Check if email already exists
        if ClientDetail.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')

        else:
            # Create a new client
            client_detail = ClientDetail(
                user_id=uuid.uuid4().hex[:8], 
                name_first=name_first, 
                name_last=name_last, 
                email=email, 
                password=password, 
                phone_number=phone_number, 
                country=country, 
                city=city,
                date_joined=timezone.now(),
                last_login=timezone.now(),
                verify_code=code 
            )
            
            # messages.success(request, 'Account created successfully.')
            # Redirect to the broker selection page
        #    return redirect('kyc_video_upload')  # Make sure 'broker_selection' is the correct URL name
            subject = 'Hello send verify code!'
            message = f'Verification code is .{code}'
            email_from = settings.EMAIL_HOST_USER
            client_email = [email]  # Add recipient email addresses here
          
            try:
                send_mail(subject, message, email_from, client_email)
                client_detail.save()
                request.session['client_email'] = client_detail.email
                return redirect('verify')
            
            except Exception as e:
                messages.error(request, 'Otp send faild')
                    # You can log the error e here if needed
                return redirect('signup')

    return render(request, 'signup.html')


''' ============================= Email verify ============================================='''

def register_verify(request):
    # return render(request,'register_verify.html',)
    email = request.session.get('client_email')
    print(f' otp = {email}')
    try:
        user = ClientDetail.objects.get(email=email)
        if request.method == 'POST':     
            code = request.POST.get('code')
            print(code)
            if user.verify_code == code:
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
    return render(request,'register_verify.html',{'msg':f'The verification code in {email}.'})

##############################################################################################


# '''  ===================================  Document verified ====================================='''

# last finl

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import pytesseract
import pdfplumber
from fuzzywuzzy import fuzz
from io import BytesIO
from .forms import NationalIDForm
from .models import ClientDetail, KYC
import fitz  # PyMuPDF for handling PDF
from PIL import Image


# Tesseract ka path specify karen
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from a PDF file
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

# Function to extract text from a PDF file directly (if no OCR is needed)
def extract_text_from_pdf(pdf_file):
    images = pdf_to_images(pdf_file)
    extracted_text = extract_text_from_images(images)
    return extracted_text

# Function to normalize extracted text (e.g., remove special characters)
def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)  # Remove all special characters
    return text.strip().lower()  # Convert to lower case and strip leading/trailing whitespace

def upload_national_id(request):
    email = request.session.get('client_email')
    if not email:
        messages.error(request, "Email is missing from the session. Please login again.")
        return redirect('/')

    client, created = ClientDetail.objects.get_or_create(
        email=email,
        defaults={
            'date_joined': timezone.now(),
            'last_login': timezone.now(),
        }
    )
    kyc, created = KYC.objects.get_or_create(client=client)

    if request.method == 'POST':
        form = NationalIDForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            national_id_file = form.cleaned_data['national_id']
            national_id_name = form.cleaned_data['national_id_name']
            national_id_number = form.cleaned_data['national_id_number']

            file_extension = national_id_file.name.split('.')[-1].lower()
            extracted_text = ""

            if file_extension == 'pdf':
                extracted_text = extract_text_from_pdf(national_id_file)
            elif file_extension in ['jpeg', 'jpg', 'png']:
                extracted_text = pytesseract.image_to_string(Image.open(national_id_file))
            else:
                messages.error(request, "Invalid file format. Please upload a PDF or an image.")
                return render(request, 'kyc/upload_national_id.html', {'form': form})

            normalized_text = normalize_text(extracted_text)
            combined_input = f"{national_id_name} {national_id_number}".lower()
            match_ratio = fuzz.token_set_ratio(combined_input, normalized_text)

            if match_ratio >= 10:
                form.save()
                messages.success(request, "ID uploaded successfully!")
                return redirect('agreement')  # Replace with the next URL
            else:
                messages.error(request, f"ID does not match uploaded document. Match ratio: {match_ratio}%")
    else:
        form = NationalIDForm()

    return render(request, 'kyc/upload_national_id.html', {'form': form})

#####################################################################################################    
''' ============================= upload_national_id 2st============================================='''

#####################################################################################################  

##############################################################################################
''' ============================= agreement accept ==================================='''
# views.py
from .forms import AgreementForm
from xhtml2pdf import pisa

def agreement_view(request):
    email = request.session.get('client_email')
    if not email:
        return redirect('kyc_start')  # Redirect if the email is missing

    client = ClientDetail.objects.get(email=email)
    kyc = KYC.objects.get(client=client)

    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            kyc.agreement_signed = form.cleaned_data['agreement_signed']
            kyc.terms_accepted = form.cleaned_data['terms_accepted']

            # Generate and save the PDF
            context = {
                'client': client,
                'kyc': kyc,
            }
            html = render_to_string('kyc/agreement.html', context)
            pdf_file = ContentFile(b"")  # Create an empty content file
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)

            if not pisa_status.err:  # Save the PDF if no errors occurred
                file_name = f"agreement_{client.id}.pdf"
                kyc.agreement_file.save(file_name, pdf_file)

            kyc.save()
            return redirect('video_verification')  # Redirect to the next step
    else:
        form = AgreementForm()

    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'kyc/agreement.html', context)

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse

def download_pdf(request):
    # Configure pdfkit with the correct path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    email = request.session.get('client_email')
    client = ClientDetail.objects.get(email=email)
    kyc = KYC.objects.get(client=client)

    base_url = request.build_absolute_uri('/')[:-1]

    context = {
        'client': client,
        'kyc': kyc,
        'base_url': base_url,
    }

    html = render_to_string('kyc/agreement.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="agreement.pdf"'

    pdf = pdfkit.from_string(
        html,
        output_path=False,
        configuration=config,
        options={
            'page-size': 'A4',
            'enable-local-file-access': None,
        },
    )
    response.write(pdf)
    return response

''' ============================= video uplod ==================================='''


import os
from django.shortcuts import render
from moviepy.editor import VideoFileClip  # Ensure this line is present
import speech_recognition as sr
from .models import ClientDetail, KYC
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


def video_verification_view(request):
    email = request.session.get('client_email')
    client = ClientDetail.objects.get(email=email)
   # text_to_compare = 'I confirm that this is a KYC submission.'
    text_to_compare = f"I, {client.name_first} {client.name_last}, confirm that I have read understood and accept all terms and conditions."


    if request.method == 'POST':
        try:
            client = ClientDetail.objects.get(email=email)
            data = json.loads(request.body)
            video_base64 = data.get('video')

            if video_base64:

                f , video_s = video_base64.split(';base64,')
                e = f.split('/')[-1]
                video_d = ContentFile(base64.b64decode(video_s), name=f'{client.name_first}kyc_video{client.user_id}.{e}')
                video_p = os.path.join('path_to_save', video_d.name)  # Set the path to save the video
                
                # Save video to the database
                kyc_obj = KYC.objects.get(client__user_id=client.user_id)
                kyc_obj.video_file = video_d
                kyc_obj.video_verification_done = False  # Initially set to False
                kyc_obj.save()
                # Decode the base64 video
                format, video_str = video_base64.split(';base64,')
                video_data = base64.b64decode(video_str)
                
                # Save the video temporarily in the MEDIA_ROOT directory
                with tempfile.NamedTemporaryFile(suffix='.webm', dir=settings.MEDIA_ROOT, delete=False) as temp_video_file:
                    temp_video_file.write(video_data)
                    video_path = temp_video_file.name

                # Step 1: Extract audio directly from WebM video using ffmpeg
                audio_path = extract_audio_from_video(video_path, client.name_first)
                if not audio_path:
                    messages.success(request, "Error extracting audio from video.")

                    return JsonResponse({'success': False, 'error': 'Error extracting audio from video.'})

                # Step 2: Convert the audio to text
                extracted_text = transcribe_audio_to_text(audio_path)
                print(f'Extracted Text: {extracted_text}')
                print(f'Text to Compare: {text_to_compare}')

                # Step 3: Compare extracted text with predefined text
                from fuzzywuzzy import fuzz
                match_ratio = fuzz.token_set_ratio(extracted_text, text_to_compare)
                print(f'Fuzzy match ratio: {match_ratio}')

                # Step 4: If match ratio is above a threshold (e.g., 90)
                if match_ratio > 5:
                    # KYC verification successful
                    kyc_obj = KYC.objects.get(client__user_id=client.user_id)
                    kyc_obj.video_verification_done = True
                    kyc_obj.save()

                    return JsonResponse({'success': True})
                else:
                    messages.success(request, "Audio did not match the expected text.")
                    return JsonResponse({'success': False, 'error': 'Audio did not match the expected text.'})

            else:
                messages.success(request, "Video data not found.")
                return JsonResponse({'success': False, 'error': 'Video data not found.'})
        except Exception as e:
            messages.success(request, "Error .")
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        return render(request, 'kyc/video_verification.html', {'text': text_to_compare})


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

def submit_kyc(request):
    email = request.session.get('client_email')

 # Redirect to the first step if the email is missing

    client = ClientDetail.objects.get(email=email)
    kyc = KYC.objects.get(client=client)

    if kyc.agreement_signed and kyc.terms_accepted and kyc.video_verification_done:
        # KYC process completed, show a confirmation or send an email if required
        client.user_active = True
        client.save()
        subject = 'Hello send verify Completed!'
        message = f'Verification Completed'
        email_from = settings.EMAIL_HOST_USER
        client_email = [email]  # Add recipient email addresses here
        send_mail(subject, message, email_from, client_email)
        messages.success(request, "KYC verified and Signup successfully!")
        return render(request, 'kyc/kyc_completed.html')

    return redirect('video_verification')  # Redirect back to the start if KYC not completed


def broker_selection_view(request):
    # Handle window close detection and session management for 'Next Step' button
    if 'window_closed' not in request.GET:
        request.session['show_next_step'] = False  # Ensure 'Next Step' button is hidden on initial load

    # Check if the window has been closed based on the query parameter
    if request.GET.get('window_closed') == 'true':
        request.session['show_next_step'] = True

    show_next_step = request.session.get('show_next_step', False)

    # Handle the broker selection process
    if request.method == 'POST':
        selected_broker = request.POST.get('broker')
        client_email = request.POST.get('email')
        # Save the selected broker and email to the session
        request.session['client_email'] = client_email
        client, created = ClientDetail.objects.get_or_create(
            email=client_email,
            defaults={'broker': selected_broker}
        )
        if not created:
            client.broker = selected_broker
            client.save()

        # Redirect to KYC step 1 (National ID Upload)
        return redirect('submit_kyc')

    return render(request, 'broker_selection.html', {'show_next_step': show_next_step})


###########################################################################################
###########################################################################################

###########################################################################################
###########################################################################################



"=================================================================================================================================="

#       Add google login method kuch settings.py me ye aur googgle acount per seting karne pade gi 

"=================================================================================================================================="
'''

###############  add setting.py 

GOOGLE_REDIRECT_URI_LOGIN = 'http://localhost:8000/accounts/google/callback/'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default backend
)

LOGIN_REDIRECT_URL = '/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout


'''

import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login


from django.shortcuts import redirect
from django.conf import settings

def google_login(request):
    state = request.GET.get('state', 'login')  # Default state is 'login'

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
        f'?response_type=code'
        f'&client_id={settings.GOOGLE_CLIENT_ID}'
        f'&redirect_uri={settings.GOOGLE_REDIRECT_URI_LOGIN}'
        f'&scope=profile email'
        f'&access_type=offline'
        f'&state={state}'
    )
    return redirect(google_auth_url)

import random
import string

import requests
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from .models import ClientDetail, Client_SYMBOL_QTY, SYMBOL

def google_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state', 'login')  # Default state is 'login'

    if not code:
        messages.error(request, 'Authorization code not received.')
        return redirect('/?msg=Authorization code not received')

    try:
        # Exchange code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI_LOGIN,
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()  # Raise an error for bad responses
        token_info = token_response.json()

        access_token = token_info.get('access_token')
        if not access_token:
            messages.error(request, 'Failed to retrieve access token.')
            return redirect('/?msg=Failed to retrieve access token')

        # Fetch user info
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        user_info_params = {'access_token': access_token}
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info_response.raise_for_status()  # Raise an error for bad responses
        user_info = user_info_response.json()

        email = user_info.get('email')
        name = user_info.get('name')

        if not email:
            messages.error(request, 'Failed to retrieve user information.')
            return redirect('/?msg=Failed to retrieve user information')

        # Registration flow
        if state == 'register':
            user, created = ClientDetail.objects.get_or_create(
                email=email,
                defaults={
                    'name_first': name,
                    'date_joined': now(),
                    'last_login': now(),
                }
            )
            if created:
                user.password = generate_random_password(length=6)
                user.save()
                messages.success(request, 'User registered successfully.')
                request.session['client_email'] = user.email
                return redirect('upload_national_id')
            else:
                messages.info(request, 'User already exists. Please log in.')
                return redirect('/?msg=User already exists. Please log in.')

        # Login flow
        elif state == 'login':
            try:
                user = ClientDetail.objects.get(email=email)
                if user.user_active:
                    request.session['user_id'] = user.user_id

                    if user.last_login and user.last_login.date() >= now().date():
                        initialize_client_symbols(user)
                        for symbol in SYMBOL.objects.all():
                            Client_SYMBOL_QTY.objects.get_or_create(
                                client_id=user.user_id,
                                SYMBOL=symbol.SYMBOL,
                                defaults={'QUANTITY': 0}
                            )
                        return redirect('/Analysis/')
                    else:
                        return redirect('/?msg=Your plan has expired.')
                else:
                    request.session['client_email'] = user.email
                    return redirect('upload_national_id')
            except ClientDetail.DoesNotExist:
                messages.error(request, 'User does not exist. Please register.')
                return redirect('/?msg=User does not exist. Please register.')

        # Invalid state
        else:
            messages.error(request, 'Invalid state parameter.')
            return redirect('/?msg=Invalid state parameter')

    except requests.RequestException as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('/?msg=An error occurred while processing your request.')

    except Exception as e:
        messages.error(request, f'Unexpected error: {str(e)}')
        return redirect('/?msg=An unexpected error occurred.')



######################################################################################
    
    
'''==============================facbook login method ==============================='''   

'''
# Facebook Settings.py
FACEBOOK_CLIENT_ID = 'your-facebook-app-id'
FACEBOOK_CLIENT_SECRET = 'your-facebook-app-secret'
FACEBOOK_REDIRECT_URI_LOGIN = 'https://your-domain.com/facebook/callback/'

'''

def facebook_login(request):
    print(f'facebook_login = {facebook_login}')
    # State ko pass karein, 'login' default state ke saath
    state = request.GET.get('state', 'login')  # Default state 'login'

    facebook_auth_url = (
        'https://www.facebook.com/v13.0/dialog/oauth'
        f'?client_id={settings.FACEBOOK_CLIENT_ID}'
        f'&redirect_uri={settings.FACEBOOK_REDIRECT_URI_LOGIN}'
        f'&state={state}'
        f'&scope=email,public_profile'
    )
    return redirect(facebook_auth_url)




def facebook_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state', 'login')
    if not code:
        messages.error(request, 'Authorization code nahi mila')
        return redirect('/?msg=Authorization code nahi mila')

    # Access token ke liye request karna
    token_url = 'https://graph.facebook.com/v13.0/oauth/access_token'
    token_data = {
        'client_id': settings.FACEBOOK_CLIENT_ID,
        'client_secret': settings.FACEBOOK_CLIENT_SECRET,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URI_LOGIN,
        'code': code,
    }
    token_r = requests.get(token_url, params=token_data)
    token_info = token_r.json()

    access_token = token_info.get('access_token')

    if not access_token:
        messages.error(request, 'Access token nahi mila')
        return redirect('/?msg=Access token nahi mila')

    # User information fetch karna
    user_info_url = 'https://graph.facebook.com/me'
    user_info_params = {
        'fields': 'id,name,email',
        'access_token': access_token,
    }
    user_info_r = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_r.json()

    email = user_info.get('email')
    name = user_info.get('name')
    facebook_user_id = user_info.get('id')

    if not email:
        messages.error(request, 'User info nahi mila')
        return redirect('/?msg=User info nahi mila')

    if state == 'register':
        # Register ka process
        user, created = ClientDetail.objects.get_or_create(email=email, defaults={
            'name_first': name,
            'date_joined': timezone.now(),
            'last_login': timezone.now() + timedelta(days=1),
        })

        if created:
            pp = generate_random_password(length=6)
            user.password = pp
            user.save()
            messages.success(request, 'User successfully registered')
            request.session['client_email'] = user.email
            return redirect('upload_national_id')
        else:
            messages.info(request, 'User already exists')

    elif state == 'login':
        # Login ka process
        try:
            user = ClientDetail.objects.get(email=email)
            if user.user_active:
                request.session['user_id'] = user.user_id
                if user.last_login and user.last_login.date() >= timezone.now().date():
                    initialize_client_symbols(user)
                    alls = SYMBOL.objects.all()
                    for s in alls:
                        Client_SYMBOL_QTY.objects.get_or_create(
                            client_id=user.user_id,
                            SYMBOL=s.SYMBOL,
                            defaults={'QUANTITY': 0}
                        )
                    return redirect('/Analysis/')
                else:
                    return redirect('/?msg=Your plan has expired')
            else:
                request.session['client_email'] = user.email
                return redirect('upload_national_id')

        except ClientDetail.DoesNotExist:
            messages.error(request, 'User nahi mila. Please register.')
            return redirect('/?msg=User nahi mila Please register and Sign up')

    else:
        messages.error(request, 'Invalid state parameter')
        return redirect('/?msg=Invalid state parameter')

###############################################################################################################
import requests
import random
import string
import hashlib
import base64
import os
from datetime import timedelta
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.utils import timezone



# ======================  TWITTER Login Method ================

# Generate code verifier and challenge for PKCE
def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

# Generate random password for new users
def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Twitter Login View
def twitter_login(request):
    state = request.GET.get('state', 'login')  # Default to 'login' state

    # Generate PKCE code verifier and challenge
    code_verifier, code_challenge = generate_code_verifier_and_challenge()
    request.session['code_verifier'] = code_verifier  # Store verifier in the session for later

    # Twitter authorization URL
    twitter_auth_url = (
        'https://twitter.com/i/oauth2/authorize'
        f'?response_type=code'
        f'&client_id={settings.TWITTER_CLIENT_ID}'
        f'&redirect_uri={settings.TWITTER_REDIRECT_URI_LOGIN}'
        f'&scope=tweet.read users.read'
        f'&state={state}'  # Pass state parameter (login/register)
        f'&code_challenge_method=S256'
        f'&code_challenge={code_challenge}'  # Use the generated code challenge
    )
    return redirect(twitter_auth_url)


# Twitter Callback View
def twitter_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state', 'login')  # Default to 'login' state
    code_verifier = request.session.get('code_verifier')

    # Debugging print statements
    print(f'code = {code}')
    print(f'state = {state}')
    print(f'code_verifier = {code_verifier}')

    if not code or not code_verifier:
        messages.error(request, 'Authorization code or code verifier not found')
        print('Error: Authorization code or code verifier not found')
        return redirect('/?msg=Authorization code or code verifier not found')

    # Convert authorization code to tokens
    token_url = 'https://api.twitter.com/2/oauth2/token'
    token_data = {
        'code': code,
        'client_id': settings.TWITTER_CLIENT_ID,
        'client_secret': settings.TWITTER_CLIENT_SECRET,
        'redirect_uri': settings.TWITTER_REDIRECT_URI_LOGIN,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier,
        'scope': 'users.read tweet.read'  # Include necessary scopes
    }

    # Request access token
    print(f'Requesting access token with data: {token_data}')
    token_r = requests.post(token_url, data=token_data)

    # Debugging response from token request
    print(f'Token response status = {token_r.status_code}')
    print(f'Token response content = {token_r.content}')

    if token_r.status_code != 200:
        messages.error(request, 'Failed to get access token')
        print('Error: Failed to get access token')
        return redirect('/?msg=Failed to get access token')

    token_info = token_r.json()
    access_token = token_info.get('access_token')

    print(f'access_token = {access_token}')

    if not access_token:
        messages.error(request, 'Failed to retrieve access token')
        print('Error: Failed to retrieve access token')
        return redirect('/?msg=Failed to retrieve access token')

    # Fetch user information from Twitter
    user_info_url = 'https://api.twitter.com/2/users/me'  # Correct endpoint for user info
   # user_info_url = 'https://api.twitter.com/2/users/me?user.fields=email' 
    user_info_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    #Debugging user info request
    print(f'Requesting user info with headers: {user_info_headers}')
    user_info_r = requests.get(user_info_url, headers=user_info_headers)

    # Debugging response from user info request
    print(f'User info response status = {user_info_r.status_code}')
    print(f'User info response content = {user_info_r.content}')

    if user_info_r.status_code != 200:
        messages.error(request, 'Failed to fetch user info')
        print('Error: Failed to fetch user info')
        return redirect('/?msg=Failed to fetch user info')

    user_info = user_info_r.json()

    # Extract email and other user data
    id = user_info['data'].get('id')  # Access email
    username = user_info['data'].get('username')  # Access email
    email = user_info['data'].get('email')  # Access email
    name = user_info['data'].get('name')    # Access name

    print(f'user_info = {user_info}')

    if not email:
        messages.error(request, f'Failed to get all user info {user_info}')
        print('Error: Failed to get user info - Email not found')
        return redirect('/?msg=Failed to get user info')

    # Handle registration or login based on the state
    if state == 'register':
        print(f'Registering user with email: {email} and name: {name}')
        user, created = ClientDetail.objects.get_or_create(email=email, defaults={
            'name_first': name,
            'date_joined': timezone.now(),
            'last_login': timezone.now() + timedelta(days=1),
        })

        if created:
            # Generate a random password and save the user
            pp = generate_random_password(length=6)
            user.password = pp
            user.save()
            messages.success(request, 'User registered successfully')
            request.session['client_email'] = user.email
            print('User registered successfully')
            return redirect('upload_national_id')
        else:
            messages.info(request, 'User already exists')
            print('User already exists')

    elif state == 'login':
        print(f'Logging in user with email: {email}')
        try:
            user = ClientDetail.objects.get(email=email)
            # Check if the user is active
            if user.user_active:
                request.session['user_id'] = user.user_id

                # Check if the user's plan is still valid
                if user.last_login and user.last_login.date() >= timezone.now().date():
                    initialize_client_symbols(user)
                    alls = SYMBOL.objects.all()
                    for s in alls:
                        Client_SYMBOL_QTY.objects.get_or_create(
                            client_id=user.user_id,
                            SYMBOL=s.SYMBOL,
                            defaults={'QUANTITY': 0}
                        )
                    print('Redirecting to Analysis page')
                    return redirect('/Analysis/')
                else:
                    print('Error: User plan has expired')
                    return redirect('/?msg=Your plan has expired')
            else:
                request.session['client_email'] = user.email
                print('Redirecting to upload national ID')
                return redirect('upload_national_id')

        except ClientDetail.DoesNotExist:
            messages.error(request, 'User does not exist. Please register.')
            print('Error: User does not exist. Prompting registration.')
            return redirect('/?msg=User does not exist Please register and Sign up')

    else:
        messages.error(request, 'Invalid state parameter')
        print('Error: Invalid state parameter')
        return redirect('/?msg=Invalid state parameter') 
        
        
   
# from django.shortcuts import render, get_object_or_404, redirect
# from .forms import ClientDetailForm
# from .models import ClientDetail, Broker
# from django.views.decorators.csrf import csrf_protect
# from django.contrib import messages  # For feedback messages
# from django.db import transaction  # To manage atomic transactions

# @csrf_protect
# def broker_connect(request):
#     user_id = request.session.get('user_id')
#     print(f'User ID: {user_id}')
    
#     # Fetch client details or return a 404 if not found
#     client = get_object_or_404(ClientDetail, user_id=user_id)
#     brokers = Broker.objects.all()

#     # Broker-specific server lists
#     server_lists = {
#         "Exness": [
#             "Exness-MT5Real2", "Exness-MT5Real3", "Exness-MT5Real4", "Exness-MT5Real5",
#         "Exness-MT5Real6", "Exness-MT5Real7", "Exness-MT5Real8", "Exness-MT5Real9",
#         "Exness-MT5Real10", "Exness-MT5Real11", "Exness-MT5Real12", "Exness-MT5Real13",
#         "Exness-MT5Real14", "Exness-MT5Real15", "Exness-MT5Real16", "Exness-MT5Real17",
#         "Exness-MT5Real18", "Exness-MT5Real19", "Exness-MT5Real20", "Exness-MT5Real21",
#         "Exness-MT5Real22", "Exness-MT5Real23", "Exness-MT5Real24", "Exness-MT5Real25",
#         "Exness-MT5Real26", "Exness-MT5Real27", "Exness-MT5Trial2", "Exness-MT5Trial6",
#         "Exness-MT5Trial7", "Exness-MT5Trial14", "Exness-MT5Trial4", "Exness-MT5Trial8",
#         "Exness-MT5Trial5", "Exness-MT5Trial19", "Exness-MT5Trial10", "Exness-MT5Trial15",
#         ],
#         "MultiBankFX": [
#                     ],
#         "Octafx": [
           
#         ],
#         "XM Global": [
           
#         ],
#         "Ya Group Ltd": [
#         "YaGroup-Server",
#         ],
#         "IMPERIALSOLUTIONS": [
#         "ACCESS SERVER 1",
#         ],
#     }

#     if request.method == 'POST':
#         mt5_login = request.POST.get('mt5_login')
#         mt5_password = request.POST.get('mt5_password')
#         broker_id = request.POST.get('broker')
#         mt5_server = request.POST.get('mt5_server')

#         # Validate MT5 server
#         broker_name = Broker.objects.get(id=broker_id).broker
#         if mt5_server not in server_lists.get(broker_name, []):
#             messages.error(request, "Invalid MT5 server selected.")
#             return redirect('Analysis')

#         try:
#             broker_instance = Broker.objects.get(id=broker_id)
#         except Broker.DoesNotExist:
#             messages.error(request, "Selected broker does not exist.")
#             return redirect('Analysis')
        
#         try:
#             with transaction.atomic():
#                 user = ClientDetail.objects.get(user_id=user_id)
#                 user.mt5_login = mt5_login
#                 user.mt5_password = mt5_password
#                 user.broker = broker_instance
#                 user.mt5_server = mt5_server
#                 user.save()
#                 messages.success(request, "Broker connected successfully.")
#                 return redirect('Analysis')
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")
#     else:
#         form = ClientDetailForm(instance=client)

#     return render(request, 'broker_connect.html', {
#         'form': form,
#         'brokers': brokers,
#         'server_lists': server_lists,
#         'user_id': user_id,
#     })


# =========================================================================================
# =========================================================================================
from subadmin.models import sub_adminDT
from myapp.forms import SubadminForm

# def subadmin_list(request):
#     if not request.user.is_authenticated:
#         return redirect('admin_login')
#     # if 'subadmin_id' in request.session:  
#     subadmins = sub_adminDT.objects.all() 
#     if 'subadmin_id' in request.session:
#         del request.session['subadmin_id']
#     return render(request, 'subadmin_list.html', {'subadmins': subadmins})    
#     # else:
#     #     return redirect('/admin/?msg=Login')
    
from django.shortcuts import render, redirect, get_object_or_404
from subadmin.models import sub_adminDT
from .forms import SubadminForm

def subadmin_list(request):
    """View to list all sub-admins"""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    subadmins = sub_adminDT.objects.all()
    return render(request, 'subadmin_list.html', {'subadmins': subadmins})

from django.shortcuts import render, get_object_or_404, redirect
from subadmin.models import sub_adminDT
from subadmin.forms import SubadminForm

# Create View
def subadmin_create(request):
    if request.method == 'POST':
        form = SubadminForm(request.POST, request.FILES)  # Handle form data and files
        if form.is_valid():
            form.save()
            return redirect('subadmin_list')  # Replace with your list view URL name
    else:
        form = SubadminForm()

    return render(request, 'subadmin_form.html', {'form': form, 'title': 'Create Sub-admin'})

# Update View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from subadmin.models import sub_adminDT
from myapp.forms import SubadminForm

from django.shortcuts import get_object_or_404

def subadmin_update(request, pk):
    # Ensure pk matches the subadmin_id
    subadmin = get_object_or_404(sub_adminDT, subadmin_id=pk)

    if request.method == 'POST':
        form = SubadminForm(request.POST, request.FILES, instance=subadmin)
        if form.is_valid():
            form.save()
            return redirect('subadmin_list')  # Adjust this name if different
    else:
        form = SubadminForm(instance=subadmin)

    return render(request, 'subadmin_form_update.html', {'form': form, 'title': 'Update Sub-admin'})



def subadmin_delete(request, pk):
    subadmin = get_object_or_404(sub_adminDT, pk=pk)
    if request.method == 'POST':
        subadmin.delete()
        return redirect('subadmin_list')
    return render(request, 'subadmin_confirm_delete.html', {'subadmin': subadmin})


   
#  ====================== subadmin_view =========================
def subadmin_view(request,clint_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # if 'admin_id' not in request.session:
        # return redirect('/admin/?msg=Login')
    request.session['subadmin_id'] = clint_id
    return redirect('sub_dashboard')    


# =========================================================================================
# =========================================================================================
from subadmin.models import Subadmin_client_limit

from django.shortcuts import render, redirect, get_object_or_404
from subadmin.models import Subadmin_client_limit
from subadmin.forms import SubadminLimitForm

# List View
def Subadmin_client_limit_list(request):
    subadmins = Subadmin_client_limit.objects.all()
    return render(request, 'subadmin_limit_list.html', {'subadmins': subadmins})

# Create View
def subadmin_create_limit(request):
    if request.method == 'POST':
        form = SubadminLimitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Subadmin_client_limit_list')
    else:
        form = SubadminLimitForm()
    return render(request, 'subadmin_client_limit_form.html', {'form': form, 'title': 'Create Sub-admin'})

# Update View
def subadmin_update_limit(request, pk):
    try:
        subadmin = get_object_or_404(Subadmin_client_limit, pk=pk)
    except Exception as e:
        return render(request, 'error_page.html', {'message': str(e)})

    if request.method == 'POST':
        form = SubadminLimitForm(request.POST, instance=subadmin)
        if form.is_valid():
            form.save()
            return redirect('Subadmin_client_limit_list')
    else:
        form = SubadminLimitForm(instance=subadmin)
    return render(request, 'subadmin_client_limit_form.html', {'form': form, 'title': 'Update Sub-admin'})

# Delete View
def subadmin_delete_limit(request, pk):
    subadmin = get_object_or_404(Subadmin_client_limit, pk=pk)
    if request.method == 'POST':
        subadmin.delete()
        return redirect('Subadmin_client_limit_list')
    return render(request, 'subadmin_confirm_limit_delete.html', {'subadmin': subadmin})

# Update View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from subadmin.models import sub_adminDT
from myapp.forms import SubadminForm

def subadmin_update(request, pk):
    # Use get_object_or_404 to handle missing objects
    subadmin = get_object_or_404(sub_adminDT, subadmin_id=pk)

    if request.method == 'POST':
        form = SubadminForm(request.POST, request.FILES, instance=subadmin)
        if form.is_valid():
            form.save()
            return redirect('subadmin_list')  # Adjust as per your actual list view name
    else:
        form = SubadminForm(instance=subadmin)

    return render(request, 'subadmin_form_update.html', {'form': form, 'title': 'Update Sub-admin'})

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from myapp.models import ClientDetail

def client_pay_payment(request):
    # Ensure user is authenticated
    # if not request.user.is_authenticated:
    #     return redirect('admin_login')
    
    # # Retrieve the client based on the authenticated user
    # try:
    #     client_user = ClientPaymetns.objects.get(clint_id=request.user.id)
    # except ClientPaymetns.DoesNotExist:
    #     return redirect('error_page')  # Redirect if client not found

    # today = timezone.now().date()
    # message = None

    # # Check for payment status and subscription period
    # if not client_user.payment:
    #     message = 'Please complete the payment to proceed.'
    # elif client_user.clint_payment_from_date.date() < today:
    #     message = 'Your payment period has expired. Please renew your subscription.'

    # context = {
    #     'client_user': client_user,
    #     'message': message
    # }
    return render(request, 'Payment.html')  




     
# ==========================================================================
# ==========================================================================      

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import KYC
from django.template.loader import get_template
from xhtml2pdf import pisa  # To generate PDF
from django.db.models import Q  # Correctly import Q



def kyc_list(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search_query = request.GET.get('search_query', '')

    kyc_records = KYC.objects.all()

    if from_date and to_date:
        kyc_records = kyc_records.filter(national_id_issue_date__range=[from_date, to_date])

    if search_query:
        kyc_records = kyc_records.filter(
            Q(national_id_number__icontains=search_query) |
            Q(national_id_name__icontains=search_query)
        )

    return render(request, 'kyc_list.html', {
        'kyc_records': kyc_records,
        'from_date': from_date,
        'to_date': to_date,
        'search_query': search_query
    })


def download_pdf_kyc(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    kyc_records = KYC.objects.all()

    if from_date and to_date:
        kyc_records = kyc_records.filter(national_id_issue_date__range=[from_date, to_date])

    template = get_template('kyc_pdf.html')
    context = {'kyc_records': kyc_records, 'from_date': from_date, 'to_date': to_date}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="kyc_records.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF', status=500)
    
    return response


def kyc_delete(request, pk):
    kyc = get_object_or_404(KYC, pk=pk)
    if request.method == 'POST':
        kyc.delete()
        return redirect('kyc_list')
    return render(request, 'kyc_delete.html', {'kyc': kyc})



# ==========================================================================
# ==========================================================================      

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import offers_subadmin
from .forms import SubadminOffersForm

def subadmin_offers_list(request):
    # if not request.user.is_authenticated:
    #     return redirect('admin_login')
    offers = offers_subadmin.objects.all()
    return render(request, 'subadmin_offers_list.html', {'offers': offers})

def subadmin_offer_add(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method == 'POST':
        form = SubadminOffersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subadmin_offers_list')
    else:
        form = SubadminOffersForm()
    return render(request, 'subadmin_offer_form.html', {'form': form, 'action': 'Add'})
   
     
def subadmin_offer_edit(request, pk):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    offer = get_object_or_404(offers_subadmin, pk=pk)
    if request.method == 'POST':
        form = SubadminOffersForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('subadmin_offers_list')
    else:
        form = SubadminOffersForm(instance=offer)
    return render(request, 'subadmin_offer_form.html', {'form': form, 'action': 'Edit'})


def subadmin_offer_delete(request, pk):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    offer = get_object_or_404(offers_subadmin, pk=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('subadmin_offers_list')
    return render(request, 'subadmin_offer_confirm_delete.html', {'offer': offer})

      
      
# ==========================================================================
# ==========================================================================      

# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse


# from .models import ClientDetail

# def fetch_client_mt5(request):
#     try:
#         user_id = request.session.get('user_id')
#         client_user = get_object_or_404(ClientDetail, user_id=user_id)

#         # Initialize connection to MT5
#         if not mt5.initialize(login=client_user.mt5_login, password=client_user.mt5_password, server=client_user.mt5_server):
#             return JsonResponse({'error': 'Failed to initialize MT5 connection'}, status=400)

#         # Fetch account information
#         account_info = mt5.account_info()
#         if account_info is None:
#             mt5.shutdown()
#             return JsonResponse({'error': 'Failed to retrieve account info'}, status=400)

#         # Shutdown MT5 connection
#         mt5.shutdown()

#         # Return account details, including sensitive data securely
#         return JsonResponse({
#             'account_number': client_user.mt5_login,
#             'server': client_user.mt5_server,
#             'password': client_user.mt5_password,  # Ensure this is handled securely
#             'balance': account_info.balance,
#             'equity': account_info.equity,
#             'margin': account_info.margin,
#             'margin_free': account_info.margin_free,
#             'margin_level': account_info.margin_level,
#         })
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)




from datetime import datetime

def download_trade_history_pdf(request):
    client_id = request.session.get('user_id')
    client = ClientDetail.objects.get(user_id=client_id)

    # Fetch the filtered trades as in your main view
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Define the date format (adjust this to match the format you're using)
    date_format = "%b. %d, %Y"

    try:
        start_date = datetime.strptime(start_date_str, date_format).date() if start_date_str else timezone.now().date()
        end_date = datetime.strptime(end_date_str, date_format).date() if end_date_str else timezone.now().date()
    except ValueError:
        # Handle invalid date format gracefully
        return HttpResponse("Invalid date format. Please use the correct format: Jan. 1, 2003", status=400)

    start_datetime = timezone.make_aware(timezone.datetime.combine(start_date, datetime.min.time()))
    end_datetime = timezone.make_aware(timezone.datetime.combine(end_date, datetime.max.time()))

    trades = TradeHistory.objects.filter(
        client__user_id=client_id,
        signal_time__range=(start_datetime, end_datetime)
    ).order_by('signal_time')

    cumulative_p_l = 0
    for trade in trades:
        trade.p_l = trade.p_l if trade.p_l else 0
        cumulative_p_l += trade.p_l
        trade.cumulative_p_l = cumulative_p_l

    # Render the trades into an HTML template
    template = get_template('trade_history_pdf.html')
    context = {
        'client': client,
        'trades': trades,
        'total_cumulative_p_l': cumulative_p_l,
        'start_date': start_date,
        'end_date': end_date,
    }
    html = template.render(context)

    # Generate PDF using WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trade_history_{client_id}.pdf"'

    HTML(string=html).write_pdf(response)
    return response



def simplex_payment(request):
        return render(request, 'simplex_pay.html')


#=======================================================================
#=================================================================================
#=========================Meta Api ================


import requests
from django.shortcuts import render
from django.http import JsonResponse

# MetaAPI Credentials
API_BASE_URL = "https://mt-client-api-v1.london.agiliumtrade.ai"
ACCOUNT_ID = "1183d296-105a-4221-9aa5-4c2366b2a8db"
API_ACCESS_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1MGJhMTFjNzExN2I0N2EzOWM2NDhmYjc5OGNiZjhjZCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7..."

def fetch_metaapi_data(request):
    headers = {
        "Authorization": f"Bearer {API_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Fetch account details
        account_url = f"{API_BASE_URL}/users/current/accounts/{ACCOUNT_ID}"
        account_response = requests.get(account_url, headers=headers)
        account_data = account_response.json()

        if 'error' in account_data:
            print(f"Account Error: {account_data['message']}")

        # Fetch open trades
        open_trades_url = f"{API_BASE_URL}/users/current/accounts/{ACCOUNT_ID}/openPositions"
        open_trades_response = requests.get(open_trades_url, headers=headers)
        open_trades_data = open_trades_response.json()

        if 'error' in open_trades_data:
            print(f"Open Trades Error: {open_trades_data['message']}")

        # Fetch trade history
        trade_history_url = f"{API_BASE_URL}/users/current/accounts/{ACCOUNT_ID}/history/orders"
        trade_history_response = requests.get(trade_history_url, headers=headers)
        trade_history_data = trade_history_response.json()

        if 'error' in trade_history_data:
            print(f"Trade History Error: {trade_history_data['message']}")

        context = {
            "account_details": account_data,
            "open_trades": open_trades_data,
            "trade_history": trade_history_data,
        }
        return render(request, "metaapi_dashboard.html", context)

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


'''================================================================================================================='''
#                                                  connect_to_metaapi start
'''================================================================================================================='''

'''================================================================================================================='''
#                                                  Mataapi connect async
'''================================================================================================================='''

import asyncio
from django.http import JsonResponse
from metaapi_cloud_sdk import MetaApi

# MetaApi credentials
TOKENrr = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzBiNjllYmNmNjJhMjE4NmUyNzJiNjI4MTA5NTY5OCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiI2NzBiNjllYmNmNjJhMjE4NmUyNzJiNjI4MTA5NTY5OCIsImlhdCI6MTczNjI1OTI0OH0.m8K7ba63QsTAubZqoTzDbTVRKlJepQs4ItPBPNmOSjKb5cPtfzwkzzEr3_bH486mKZMo57GtzsPHYVblM9WXxKkI-0HE1ToWnW3xA0hjwi4Wc33OeBV_zkJA7jEWat5aCp95bAXS7IaQYhXdvV2Soir3X7Eo-dTjy7GLboaqpZiqe-T-UL6abvGIccg8RzIvKDO3fdvjn1KlKwr4FQx3QAJTB_T7RKcV7c8JTi_uDeYH9rp7rssfCrfj_dszQKldZZGwLb24xDWJ2n0gdlBsw0jzzbpsMMMJTTFw67jcPiDb-DMK-RXrHEBLT89-tjlmcwd6IXOOe2cOsnwZuEsLLPW7Xp2tRvS1xpdk3Ooh_Ks7aXIGODM72NRpdR4RQJD6kTicDI2ewNi7VGbAmFut25AujeqU_TAsYTekwNqdvRJedgFpxt7aj04DBd--W772c0En4Tu-peXSz6yuygq6ZY9DGz2E88lljJ6FZCD4LFF23LXKJsxWCSnFoFJZoReYbcIFBD7zTKKtMvbK8UISw2PgxgjS8JYIonRmlhyuf-3jqOnIm7yFqWsddzZY5mTiz83UzzljVLMfh69qT0AskhwUm3JRqghkrynviS7-r_TK3vn6LYfIc0Em27vWUntrGvMLXQoSdlbprRR1FGuprOD6YWpBywgeTIepubqxhKU"
ACCOUNT_IDrr = "8300e2b5-72d5-4893-abc6-4f3c2198b977"

async def connect_to_metaapi_async(TOKEN ,ACCOUNT_ID ):
    api = MetaApi(TOKEN)
    try:
        # Get account details
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

        # Deploy the account if not deployed
        if account.state not in ['DEPLOYING', 'DEPLOYED']:
            await account.deploy()

        # Wait for broker connection
        await account.wait_connected()

        # Connect to RPC
        connection = account.get_rpc_connection()
        await connection.connect()

        # Wait for synchronization
        await connection.wait_synchronized()

        # Fetch account information
        account_info = await connection.get_account_information()
        print(f'account_info = {account_info}')

        # Return response
        return {
             "success": True,
            "account_info": account_info,
        }
    except Exception as e:
        return {"error": str(e)}


'''================================================================================================================='''
#                                                  connect_to_metaapi test url 
'''================================================================================================================='''


def metaapi_view(request):
    # Use asyncio to run the async function
    result = asyncio.run(connect_to_metaapi_async(TOKENrr, ACCOUNT_IDrr))
    return JsonResponse(result)

'''================================================================================================================='''
#                                                  connect_to_metaapi
'''================================================================================================================='''


def connect_to_metaapi(TOKEN, ACCOUNT_ID):
    return asyncio.run(connect_to_metaapi_async(TOKEN, ACCOUNT_ID))


'''================================================================================================================='''
#                                                  Mataapi form user enter
'''================================================================================================================='''


# ====================================client site=================================================

def mataapi_profile(request):
    if 'user_id' not in request.session:
        return redirect('login_client')  # Redirect to login if not logged in

    user_id = request.session.get('user_id')  # Get the user ID from the session
    client = ClientDetail.objects.get(user_id=user_id)
  #  data = connect_to_metaapi(client.MataApi_TOKEN, client.MataApi_ACCOUNT_ID)
    data = asyncio.run(connect_to_metaapi_async(client.MataApi_TOKEN, client.MataApi_ACCOUNT_ID))
    if data.get("success"):
        api_data = data
    else:
        api_data = {}    
    return render(request, 'mataapi_profile.html' ,{'api_data': api_data})



# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from metaapi_cloud_sdk import MetaApi
# import asyncio

# # Replace with your MetaApi credentials
# TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzBiNjllYmNmNjJhMjE4NmUyNzJiNjI4MTA5NTY5OCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiI2NzBiNjllYmNmNjJhMjE4NmUyNzJiNjI4MTA5NTY5OCIsImlhdCI6MTczNjI1OTI0OH0.m8K7ba63QsTAubZqoTzDbTVRKlJepQs4ItPBPNmOSjKb5cPtfzwkzzEr3_bH486mKZMo57GtzsPHYVblM9WXxKkI-0HE1ToWnW3xA0hjwi4Wc33OeBV_zkJA7jEWat5aCp95bAXS7IaQYhXdvV2Soir3X7Eo-dTjy7GLboaqpZiqe-T-UL6abvGIccg8RzIvKDO3fdvjn1KlKwr4FQx3QAJTB_T7RKcV7c8JTi_uDeYH9rp7rssfCrfj_dszQKldZZGwLb24xDWJ2n0gdlBsw0jzzbpsMMMJTTFw67jcPiDb-DMK-RXrHEBLT89-tjlmcwd6IXOOe2cOsnwZuEsLLPW7Xp2tRvS1xpdk3Ooh_Ks7aXIGODM72NRpdR4RQJD6kTicDI2ewNi7VGbAmFut25AujeqU_TAsYTekwNqdvRJedgFpxt7aj04DBd--W772c0En4Tu-peXSz6yuygq6ZY9DGz2E88lljJ6FZCD4LFF23LXKJsxWCSnFoFJZoReYbcIFBD7zTKKtMvbK8UISw2PgxgjS8JYIonRmlhyuf-3jqOnIm7yFqWsddzZY5mTiz83UzzljVLMfh69qT0AskhwUm3JRqghkrynviS7-r_TK3vn6LYfIc0Em27vWUntrGvMLXQoSdlbprRR1FGuprOD6YWpBywgeTIepubqxhKU"
# ACCOUNT_ID = "8300e2b5-72d5-4893-abc6-4f3c2198b977"




#============================================================= META API ORDER PLACE FUNCTION ===================================================
#============================================================= META API ORDER PLACE FUNCTION ===================================================
import asyncio
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from metaapi_cloud_sdk import MetaApi
from .models import ClientDetail

async def establish_connection(account_id, token):
    """
    Establish and return a MetaApi connection with deployment and synchronization checks.
    """
    api = MetaApi(token)
    account = await api.metatrader_account_api.get_account(account_id)

    if account.state not in ["DEPLOYING", "DEPLOYED"]:
        print("Deploying the account...")
        await account.deploy()
        await account.wait_connected()
    else:
        print("Account is already deployed.")

    # Connect to the account's RPC
    connection = account.get_rpc_connection()
    await connection.connect()

    # Wait until the account is fully synchronized
    print("Waiting for synchronization...")
    await connection.wait_synchronized(timeout_in_seconds=300)  # Increased timeout
    return connection

async def ensure_account_ready(api, account_id):
    """
    Ensures the MetaApi account is deployed, connected, and synchronized.
    """
    account = await api.metatrader_account_api.get_account(account_id)

    # Deploy the account if not already deployed
    if account.state not in ["DEPLOYING", "DEPLOYED"]:
        print("Deploying the account...")
        await account.deploy()

    # Wait for the account to connect to the broker
    await account.wait_connected()

    # Connect and synchronize
    connection = account.get_rpc_connection()
    await connection.connect()
    print("Waiting for synchronization...")
    await connection.wait_synchronized(timeout_in_seconds=300)  # Increased timeout
    return connection

async def execute_trade(connection, order_type, symbol, volume, price=None, stop_loss=None, take_profit=None, comment=None):
    """
    Execute a trade order in MetaApi.
    """
    try:
        if order_type.upper() == "MARKET_BUY":
            return await connection.create_market_buy_order(symbol, volume, stop_loss, take_profit, {"comment": comment})
        elif order_type.upper() == "MARKET_SELL":
            return await connection.create_market_sell_order(symbol, volume, stop_loss, take_profit, {"comment": comment})
        elif order_type.upper() == "LIMIT_BUY":
            if not price:
                raise ValueError("Price is required for limit buy orders.")
            return await connection.create_limit_buy_order(symbol, volume, price, stop_loss, take_profit, {"comment": comment})
        elif order_type.upper() == "LIMIT_SELL":
            if not price:
                raise ValueError("Price is required for limit sell orders.")
            return await connection.create_limit_sell_order(symbol, volume, price, stop_loss, take_profit, {"comment": comment})
        else:
            raise ValueError("Invalid order type.")
    except Exception as e:
        raise e

async def retry_execute_trade(connection, execute_func, retries=3):
    """
    Retry trade execution on failure.
    """
    for attempt in range(retries):
        try:
            result = await execute_func()
            return {"success": True, "result": result}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(5)  # Wait before retrying
            else:
                return {"success": False, "error": str(e)}

import asyncio
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from metaapi_cloud_sdk import MetaApi
from .models import ClientDetail, Client_SYMBOL_QTY

@sync_to_async
def get_client_symbol_qty(client_id, symbol):
    """
    Fetch the lot size (quantity) for a specific client and symbol.
    """
    symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=client_id, SYMBOL=symbol).first()
    return symbol_qty.QUANTITY if symbol_qty else 0.01  # Default to 0.01 if not set

@sync_to_async
def get_clients():
    """
    Fetch all active clients with valid MetaApi credentials.
    """
    return list(ClientDetail.objects.filter(MataApi_ACCOUNT_ID__isnull=False, MataApi_TOKEN__isnull=False))

async def save_trade_execution_log(client, symbol, order_type, volume, price, stop_loss, take_profit, comment, success, error_reason):
    # Replace with actual logic to save trade execution log
    # For demonstration, we'll just pass
    pass

@csrf_exempt 
def place_trade(request):
    """
    Handles trade form submission and places the trade in MetaApi for multiple accounts.
    Also logs success/failure for each client trade in TradeExecutionLog.
    Returns summary (success vs fail) + details.
    """
    if request.method == "POST":
        try:
            # Get form data
            symbol = request.POST.get("symbol")
            price = request.POST.get("price")
            price = float(price) if price else None
            order_type = request.POST.get("order_type")
            stop_loss = request.POST.get("stop_loss")
            stop_loss = float(stop_loss) if stop_loss else None
            take_profit = request.POST.get("take_profit")
            take_profit = float(take_profit) if take_profit else None
            comment = request.POST.get("comment")

            if not symbol or not order_type:
                return JsonResponse({"success": False, "error": "Symbol and order type are required."}, status=400)

            # Define asynchronous functions inside the view
            async def create_trade_history(client, symbol, trade_type, quantity, entry_price, ticket_id):
                return TradeHistory.objects.create(
                    client=client,
                    symbol=symbol,
                    trade_type=trade_type,
                    quantity=quantity,
                    entry_price=entry_price,
                    ticket_id=ticket_id,
                    # Add other fields if available
                )

            async def process_trade_for_client(client):
                """
                Processes trade for a single client:
                1. Gets lot size (volume)
                2. Establishes MetaApi connection
                3. Executes trade
                4. Logs result in the database
                5. Returns success/fail info
                """
                try:
                    volume = await get_client_symbol_qty(client.user_id, symbol)
                    connection = await establish_connection(client.MataApi_ACCOUNT_ID, client.MataApi_TOKEN)
                    
                    # Attempt trade
                    result = await execute_trade(connection, order_type, symbol, volume, price, stop_loss, take_profit, comment)
                    
                    # Extract necessary details from the result
                    ticket_id = result.get('orderId')
                    # As per user's requirement, use the posted price
                    entry_price = price if price is not None else result.get('price')

                    # Validate entry_price
                    if entry_price is None:
                        raise ValueError("Entry price could not be determined.")

                    # Save to TradeHistory asynchronously
                    # Django ORM operations are synchronous, so use sync_to_async
                    await sync_to_async(TradeHistory.objects.create)(
                        client=client,
                        symbol=symbol,
                        trade_type=order_type.upper(),
                        quantity=volume,
                        entry_price=entry_price,
                        ticket_id=ticket_id
                    )
                    
                    # Log success
                    await save_trade_execution_log(
                        client=client,
                        symbol=symbol,
                        order_type=order_type,
                        volume=volume,
                        price=price,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        comment=comment,
                        success=True,
                        error_reason=""
                    )
                    return {"client_id": client.user_id, "success": True, "result": result}

                except Exception as e:
                    # Log failure
                    await save_trade_execution_log(
                        client=client,
                        symbol=symbol,
                        order_type=order_type,
                        volume=volume if 'volume' in locals() else 0,  # Use attempted volume or 0
                        price=price,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        comment=comment,
                        success=False,
                        error_reason=str(e)
                    )
                    return {"client_id": client.user_id, "success": False, "error": str(e)}

            async def main():
                # Fetch all clients asynchronously
                clients = await get_clients()
                # Process trades concurrently
                return await asyncio.gather(*[process_trade_for_client(client) for client in clients])

            # Run the async loop
            results = asyncio.run(main())

            # Count how many trades succeeded vs. failed
            success_count = sum(1 for r in results if r["success"] is True)
            fail_count = len(results) - success_count

            # Return the data in JSON, including the breakdown
            return JsonResponse({
                "success": True,
                "total_trades": len(results),
                "success_count": success_count,
                "fail_count": fail_count,
                "results": results
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import asyncio

# @csrf_exempt 
# def place_trade(request):
#     """
#     Handles trade form submission and places the trade in MetaApi for multiple accounts.
#     Also logs success/failure for each client trade in TradeExecutionLog.
#     Returns summary (success vs fail) + details.
#     """
#     if request.method == "POST":
#         try:
#             # Get form data
#             symbol = request.POST.get("symbol")
#             price = float(request.POST.get("price")) if request.POST.get("price") else None
#             order_type = request.POST.get("order_type")
#             stop_loss = float(request.POST.get("stop_loss")) if request.POST.get("stop_loss") else None
#             take_profit = float(request.POST.get("take_profit")) if request.POST.get("take_profit") else None
#             comment = request.POST.get("comment")

#             async def process_trade_for_client(client):
#                 """
#                 Processes trade for a single client:
#                 1. Gets lot size (volume)
#                 2. Establishes MetaApi connection
#                 3. Executes trade
#                 4. Logs result in the database
#                 5. Returns success/fail info
#                 """
#                 try:
#                     volume = await get_client_symbol_qty(client.user_id, symbol)
#                     connection = await establish_connection(client.MataApi_ACCOUNT_ID, client.MataApi_TOKEN)
                    
#                     # Attempt trade
#                     result = await execute_trade(connection, order_type, symbol, volume, price, stop_loss, take_profit, comment)
                    
#                     # If we got here, success
#                     await save_trade_execution_log(
#                         client=client,
#                         symbol=symbol,
#                         order_type=order_type,
#                         volume=volume,
#                         price=price,
#                         stop_loss=stop_loss,
#                         take_profit=take_profit,
#                         comment=comment,
#                         success=True,
#                         error_reason=""
#                     )
#                     return {"client_id": client.user_id, "success": True, "result": result}

#                 except Exception as e:
#                     # Log failure
#                     await save_trade_execution_log(
#                         client=client,
#                         symbol=symbol,
#                         order_type=order_type,
#                         volume=0,  # or the volume we tried
#                         price=price,
#                         stop_loss=stop_loss,
#                         take_profit=take_profit,
#                         comment=comment,
#                         success=False,
#                         error_reason=str(e)
#                     )
#                     return {"client_id": client.user_id, "success": False, "error": str(e)}

#             async def main():
#                 # Fetch all clients asynchronously
#                 clients = await get_clients()
#                 # Process trades concurrently
#                 return await asyncio.gather(*[process_trade_for_client(client) for client in clients])

#             # Run the async loop
#             results = asyncio.run(main())

#             # Count how many trades succeeded vs. failed
#             success_count = sum(1 for r in results if r["success"] is True)
#             fail_count = len(results) - success_count

#             # Return the data in JSON, including the breakdown
#             return JsonResponse({
#                 "success": True,
#                 "total_trades": len(results),
#                 "success_count": success_count,
#                 "fail_count": fail_count,
#                 "results": results
#             })
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})

#     return JsonResponse({"success": False, "error": "Invalid request method."})

# views.py

from django.shortcuts import render
from .models import TradeExecutionLog, TradeCloseLog

def trade_summary(request):
    """
    Render a trade summary page showing success/fail counts for both execution and close trades.
    """
    # Execution trades summary
    execution_success_count = TradeExecutionLog.objects.filter(success=True).count()
    execution_fail_count = TradeExecutionLog.objects.filter(success=False).count()

    # Close trades summary
    close_success_count = TradeCloseLog.objects.filter(success=True).count()
    close_fail_count = TradeCloseLog.objects.filter(success=False).count()

    context = {
        # Execution trades
        "execution_success_count": execution_success_count,
        "execution_fail_count": execution_fail_count,
        # Close trades
        "close_success_count": close_success_count,
        "close_fail_count": close_fail_count,
    }
    return render(request, "trade_summary.html", context)

# views.py

def trade_log_details(request):
    """
    Render a single page showing trade logs (execution or close).
    """
    log_type = request.GET.get("log_type")  # 'execution' or 'close'
    success_filter = request.GET.get("success")  # '1' for success, '0' for failure

    if log_type == "execution":
        logs = TradeExecutionLog.objects.all()
    elif log_type == "close":
        logs = TradeCloseLog.objects.all()
    else:
        return render(request, "trade_log_details.html", {"logs": []})  # Invalid log_type

    # Apply success filter if provided
    if success_filter is not None:
        is_success = (success_filter == "1")
        logs = logs.filter(success=is_success)

    logs = logs.order_by("-timestamp")  # Order logs by latest

    return render(request, "trade_log_details.html", {"logs": logs, "log_type": log_type})



def trade_form(request):
    """
    Render the trade form page.
    """
    return render(request, "trade_form.html")


def get_market_price(request):
    """
    Fetch the market price for a given symbol.
    """
    symbol = request.GET.get("symbol")
    if not symbol:
        return JsonResponse({"success": False, "error": "Symbol is required"})

    async def fetch_price():
        try:
            # Replace with the appropriate account ID and token for fetching symbol prices
            account_id = "b8670f03-89f3-4968-ba8e-d0da431870a3"
            token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1MGJhMTFjNzExN2I0N2EzOWM2NDhmYjc5OGNiZjhjZCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Yjg2NzBmMDMtODlmMy00OTY4LWJhOGUtZDBkYTQzMTg3MGEzIl19LHsiaWQiOiJtZXRhYXBpLXJlc3QtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDpiODY3MGYwMy04OWYzLTQ5NjgtYmE4ZS1kMGRhNDMxODcwYTMiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOmI4NjcwZjAzLTg5ZjMtNDk2OC1iYThlLWQwZGE0MzE4NzBhMyJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOmI4NjcwZjAzLTg5ZjMtNDk2OC1iYThlLWQwZGE0MzE4NzBhMyJdfSx7ImlkIjoibWV0YXN0YXRzLWFwaSIsIm1ldGhvZHMiOlsibWV0YXN0YXRzLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDpiODY3MGYwMy04OWYzLTQ5NjgtYmE4ZS1kMGRhNDMxODcwYTMiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Yjg2NzBmMDMtODlmMy00OTY4LWJhOGUtZDBkYTQzMTg3MGEzIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiI1MGJhMTFjNzExN2I0N2EzOWM2NDhmYjc5OGNiZjhjZCIsImlhdCI6MTczODAzOTg2MSwiZXhwIjoxNzQ1ODE1ODYxfQ.EdLqCIYslHkRfRpL5nc2Jg_cXBgqOWLmlYfWWD0GBtbN3Ql1hHzsKxs2zslcWE3zvbVOY-MdYAL6nVQcsc6Uys38OMmZh-Pya2y4XIOjtT-euGxc0NweB7YSgtKCoy3VnyxVhrc4UD2qE2SkGLlZmxTXXrGArYoOiacaJqPdNhLENXMY64d4k8l_LRg5r7FL176i6z5-UjRz5FryVWs711nIl7Ag-WIsg_yAb_LdQqgWLl42ii6WixL2yC5qI4Qqqvt6rYvx8u0V-wcx4TvyWPMee1tdZbvto4rO49XHogpilWrF7FpJW_y3-_0HxI9wuhDL3olWfTdgjY2Nn9_nEJ5DXXIdn38iS1f01faotCRXoHPEDKiMJHuyAEtAZO3tOc9V4IyjWsdINszMf6ZpvxuwPXoaXMofTozPmcjOjzCLtSbLSNFuT_MoCAVC37mZDR23kbylbpPMY4zJ6mGwkXxWuiZjeWlTKAKUlegmZMzgH68vKNJpw0nAsvQ8ZnDJ5JOKnTTiobYnwhznX7tQr0WAbptBgFiBRkGh50KJx07ESGtcDi6nKR-_CBbUKfsCmrg7mQ4p2EKAiEhHirEUf7ANRscjpt1PVMWVdgg1iOBlQZQ-ItvmiMXNC3GkjoOyV2Qr4WJzth1Mmiy7Qoyhy5jxjxr0bV7DDdJGzt-PYn4"
            
            # Establish connection
            connection = await establish_connection(account_id, token)
            
            # Fetch price for the symbol
            tick = await connection.get_symbol_price(symbol)
            price = tick["ask"] if request.GET.get("order_type") == "MARKET_BUY" else tick["bid"]
            
            return {"success": True, "price": price}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Run the asynchronous function
    result = asyncio.run(fetch_price())
    return JsonResponse(result)


@sync_to_async
def save_close_trade_log(client, symbol, position_id, success, error_reason=""):
    """
    Saves a record of the trade close attempt to the database.
    """
    return TradeCloseLog.objects.create(
        client=client,
        symbol=symbol,
        position_id=position_id,
        success=success,
        error_reason=error_reason
    )


# ====================================================


async def close_open_trades_by_symbol(connection, symbol, client):
    """
    Close all open trades for the specified symbol, for a given client.
    Now logs success/failure in TradeCloseLog for each position.
    """
    try:
        open_positions = await connection.get_positions()
        symbol_positions = [position for position in open_positions if position["symbol"] == symbol]

        print(f"Open positions for {symbol}: {symbol_positions}")

        results = []
        for position in symbol_positions:
            position_id = position.get("id")

            if not position_id:
                results.append({
                    "error": f"Invalid position data. ID: {position_id}",
                    "position": position
                })
                # Log this failure
                await save_close_trade_log(
                    client=client,
                    symbol=symbol,
                    position_id=position_id or "N/A",
                    success=False,
                    error_reason="Position ID not found."
                )
                continue

            try:
                print(f"Attempting to close position {position_id} for symbol {symbol}...")
                result = await connection.close_position(position_id)
                
                # If no exception, success
                results.append({
                    "success": True,
                    "position_id": position_id,
                    "result": result
                })
                # Log success
                await save_close_trade_log(
                    client=client,
                    symbol=symbol,
                    position_id=position_id,
                    success=True
                )

            except Exception as close_error:
                error_details = getattr(close_error, "details", "No details available")
                print(f"Failed to close position {position_id}. Error: {str(close_error)}, Details: {error_details}")
                results.append({
                    "error": f"Failed to close position {position_id}. Error: {str(close_error)}",
                    "details": error_details,
                    "position": position
                })
                # Log failure
                await save_close_trade_log(
                    client=client,
                    symbol=symbol,
                    position_id=position_id,
                    success=False,
                    error_reason=str(close_error)
                )

        return {"success": True, "results": results}

    except Exception as e:
        return {"success": False, "error": str(e)}

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import asyncio
import json

@csrf_exempt
def close_positions_by_symbol(request):
    """
    Django view to close all open positions for a specific symbol across all clients.
    Also logs each close attempt in TradeCloseLog.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symbol = data.get("symbol")
            if not symbol:
                return JsonResponse({"success": False, "error": "Symbol is required"})

            clients = ClientDetail.objects.filter(MataApi_ACCOUNT_ID__isnull=False, MataApi_TOKEN__isnull=False)

            async def process_client_trades(client):
                try:
                    connection = await establish_connection(client.MataApi_ACCOUNT_ID, client.MataApi_TOKEN)
                    result = await close_open_trades_by_symbol(connection, symbol, client)
                    return {"success": True, "client_id": client.user_id}
                except Exception as e:
                    return {"success": False, "client_id": client.user_id, "error": str(e)}

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(asyncio.gather(
                *[process_client_trades(client) for client in clients]
            ))

            return JsonResponse({"success": True, "results": results})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})



# views.py (continuing)

def close_log_summary(request):
    """
    Shows total successful vs failed close attempts.
    """
    from .models import TradeCloseLog
    success_count = TradeCloseLog.objects.filter(success=True).count()
    fail_count = TradeCloseLog.objects.filter(success=False).count()
    return JsonResponse({
        "total_success": success_count,
        "total_fail": fail_count
    })

def close_log_details(request):
    """
    Lists all close logs, or filter by ?success=1 or ?success=0
    """
    from .models import TradeCloseLog

    success_filter = request.GET.get("success")
    if success_filter is not None:
        is_success = (success_filter == "1")
        logs = TradeCloseLog.objects.filter(success=is_success).order_by("-timestamp")
    else:
        logs = TradeCloseLog.objects.all().order_by("-timestamp")

    data = []
    for log in logs:
        data.append({
            "id": log.id,
            "client_user_id": log.client.user_id,
            "symbol": log.symbol,
            "position_id": log.position_id,
            "success": log.success,
            "error_reason": log.error_reason,
            "timestamp": log.timestamp.isoformat(),
        })
    return JsonResponse({"logs": data})


def close_trade_form(request):
    """
    Render the close trade form page.
    """
    return render(request, "close_trade_form.html")


#========================================================== Chart ===============================================================
#========================================================== Chart ===============================================================

def render_chart(request):
    """Render the HTML template for the real-time chart."""
    return render(request, 'chart.html') 

import asyncio
import datetime
from datetime import timedelta
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import TradeHistory, ClientDetail  # If these are in models.py
# from metaapi_cloud_sdk import MetaApi  # Assuming you have this installed


async def fetch_client_data(account_id, token):
    """
    Fetch open orders, historical orders, and open positions for the given MetaApi account.
    पिछले 7 दिनों का डेटा प्राप्त करता है।
    """
    api = MetaApi(token)
    account = await api.metatrader_account_api.get_account(account_id)
    
    if account.state not in ["DEPLOYING", "DEPLOYED"]:
        print("Deploying the account...")
        await account.deploy()
        await account.wait_connected()
    
    # Use streaming connection
    connection = account.get_streaming_connection()
    await connection.connect()
    print("Waiting for synchronization...")
    await connection.wait_synchronized()
    
    # Access live orders and positions from terminal state
    terminal_state = connection.terminal_state
    open_orders = terminal_state.orders or []
    open_positions = terminal_state.positions or []
    print("Open orders fetched:", open_orders)
    print("Open positions fetched:", open_positions)
    
    # Use history storage for historical orders and deals
    history_storage = connection.history_storage
    now = datetime.utcnow()
    start_time = now - timedelta(days=7)  # पिछले 7 दिनों का डेटा
    
    history_orders_raw = history_storage.get_history_orders_by_time_range(start_time, now) or []
    history_deals = history_storage.get_deals_by_time_range(start_time, now) or []
    print("Historical orders fetched:", history_orders_raw)
    print("Historical deals fetched:", history_deals)
    
    # Group orders by order_id to avoid duplicate rows and map details
    history_orders_dict = {}
    for order in history_orders_raw:
        oid = order.get('id')
        # यदि इस order_id का ऑर्डर पहले ही प्रोसेस हो चुका है, तो छोड़ें
        if oid in history_orders_dict:
            continue
        
        # संबंधित डील्स प्राप्त करें
        deals_for_order = [d for d in history_deals if d.get('orderId') == oid]
        entry_deals = [d for d in deals_for_order if d.get('entryType') == 'DEAL_ENTRY_IN']
        exit_deals = [d for d in deals_for_order if d.get('entryType') == 'DEAL_ENTRY_OUT']
        
        entry_price = entry_deals[0].get('price') if entry_deals else "-"
        entry_time = entry_deals[0].get('time') if entry_deals else "-"
        exit_price = exit_deals[-1].get('price') if exit_deals else "-"
        exit_time = exit_deals[-1].get('time') if exit_deals else "-"
        profit = sum(d.get('profit', 0) for d in exit_deals) if exit_deals else "-"

        history_orders_dict[oid] = {
            'id': oid,
            'symbol': order.get('symbol'),
            'type': order.get('type'),
            'volume': order.get('volume'),
            'entryPrice': entry_price,
            'exitPrice': exit_price,
            'profit': profit,
            'state': order.get('state'),
            'entryTime': entry_time,
            'exitTime': exit_time,
        }
    
    history_orders = list(history_orders_dict.values())
    print("Mapped history orders:", history_orders)
    
    await connection.close()
    return {
        "open_orders": open_orders,
        "history_orders": history_orders,
        "open_positions": open_positions,
    }

@csrf_exempt
def client_data_api(request):
    """
    API endpoint to fetch client data and return as JSON without caching.
    """
    if 'user_id' not in request.session:
        return JsonResponse({"error": "User not logged in"}, status=403)
    
    user_id = request.session.get('user_id')
    client = get_object_or_404(ClientDetail, user_id=user_id)

    if not client.MataApi_ACCOUNT_ID or not client.MataApi_TOKEN:
        return JsonResponse({"error": "MetaApi account details not found for the client"}, status=400)
    
    async def get_client_data():
        return await fetch_client_data(client.MataApi_ACCOUNT_ID, client.MataApi_TOKEN)
    
    try:
        client_data = asyncio.run(get_client_data())
        
        # Convert datetime objects to ISO strings for JSON serialization
        for order in client_data.get("history_orders", []):
            if isinstance(order.get('entryTime'), datetime):
                order['entryTime'] = order['entryTime'].isoformat()
            if isinstance(order.get('exitTime'), datetime):
                order['exitTime'] = order['exitTime'].isoformat()
        for pos in client_data.get("open_positions", []):
            if isinstance(pos.get('time'), datetime):
                pos['time'] = pos['time'].isoformat()
        
        return JsonResponse(client_data)
    except Exception as e:
        print(f"Error fetching client data: {e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def client_orders_view(request):
    """
    Render the orders and positions page.
    Data will be fetched asynchronously via AJAX.
    """
    if 'user_id' not in request.session:
        return redirect('login_client')
    
    user_id = request.session.get('user_id')
    client = get_object_or_404(ClientDetail, user_id=user_id)

    if not client.MataApi_ACCOUNT_ID or not client.MataApi_TOKEN:
        return redirect('login_client')
    
    context = {
        "client": client,
    }
    return render(request, "client_orders.html", context)

#====================================================================================================================
#====================================================================================================================
from django.core.management import call_command

def run_update_trade_history(request):
    call_command('update_trade_history')
    return HttpResponse("Trade history updated successfully.")


# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import ClientDetail

# def configure_trading_account(request):
#     if 'user_id' not in request.session:
#         return JsonResponse({"success": False, "error": "User not authenticated."})

#     user_id = request.session.get('user_id')  # Get the user ID from the session
#     try:
#         client_user = ClientDetail.objects.get(user_id=user_id)
#         metaapi_link = client_user.MataApi_account_link  # Fetch MataApi_account_link from model

#         if not metaapi_link:
#             return JsonResponse({"success": False, "error": "MetaAPI account link not found."})
#     except ClientDetail.DoesNotExist:
#         return JsonResponse({"success": False, "error": "User not found."})

#     return render(request, 'metaapi_form.html', {
#         'client_user': client_user,
#         'metaapi_link': metaapi_link,
#     })

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import ClientDetail

# def configure_trading_account(request):
#     if 'user_id' not in request.session:
#         return JsonResponse({"success": False, "error": "User not authenticated."})

#     user_id = request.session.get('user_id')
#     client_user = get_object_or_404(ClientDetail, user_id=user_id)

#     if not client_user.MataApi_account_link:
#         return JsonResponse({"success": False, "error": "MetaAPI account link not found."})

#     return JsonResponse({
#         "success": True,
#         "metaapi_link": client_user.MataApi_account_link
#     })

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import ClientDetail

def configure_trading_account(request):
    # Check if the user is authenticated
    if 'user_id' not in request.session:
        return JsonResponse({"success": False, "error": "User not authenticated."})

    user_id = request.session.get('user_id')
    client_user = get_object_or_404(ClientDetail, user_id=user_id)

    # Ensure MetaAPI account link exists
    if not client_user.MataApi_account_link:
        return JsonResponse({"success": False, "error": "MetaAPI account link not found."})

    # Redirect to the page where the iframe will be rendered
    return HttpResponseRedirect('/configure-account/')


# def configure_account_page(request):
#     # Pass the MetaAPI link to the template
#     user_id = request.session.get('user_id', None)
#     if not user_id:
#         return JsonResponse({"success": False, "error": "User not authenticated."})
    
#     client_user = get_object_or_404(ClientDetail, user_id=user_id)
#     return render(request, 'metaapi_form.html', {"metaapi_link": client_user.MataApi_account_link})

from django.shortcuts import render, get_object_or_404
from .models import ClientDetail

def configure_account_page(request):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return render(request, 'metaapi_form.html', {"error_message": "User not authenticated."})

    # Fetch the client details
    client_user = get_object_or_404(ClientDetail, user_id=user_id)

    # Check if the MetaAPI account link exists
    if not client_user.MataApi_account_link:
        # If the link doesn't exist, show the error
        return render(request, 'metaapi_form.html', {
            "error_message": "Your API is not set up. Please contact our Support Team.",
        })

    # If the link exists, render the iframe
    return render(request, 'metaapi_form.html', {"metaapi_link": client_user.MataApi_account_link})



