import logging

from twilio.rest import Client

from Maple.settings import base


class TwilioService:
    def __init__(self):
        self.message_service_sid = 'MG0067298bd6d6510cce0512f4e6bffdd5'
        self.client = Client(base.ACCOUNT_SID, base.AUTH_TOKEN)
    
    def send_code(self, phone: str, code: str) -> bool:
        try:
            logging.debug(f"TwilioService send_code phone: {phone}, code: {code}")
            # message = client.messages.create(
            #     messaging_service_sid=self.message_service_sid,
            #     body=code,
            #     to=phone
            # )
            return True
        except Exception as e:
            logging.error(f'TwilioService send_code error: {e}')
            return False


# +86
# 13723488824

# +886
# 0929100148
twilio_service = TwilioService()
