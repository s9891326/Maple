import logging

from twilio.rest import Client

from Maple.settings import base

account_sid = 'AC8ac01724e18b8f7e968696bf1e33c2f0'
auth_token = '2e1b38236a5c45144903442d33b8366a'
client = Client(base.ACCOUNT_SID, base.AUTH_TOKEN)


class TwilioService:
    def __init__(self):
        self.message_service_sid = 'MG0067298bd6d6510cce0512f4e6bffdd5'
        self.client = Client(base.ACCOUNT_SID, base.AUTH_TOKEN)
    
    def send_code(self, phone: str, code: str):
        try:
            logging.debug(f"TwilioService send_code phone: {phone}, code: {code}")
            # message = client.messages.create(
            #     messaging_service_sid=self.message_service_sid,
            #     body=code,
            #     to=phone
            # )
            # return message.sid
        except Exception as e:
            logging.error(f'TwilioService send_code error: {e}')


# +86
# 13723488824

# +886
# 0929100148
twilio_service = TwilioService()
