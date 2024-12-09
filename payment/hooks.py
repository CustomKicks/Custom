from paypal.standard.ipn.models import ST_COMPLETED 
from paypal.standard.ipn.signals import valid_ipn_received 
from django.dispatch import receiver 
from django.contrib.auth.models import User 
from django.conf import settings  

@receiver(valid_ipn_received) 
def payment_notification(sender, **kwargs): 
    ipn_obj = sender 

    print(ipn_obj)
    print(f'Amount Paid: {ipn_obj.gross}')
    