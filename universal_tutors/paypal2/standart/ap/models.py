from django.db import models
from django.conf import settings

class MassPayment(models.Model):
    PROCESSING = 0
    FINISHED = 1
    ERROR = 2
    
    STATUS_TYPES = (
        (PROCESSING, 'Processing'),
        (FINISHED, 'Finished with success'),
        (ERROR, 'Error')
    )

    currency_code = models.CharField(max_length=5)
    sender_email = models.EmailField()
    memo = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    status = models.SmallIntegerField(choices = STATUS_TYPES, default = PROCESSING)
    
    def unicode(self):
        return self.memo

class MassPaymentReceiver(models.Model):
    payment = models.ForeignKey(MassPayment, related_name='receivers')
    email = models.EmailField()
    amount = models.FloatField()
    primary = models.BooleanField(default=False)
    
    def unicode(self):
        return '%s: %s to %s' % (self.payment, self.amount, self.email)
