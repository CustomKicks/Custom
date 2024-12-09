from paypal.standard.ipn.models import ST_COMPLETED 
from paypal.standard.ipn.signals import valid_ipn_received 
from django.dispatch import receiver 
from django.contrib.auth.models import User 
from django.conf import settings  

@receiver(valid_ipn_received) 
def payment_notification(sender, **kwargs): 
    ipn_obj = sender 
    if ipn_obj.payment_status == ST_COMPLETED: 
        if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL: 
            user = User.objects.get(email=ipn_obj.receiver_email) 
            order = user.order_set.get(order_number=ipn_obj.custom)