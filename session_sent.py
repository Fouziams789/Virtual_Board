import time
import requests
import smtplib
import os
import imghdr
from email.message import EmailMessage
from datetime import datetime
from datetime import date
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def emailsender(img):
    with open(img,'rb') as f:
        file_data=f.read()
        file_type=imghdr.what(f.name)
        file_name=f.name
    EMAIL_ADDRESS ='vb.airoboard@gmail.com'
    EMAIL_PASSWORD ='bstzcgymwettgcpb'
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M:%S")
    d2 = today.strftime("%B %d, %Y")
    Latitude = "8.5143"
    Longitude = "76.9268"
    location = geolocator.geocode(Latitude+","+Longitude)
    msg=EmailMessage()
    msg['Subject']='ACCIDENT DETECTED AT '+current_time+' ON '+d2
    msg['From']=EMAIL_ADDRESS
    msg['To']='smohammedshafeeqhameed@gmail.com'
    msg.set_content('EMERGENCY CARE ABULANCE REQUIRED..Location of the Accident place :  '+str(location))
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    s = smtplib.SMTP("smtp.gmail.com:587")
    s.starttls()
    s.ehlo
    try:
        s.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        s.send_message(msg)
    except:
        print('SMTPAuthenticationError')
    #     s.sendmail(gmail_user, to, msg.as_string())
    #     s.quit()

# import smtplib
#
# def emailsender(img):
#     with open(img,'rb') as f:
#         file_data = f.read()
#         file_type = imghdr.what(f.name)
#         file_name = f.name
# # creates SMTP session
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#
#     # start TLS for security
#     s.starttls()
#
#     # Authentication
#     s.login("vb.airoboard@gmail.com", "bstzcgymwettgcpb")
#
#     # message to be sent
#     message = "Message_you_need_to_send"
#
#     # sending the mail
#     s.sendmail("vb.airoboard@gmail.com", "smohammedshafeeqhameed@gmail.com", message)
#
#     # terminating the session
#     s.quit()
