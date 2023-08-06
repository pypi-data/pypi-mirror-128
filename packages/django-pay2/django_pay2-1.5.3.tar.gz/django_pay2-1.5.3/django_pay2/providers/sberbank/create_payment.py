from django_pay2.decorators import handle_debug
from django_pay2.models import Payment
from django_pay2.settings import payment_settings
from django.http import HttpRequest
from django.db.models import Model
from typing import Any, Optional
from django_pay2.payment_methods import PaymentRedirect

from .api import SberbankApi


def get_api() -> SberbankApi:
    return SberbankApi(
        username=payment_settings.SBERBANK.username,
        password=payment_settings.SBERBANK.password,
    )


@handle_debug
def create_sberbank_payment(
    request: HttpRequest,
    amount: Any,
    desc: str,
    receiver: Model,
    return_url: Optional[str] = None,
    fail_url: Optional[str] = None,
    page_view: Optional[str] = None,
    phone: Optional[str] = None,
) -> PaymentRedirect:
    return_url = return_url or payment_settings.SBERBANK.return_url
    fail_url = fail_url or payment_settings.SBERBANK.fail_url
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    api = get_api()
    return api.register_payment(
        order_num=str(payment.id),
        amount=str(amount),
        return_url=return_url,
        fail_url=fail_url,
        description=desc,
        page_view=page_view,
        phone=phone,
    )
