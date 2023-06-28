from django.shortcuts import render, redirect
# Create your views here.
from .models import EmailInfo, MailLog, SMSLog
from twilio.rest import Client
import Task10.keys as keys
from django.core.mail import send_mail, BadHeaderError
import smtplib
from email.mime.text import MIMEText
from email.header import Header



def send_email(request):
    if request.method == 'POST':
        # Get recipients email ids to send 
        email_ids = request.POST.getlist('recipients[]')
        sender_email = 'kyathamaryan@gmail.com'
        recipients = [email.strip() for email in email_ids]

        # Content of mail
        subject = 'Testing Email Counts Xircls'
        message = 'Test Email'
        domain = request.POST.get('domain')
        data = send_mail
        data(
            subject,
            '',
            sender_email,
            recipients,
            html_message=message,
            fail_silently=False,
        )
        print(data)

        sent_count = len(email_ids)
        email_info = EmailInfo.objects.first()
        
        #Mail Count is getting incremented in frontend using js not via code :
        email_info.update_counts(sent_count)
        

        # Save the mail log entry
        for recipient in recipients:
            MailLog.objects.create(domain=domain, recipient_email=recipient)

        return redirect(send_email)
    email_info = EmailInfo.objects.first()
    email_ids_list = email_info.email_ids.split(',') if email_info else []
    counts = {
        'total_count': count_email_ids(email_info.email_ids) if email_info else 0,
        'sent_count': email_info.sent_count if email_info else 0,
    }

    mail_logs = MailLog.objects.all()

    return render(request, 'log.html', {'counts': counts, 'email_ids': email_ids_list, 'mail_logs': mail_logs })


# Add email ids in recipients list:
def add_email_ids(request):
    if request.method == 'POST':
        email_ids = request.POST.get('email_ids')
        # Process the email IDs and add them to the database

        email_info = EmailInfo.objects.first()
        if email_info:
            existing_ids = email_info.email_ids.split(',')
            new_ids = [email_id.strip() for email_id in email_ids.split(',')]
            updated_ids = list(set(existing_ids + new_ids))
            email_info.email_ids = ','.join(updated_ids)
            email_info.save()
        else:
            email_info = EmailInfo(email_ids=email_ids)
            email_info.save()

        return redirect(email_count)

    return render(request, 'add_email.html')

# Count existing emails in the database :
def count_email_ids(email_ids):
    if isinstance(email_ids, str):
        return len(email_ids.split(','))
    elif isinstance(email_ids, EmailInfo):
        return len(email_ids.email_ids.split(','))
    else:
        return 0

#Messed up     
def email_count(request):
    email_info = EmailInfo.objects.first()
    count = email_info.total_count if email_info else 0
    email_ids_list = email_info.email_ids.split(',') if email_info else []

    return render(request, 'add_email.html', {'count': count, 'email_ids': email_ids_list})

# Sends sms with whatsapp and also normal text message
def send_sms(request):
    sms_logs = SMSLog.objects.all()
    sms_count = SMSLog.objects.count()
    print(sms_count)

    if request.method == 'POST':
        client = Client(keys.account_sid, keys.auth_token)
        domain = request.POST.get('domain')
        body = request.POST.get('body')
        target_number = request.POST.get('target_number')
        print(sms_count)

        if domain == 'SMS':
            message = client.messages.create(
                body=body,
                from_=keys.twilio_number,
                to=target_number,
            )
        
        if domain == 'Whatsapp':
            account_sid = 'AC8ff1c391e4daaab4fd0a0d0faa4bab65'
            auth_token = '2df97aeb016072dc37db9675d18e90b0'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=body,
                to='whatsapp:+918657689680'
            )

            print(message.sid)

        log_entry = SMSLog(
            from_domain=domain,
            from_number=keys.twilio_number,
            to_number=target_number,
            body=body,
        )
        #Sms Count increment
        sms_count = log_entry.sms_count + 1
        log_entry.sms_count = sms_count
        log_entry.save()
        sms_logs = SMSLog.objects.all()

        
        return render(request, 'sms.html', {'sms_count': sms_count, 'sms_logs': sms_logs})
    
    #To Store the count of Whatsapp Via Sent SMS , Normal SMS
    whatsapp_count = sms_logs.filter(from_domain='Whatsapp').count()
    smso_count = sms_logs.filter(from_domain='SMS').count()

    return render(request, 'sms.html', {'sms_count': sms_count, 'sms_logs': sms_logs,'whatsapp_count': whatsapp_count,
        'smso_count': smso_count})

    # Perform actions based on the selected domain
        # if domain == 'mailchimp':
        #     # Perform actions for MailChimp
        #     # ...
        #Here Mailchimp Transactional API will come 
        # elif domain == 'smtp':
        #     # Perform actions for SMTP
        #     # ...

        # elif domain == 'sendgrid':
        #     # Perform actions for SendGrid
        #     # ...
        
# def send_email(request):
#     if request.method == 'POST':
#         email_ids = request.POST.getlist('recipients[]')
#         sender_email = 'kyathamaryan@gmail.com'
#         recipients = [email.strip() for email in email_ids]

#         subject = 'Testing Email Counts Xircls'
#         message = 'Test Email'
#         domain = request.POST.get('domain')

#         email_content = MIMEText(message, 'plain', 'utf-8')
#         email_content['Subject'] = Header(subject, 'utf-8')
#         email_content['From'] = sender_email
#         email_info = EmailInfo.objects.first()

#         try:
#             # Connect to the SMTP server
#             smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server address and port
#             smtp_server.starttls()
#             smtp_server.login(sender_email, 'qsloqwyaivzrunyp')

#             sent_count = 0  # Track the number of successfully sent emails

#             # Send the email to each recipient individually
#             for recipient in recipients:
#                 try:
#                     # Send the email and get the server response
#                     smtp_server.sendmail(sender_email, recipient, email_content.as_string())
                    
#                     # Get the response code and message
#                     response_code = smtp_server.getreply()[0]
#                     response_message = smtp_server.getreply()[1].decode('utf-8')

#                     # Print the server response
#                     print(f"Response code: {response_code}")
#                     print(f"Response message: {response_message}")


#                     # Save the mail log entry
#                     MailLog.objects.create(domain=domain, recipient_email=recipient)

#                 except Exception as e:
#                     print(f"An error occurred while sending email to {recipient}: {str(e)}")

#             # Update the email counts
#             if email_info:
#                 email_info.update_counts(sent_count)

#             # Disconnect from the SMTP server
#             smtp_server.quit()

#             return redirect('send_email')  # Replace with your desired redirect URL

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")

#             return redirect('send_email')  # Replace with your desired redirect URL and error handling

#     email_info = EmailInfo.objects.first()
#     email_ids_list = email_info.email_ids.split(',') if email_info else []
#     counts = {
#         'total_count': count_email_ids(email_info.email_ids) if email_info else 0,
#         'sent_count': email_info.sent_count if email_info else 0,
#     }

#     mail_logs = MailLog.objects.all()

#     return render(request, 'log.html', {'counts': counts, 'email_ids': email_ids_list, 'mail_logs': mail_logs})

