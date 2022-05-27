import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.mail import send_mail
from paypalrestsdk import notifications
from pprint import pprint

@method_decorator(csrf_exempt, name="dispatch")
class ProcessWebhookView(View):
    def post(self, request):
        if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
            return HttpResponseBadRequest()

        auth_algo = request.META['HTTP_PAYPAL_AUTH_ALGO']
        cert_url = request.META['HTTP_PAYPAL_CERT_URL']
        transmission_id = request.META['HTTP_PAYPAL_TRANSMISSION_ID']
        transmission_sig = request.META['HTTP_PAYPAL_TRANSMISSION_SIG']
        transmission_time = request.META['HTTP_PAYPAL_TRANSMISSION_TIME']
        webhook_id = settings.PAYPAL_WEBHOOK_ID
        event_body = request.body.decode(request.encoding or "utf-8")

        valid = notifications.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=transmission_time,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            actual_sig=transmission_sig,
            auth_algo=auth_algo,
        )

        if not valid:
            return HttpResponseBadRequest()

        webhook_event = json.loads(event_body)

        event_type = webhook_event["event_type"]

        print("CHECKPOINT 1")

        print(event_type)

        print("CHECKPOINT 2")

        pprint(webhook_event)

        print("CHECKPOINT 3")

        CHECKOUT_ORDER_APPROVED = "CHECKOUT.ORDER.APPROVED"

        print("EVENT TYPE:", event_type, CHECKOUT_ORDER_APPROVED)

        if event_type == CHECKOUT_ORDER_APPROVED:
            customer_email = webhook_event["resource"]["payer"]["email_address"]
            product_link = "https://prometeoapi.com"
            send_mail(
                subject="Your access",
                message=f"Thank you for purchasing my product. Here is the link: {product_link}",
                from_email="your@email.com",
                recipient_list=[customer_email]
            )

        print("CHECKPOINT 4")

        return HttpResponse()
