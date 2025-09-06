# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import json

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "" #SID do Twilio tem que pegar novamente
auth_token = "" #token do Twilio tem que pegar novamente (git ta barrando)
client = Client(account_sid, auth_token)

def Twilio():
        
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    content_sid='', #tem que pegar de novo
    content_variables='{"1":"111111"}',
    to='whatsapp:+5511952912079'
    )
    print(message.sid)
