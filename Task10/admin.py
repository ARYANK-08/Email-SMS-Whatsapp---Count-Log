from django.contrib import admin
from .models import EmailInfo , MailLog , SMSLog
# Register your models here.

admin.site.register(EmailInfo)
admin.site.register(MailLog)
admin.site.register(SMSLog)