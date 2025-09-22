import os 
from twilio.rest import Client
import json
from src.Domain.User import UserDomain

def send_whatsapp_code(code:str,phone:str):

    account_sid = ""
    auth_token = "" 
    client = Client(account_sid, auth_token)
        
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    content_sid='',
    content_variables=f'{{"1":"{code}"}}',
    to=f"whatsapp:+{phone}"
    )
    print(message.sid)

