import os 
from twilio.rest import Client
import json
import UserDomain from src.Domain.User

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_whatsapp_code(code:str,phone:str):

    account_sid = "" #SID do Twilio tem que pegar novamente
    auth_token = "" #token do Twilio tem que pegar novamente (git ta barrando)
    client = Client(account_sid, auth_token)
        
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    content_sid='', #tem que pegar de novo
    content_variables=f'{{"1":"{code}"}}',
    to=f"whatsapp:+{phone}"
    )
    print(message.sid)


#send_whatsapp_code(123456,5511952912079)