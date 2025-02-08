from django.db import models
from subadmin.services import calculate_revenue_share

# Create your models here.
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator

class Subadmin_client_limit(models.Model):
    Subadmin_limit = models.CharField(max_length=20)
    max_quantity = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_credit = models.IntegerField(default=0)
    withdraw = models.IntegerField(default=0)
    expired_limit = models.IntegerField(default=0)
    active_limit = models.IntegerField(default=0)
    def _str_(self):
        return self.Subadmin_limit


# subadmin_logo
# class subadmin_logo(models.Model):
#     subadmin_keyword = models.CharField(max_length=1000,blank=True,null=True)
#     subadmin_logo = models.ImageField(upload_to='photos/subadmin_logo',blank=True,null=True)
#     # timestamp
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)

#     def _str_(self):
#         return self.subadmin_keyword
    
from datetime import timedelta    
class sub_adminDT(models.Model):
  #  subadmin_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    subadmin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
  #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    subadmin_active = models.BooleanField(default=False)
    subadmin_name_first = models.CharField(max_length=50, blank=True, null=True) 
    subadmin_name_last = models.CharField(max_length=50, blank=True, null=True)
    subadmin_email = models.EmailField(blank=True, null=True)
    subadmin_password = models.CharField(max_length=50,blank=True, null=True)
    subadmin_phone_number = models.CharField(max_length=15,blank=True, null=True)
    subadmin_verify_code = models.CharField(max_length=15,blank=True, null=True)

    subadmin_keyword = models.CharField(max_length=1000,blank=True,null=True)
    subadmin_logo = models.ImageField(upload_to='photos/subadmin_logo',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True,blank=True, null=True)

    subadmin_client_limit = models.ForeignKey(Subadmin_client_limit, on_delete=models.SET_NULL, blank=True, null=True)
    subadmin_status= models.BooleanField(default=False,blank=True, null=True)  

    subadmin_date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    subadmin_last_login = models.DateTimeField(verbose_name='last login', default=timezone.now() + timedelta(days=1))
     
    # Subadmin admin account type Demo/Live 
    demo_live_choice = (
        ('demo', 'Demo'),
        ('live', 'Live'),
    ) 
    subadmin_account_type = models.CharField(max_length=10, choices=demo_live_choice, default='live')
 
    # kyc 
    sub_admin_active = models.BooleanField(default=False)
    subadmin_paid_paln = models.BooleanField(default=True, blank=True, null=True)
    subadmin_Term_condition = models.BooleanField(default=False)  
    subadmin_ip_address = models.GenericIPAddressField(blank=True, null=True)

    # Revenue and payout fields 
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True, null=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True, null=True)
    
    def save(self, *args, **kwargs):
          # If subadmin_id is not set, generate a new unique ID
          if not self.subadmin_id:
              self.subadmin_id = self.generate_unique_id()
          super(sub_adminDT, self).save(*args, **kwargs)
      
    def generate_unique_id(self): 
          while True:
              # Generate a new ID
              new_id = uuid.uuid4().hex[:8]
              # Check if this ID already exists
              if not sub_adminDT.objects.filter(subadmin_id=new_id).exists():
                  return new_id  
      
      
    def _str_(self):
        return f'{self.subadmin_name_first} {self.subadmin_name_last}'
     
    def update_earnings(self):
        # Call calculate_revenue_share to get the percentage
        percentage = calculate_revenue_share(self.total_revenue)
        # Calculate the earnings based on the percentage
        self.earnings = self.total_revenue * (percentage / 100)
        self.save()


    def update_revenue_and_earnings(self, subadmin_id, revenue):
        try:
            # Fetch the sub-admin by ID
            subadmin = sub_adminDT.objects.get(subadmin_id=subadmin_id)

            # Fetch all active clients for the sub-admin
            active_clients = ClientDetail.objects.filter(
                sub_admin_id=subadmin_id,
                sub_admin_user_active=True  # Only consider active clients
            )
            
            if not active_clients.exists():
                print("No active clients found for this sub-admin. Skipping calculation.")
                return

            # Calculate total revenue only for active clients
            total_revenue_from_active_clients = 0

            for client in active_clients:
                # Assuming 'client_revenue' is a field in ClientDetail that tracks individual client revenue
                total_revenue_from_active_clients += client.client_revenue

            # Update sub-admin's revenue based on active clients' revenue
            subadmin.total_revenue = total_revenue_from_active_clients
            
            # Call the update_earnings method to update earnings based on new revenue
            subadmin.update_earnings()

            # Save the sub-admin instance
            subadmin.save()

        except sub_adminDT.DoesNotExist:
            print("Sub-admin not found")


from django.db import models

from django.utils.html import format_html

class SUBKYC(models.Model):
    subadmin_id = models.ForeignKey(
        sub_adminDT, on_delete=models.CASCADE, related_name="kyc_details"
    )
    subadmin_national_id = models.FileField(upload_to='subadmin_national_ids/', blank=True, null=True)
    subadmin_national_id_number = models.CharField(max_length=20, blank=True, null=True)
    subadmin_national_id_name = models.CharField(max_length=100, blank=True, null=True)
    subadmin_national_id_issue_date = models.DateField(blank=True, null=True)
    subadmin_agreement_signed = models.BooleanField(default=False)
    subadmin_agreement_file = models.FileField(upload_to='subadmin_agreements/', blank=True, null=True)
    subadmin_terms_accepted = models.BooleanField(default=False)
    subadmin_reference_text = models.TextField(blank=True, null=True)
    subadmin_kyc_completed = models.BooleanField(default=False)
    subadmin_video_file = models.FileField(upload_to='subadmin_video_verifications/', blank=True, null=True)
    subadmin_video_verification_done = models.BooleanField(default=False)
    reference_text = models.TextField(null=True, blank=True)  # Add this if it is required
     
    def _str_(self):
        return f"KYC for {self.subadmin_id.subadmin_email}"

    def subadmin_video_file_url(self):
        if self.subadmin_video_file:
            return self.subadmin_video_file.url
        return None
               
