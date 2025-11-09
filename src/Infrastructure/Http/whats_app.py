import os 
from twilio.rest import Client
import json
from src.Domain.User import UserDomain
from src.Application.Service import user_service


#Whatsapp parou de funcionar
'''
def send_whatsapp_code(code:str,phone:str):

    account_sid = ""
    auth_token = "" 
    client = Client(account_sid, auth_token)
        
    message = client.messages.create(
    from_='whatsapp:',
    content_sid='',
    content_variables=f'{{"1":"{code}"}}',
    to=f"whatsapp:+55{phone}"
    )
    print(message.sid)
'''


def send_sms_code(code: str, phone: str):
    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Código: {code}",
        from_="+14025184722",
        to=f"+55{phone}",     
    )

    print(message.sid)