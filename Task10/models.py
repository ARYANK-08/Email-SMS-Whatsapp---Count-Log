from django.db import models
from django.utils import timezone 

# Create your models here.

class EmailInfo(models.Model):
    email_ids = models.TextField()
    total_count = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)

    def update_counts(self, sent_count):
        self.sent_count += sent_count
        self.save()
        

    def get_counts(self):
        return {
            'total_count': self.total_count,
            'sent_count': self.sent_count,
        }


class MailLog(models.Model):
    DOMAIN_CHOICES = [
        ('mailchimp', 'MailChimp'),
        ('smtp', 'SMTP'),
        ('sendgrid', 'SendGrid'),
    ]

    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Log Entry - {self.domain} {self.recipient_email} ({self.sent_at})"



from datetime import datetime
class SMSLog(models.Model):

    timestamp = models.DateTimeField(default=datetime.now())
    from_domain = models.CharField(max_length=20)
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=20)
    sms_count = models.IntegerField(default=0)
    body = models.CharField(max_length = 100,default=0)

