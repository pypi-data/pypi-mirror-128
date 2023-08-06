from typing import List, Optional

from django.urls import reverse
from ipware.ip import get_client_ip

from django.utils.translation import get_language
from django_pay2.decorators import handle_debug
from django_pay2.exceptions import CreatePaymentError
from django_pay2.models import Payment
from django_pay2.settings import payment_settings
from django_pay2.payment_methods import PaymentRedirect

from .api import TinkoffOrderItem, TinkoffApiError
from .services import get_tinkoff_api


@handle_debug
def create_tinkoff_payment(
    request,
    amount,
    desc,
    receiver,
    items: List[TinkoffOrderItem],
    client_email: Optional[str] = None,
    client_phone: Optional[str] = None,
):
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    try:
        api = get_tinkoff_api()
        notification_url = reverse("django_pay2:tinkoff:notify")
        success_url = reverse("django_pay2:success")
        fail_url = reverse("django_pay2:fail")
        result = api.init_payment(
            amount,
            str(payment.id),
            get_client_ip(request)[0],
            desc,
            get_language(),
            notification_url,
            success_url,
            fail_url,
            items=items,
            client_email=client_email,
            client_phone=client_phone,
            email_company=payment_settings.TINKOFF.email_company,
            taxation=payment_settings.TINKOFF.taxation,
        )
        return PaymentRedirect(result.payment_url)
    except TinkoffApiError as exc:
        payment.reject()
        raise CreatePaymentError(str(exc))
