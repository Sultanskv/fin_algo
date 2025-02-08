from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import authenticate

#admin create_superuser
class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

 
class SYMBOL(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True) 
      SYMBOL = models.CharField(max_length=10)
      created_at = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
        return self.SYMBOL
    
class GROUP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GROUP = models.CharField(max_length=10)
    min_quantity = models.FloatField(validators=[MinValueValidator(0.0)],blank=True,null=True)
    max_quantity = models.FloatField(validators=[MinValueValidator(0.0)],blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.GROUP
     
class Broker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True)
    broker = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.broker 
    
class mt5_server(models.Model):
    broker = models.ForeignKey(Broker, related_name='servers', on_delete=models.CASCADE) 
    mt5_server = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.broker.broker} - {self.mt5_server}"   

class ClientDetail(models.Model):
    user_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    user_active = models.BooleanField(default=False)
 #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    verify_code = models.CharField(max_length=15,blank=True, null=True)
    date_joined	= models.DateTimeField(verbose_name='date joined', default=None)
    last_login= models.DateTimeField(verbose_name='last login',default=None)
    panel_last_login = models.DateTimeField(blank=True, null=True)
    clint_plane = models.CharField(max_length=15,blank=True, null=True) 
    client_Group = models.ForeignKey(GROUP, on_delete=models.SET_NULL, blank=True, null=True)
    
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, blank=True, null=True)     
    is_staff= models.BooleanField(default=False)    
    clint_status = models.CharField(max_length=15,blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    mt5_login = models.IntegerField(blank=True, null=True)
    mt5_password = models.CharField(max_length=100, blank=True, null=True)
    mt5_server = models.CharField(max_length=100, blank=True, null=True)
    AppName = models.CharField(max_length=500, blank=True, null=True)
    MataApi_ACCOUNT_ID = models.CharField(max_length=500, blank=True, null=True)
    MataApi_TOKEN = models.CharField(max_length=10000, blank=True, null=True) 
    MataApi_account_link = models.CharField(max_length=10000, blank=True, null=True) 
    MataApi_server_url = models.CharField(max_length=10000, blank=True, null=True)
   # mt5_server = models.ForeignKey(mt5_server, on_delete=models.SET_NULL, blank=True, null=True)  # Corrected ForeignKey
    # client_Group = models.ForeignKey(GROUP, on_delete=models.SET_NULL, blank=True, null=True)
    # broker = models.ForeignKey(BROKERS, on_delete=models.SET_NULL, blank=True, null=True)
    demo_live_choice = (
        ('demo', 'Demo'),
        ('live', 'Live'),
    )
    account_type = models.CharField(max_length=10, choices=demo_live_choice, default='live')
    sub_admin_id = models.CharField(max_length=50, blank=True, null=True)
    sub_admin_user_active = models.BooleanField(default=False)
    paid_paln = models.BooleanField(default=True, blank=True, null=True)
    Term_condition = models.BooleanField(default=False)  
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    OPTIONS = [
        ('A', 'Route'),
        ('B', 'Detour'),
        ('C', 'Destination'),
        ('D', 'Demograph'),
        ('M', 'Messanger'),
    ]
    
    selected_option = models.CharField(max_length=1, choices=OPTIONS, default='A')
    forex_option = models.BooleanField(default=False)  # For Forex option
    comex_option = models.BooleanField(default=False)
    Singapore = models.BooleanField(default=False)  # For Forex option
    Bursa_Malaysia = models.BooleanField(default=False)  
    US30 = models.BooleanField(default=False)  
    HK100 = models.BooleanField(default=False)   
    # def __str__(self):
    #     return f"{self.broker.broker}"
    def save(self, *args, **kwargs):
        # Check if sub_admin_id is not available (None or empty)
        if not self.sub_admin_id:
            self.sub_admin_user_active = True
        else:
            self.sub_admin_user_active = False
        # Save the instance
        super(ClientDetail, self).save(*args, **kwargs)
    
class Strategy(models.Model):
    Strategy = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.Strategy       

from django.db import models

class ClientSymbolSetting(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trade_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.name_first} - {self.symbol}"


from django.contrib.auth.models import User
from django.db import models

class ClientSignal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True)
    admin = models.CharField(max_length=50, blank=True, null=True)
    client_id = models.CharField(max_length=50, blank=True, null=True)
    message_id = models.CharField(max_length=50, blank=True, null=True)
    ids = models.CharField(max_length=50, blank=True, null=True)
    
    SYMBOL = models.ForeignKey(SYMBOL, on_delete=models.CASCADE, related_name='client_signals')
    TYPE_CHOICES = (
        ('BUY_ENTRY', 'BUY_ENTRY'),
        ('BUY_EXIT', 'BUY_EXIT'),
        ('SELL_ENTRY', 'SELL_ENTRY'),
        ('SELL_EXIT', 'SELL_EXIT'),
    )
    TYPE = models.CharField(max_length=10, choices=TYPE_CHOICES)
    QUANTITY = models.FloatField(null=True, blank=True)
    ENTRY_PRICE = models.DecimalField(max_digits=12, decimal_places=5,null=True,blank=True)
    EXIT_PRICE = models.DecimalField(max_digits=12, decimal_places=5,null=True,blank=True)
    profit_loss =  models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    cumulative_pl =  models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
     

class Client_SYMBOL_QTY(models.Model):
    client_id = models.CharField(max_length=50, blank=True, null=True)    
    SYMBOL = models.CharField(max_length=50, blank=True, null=True)
    QUANTITY = models.FloatField(null=True, blank=True)
    trade = models.CharField(max_length=50, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)


class HelpMessage(models.Model):
    user_id = models.ForeignKey(ClientDetail, to_field='user_id', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user_id} {self.client_name} at {self.timestamp}'

from django.db import models

class MT4Account(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    server = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.login} - {self.server}"
    
from django.db import models

class Trade(models.Model):
    ticket = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=10)
    volume = models.FloatField()
    price_open = models.DecimalField(max_digits=10, decimal_places=5)
    price_current = models.DecimalField(max_digits=10, decimal_places=5)
    sl = models.DecimalField(max_digits=10, decimal_places=5)
    tp = models.DecimalField(max_digits=10, decimal_places=5)
    profit = models.DecimalField(max_digits=10, decimal_places=5)
    time = models.DateTimeField()
    type = models.CharField(max_length=4)  # BUY or SELL
    

from django.db import models
from django.utils import timezone

class TradeHistory(models.Model):
    client = models.ForeignKey('ClientDetail', on_delete=models.CASCADE)
    signal_time = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=50)
    trade_type = models.CharField(max_length=10)  # 'BUY', 'SELL', 'CLOSE'
    quantity = models.FloatField()
    entry_price = models.FloatField(null=True, blank=True)
    exit_price = models.FloatField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True) 
    ticket_id = models.CharField(max_length=20, null=True, blank=True)
    p_l = models.FloatField(null=True, blank=True)
    cumulative_p_l = models.FloatField(null=True, blank=True)
    
    def calculate_p_l(self):
        if self.exit_price and self.entry_price:
            if self.trade_type == 'BUY':
                return (self.exit_price - self.entry_price) * self.quantity
            elif self.trade_type == 'SELL':
                return (self.entry_price - self.exit_price) * self.quantity
        return None

    def save(self, *args, **kwargs):
        if self.trade_type == 'CLOSE':
            self.p_l = self.calculate_p_l()
            last_trade = TradeHistory.objects.filter(client=self.client, symbol=self.symbol, trade_type='CLOSE').order_by('-signal_time').first()
            if last_trade:
                self.cumulative_p_l = last_trade.cumulative_p_l + self.p_l
            else:
                self.cumulative_p_l = self.p_l
        super(TradeHistory, self).save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import User

class ClientActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=10)  # "login", "logout", "update"
    symbol = models.CharField(max_length=255, null=True, blank=True)  # To store symbol name
    quantity = models.FloatField(null=True, blank=True)  # To store quantity
    updated_by = models.CharField(max_length=255, null=True, blank=True)  # 'client' or 'admin'
    
    def __str__(self):
        return f'{self.user.username} - {self.action} at {self.time}'


from django.db import models

class TradeStatus(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    quantity = models.FloatField()
    status_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.symbol} - {self.status_message}"
    
from django.db import models

class OperationMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    operation_type = models.CharField(max_length=20)  # "place" or "close"
    message = models.TextField()

    def __str__(self):
        return f"[{self.timestamp}] {self.operation_type.upper()}: {self.message}"


from django.db import models

class MT5OperationLog(models.Model):
    operation_type = models.CharField(max_length=50)  # e.g., "Place Order", "Close Order"
    client_login = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.operation_type} - {self.client_login} - {self.symbol}"


from django.db import models
from .models import ClientDetail
from django.utils.html import format_html

class KYC(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    national_id = models.FileField(upload_to='national_ids/', blank=True, null=True)
    national_id_number = models.CharField(max_length=20, blank=True, null=True)  # ID number
    national_id_name = models.CharField(max_length=100, blank=True, null=True)   # Name on ID
    national_id_issue_date = models.DateField(blank=True, null=True)  # Issue date
    agreement_signed = models.BooleanField(default=False)
    agreement_file = models.FileField(upload_to='agreements/', null=True, blank=True)
    terms_accepted = models.BooleanField(default=False)
    reference_text = models.TextField(blank=True, null=True)  # Field to store the reference text
    kyc_completed = models.BooleanField(default=False)  # Flag for KYC completion
    video_file = models.FileField(upload_to='video_verifications/', blank=True, null=True)
    video_verification_done = models.BooleanField(default=False)

    def __str__(self):
        return f"KYC for {self.client.email}"

    def video_file_url(self):
        if self.video_file:
            return self.video_file.url
        return None
    
       
class ClientStatus(models.Model):
    sub_admin_id = models.CharField(max_length=50,null=True, blank=True)
    clint_id = models.CharField(max_length=50,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)  # 'Name' field as a string
    time = models.DateTimeField(auto_now_add=True)  # 'Time' field as a DateTime field
    clint_email = models.EmailField(blank=True, null=True)   # client email 
    clint_phone_number = models.CharField(max_length=15,blank=True, null=True)  # client phone Number
    service_name = models.CharField(max_length=255,null=True, blank=True)  # 'Service Name' field as a string
    quantity = models.IntegerField(null=True, blank=True)  # 'Quantity' field as an integer
    strategy = models.CharField(max_length=255,null=True, blank=True)  # 'Strategy' field as a string
    login_date_time = models.DateTimeField(blank=True, null=True)             #broker On/Off 
    panel_last_login = models.DateTimeField(blank=True, null=True)     # panel On/Off
    clint_plane = models.CharField(max_length=15,blank=True, null=True)  # client plane Demo/Live
    trading = models.CharField(max_length=255,null=True, blank=True)  # 'Trading' field as a string
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # 'IP Address' field as an IP address
    updated_by = models.CharField(max_length=255,null=True, blank=True)  # 'UPDATED BY' field as a string
    client_status = models.CharField(max_length=255,null=True, blank=True)  # 'Strategy' field as a string

    def _str_(self):
        return f"{self.name} - {self.service_name} ({self.clint_id})"
   

from django.db import models

class MarketData(models.Model):
    date = models.DateField(auto_now_add=True)
    symbol = models.CharField(max_length=50)  # e.g., 'XAU/USD', 'USOIL'
    data = models.TextField()  # Raw market data

    def __str__(self):
        return f"{self.symbol} data on {self.date}"
   
class ClientMessage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Admin sending the message
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)  # Client receiving the message
    message = models.TextField()  # Advisory message
    created_at = models.DateTimeField(auto_now_add=True)  # Time of message creation
    read = models.BooleanField(default=False)  # Read status
    advisory_type = models.CharField(max_length=20, choices=[('Forex', 'Forex'), ('Comex', 'Comex')], null=True, blank=True)  # New field for advisory type


    def __str__(self):
        return f"Message to {self.client}: {self.message[:30]}..."

class Notification(models.Model):
    client = models.ForeignKey(
        'myapp.ClientDetail',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,  # Allow NULL temporarily
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ClientPaymetns(models.Model):    
    sub_admin_id = models.CharField(max_length=100,null=True, blank=True)
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE, null=True, blank=True)
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50, blank=True, null=True)
    payer_email = models.EmailField(max_length=100,null=True, blank=True)
    payer_mobile = models.CharField(max_length=20,null=True, blank=True)
    payment_txn_id = models.CharField(max_length=100,null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True) 
    pay_amount = models.IntegerField(null=True, blank=True) 
    offer_discount = models.IntegerField(null=True, blank=True) 
    bill_no = models.CharField(max_length=100,null=True, blank=True)
    bill_date = models.DateTimeField(auto_now_add=True,null=True, blank=True) 
    plan_name = models.CharField(max_length=100,null=True, blank=True)
    valid_plan_date = models.DateTimeField(auto_now_add=False,null=True, blank=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )  #
    
    def _str_(self):
        return f"Payment: {self.sub_admin_id} {self.payment_txn_id} {self.client.user_id}"
    

    

class offers_subadmin(models.Model): 
    Title = models.CharField(max_length=500) 
    Offer_Title = models.CharField(max_length=200)  # Adjust max_length as needed
    offer_price = models.IntegerField() # Adjust max_length as needed
    revenue = models.CharField(max_length=200)  # Adjust max_length as needed
    offer_image = models.ImageField(upload_to='offers_images/', null=True, blank=True)  # New image field

    def __str__(self):
        return f"Order {self.Offer_Title}" 




class TradeExecutionLog(models.Model):
    """
    Stores the result of each trade execution for every client.
    """
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    order_type = models.CharField(max_length=50)
    volume = models.FloatField()
    price = models.FloatField(null=True, blank=True)
    stop_loss = models.FloatField(null=True, blank=True)
    take_profit = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_reason = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"Trade #{self.id} - {self.symbol} ({status}) for Client {self.client.user_id}"
    

# New model to track every attempt to close trades
class TradeCloseLog(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    position_id = models.CharField(max_length=100, null=True, blank=True)  # from MetaApi
    success = models.BooleanField(default=False)
    error_reason = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "SUCCESS" if self.success else f"FAILED: {self.error_reason}"
        return f"CloseLog #{self.id} | Client={self.client.user_id} | {self.symbol} | Position={self.position_id} | {status}"
    
from django.db import models

class TradeDeleteLog(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE, related_name='delete_logs')
    symbol = models.CharField(max_length=20)
    order_id = models.CharField(max_length=50)
    success = models.BooleanField(default=False)
    error_reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.username} - {self.symbol} - {'Success' if self.success else 'Failure'}"
