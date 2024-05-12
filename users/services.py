import os

import stripe
from dotenv import load_dotenv

from users.models import Payment

load_dotenv()


def get_pay(amount_payment, user):
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_payment,
            currency="usd",
            payment_method_types=["card"]
        )

        payment = Payment.objects.create(
            user=user,
            amount_payment=amount_payment,
            stripe_id=payment_intent.id
        )

        return payment
    except stripe.error.StripeError as e:
        # Обработка ошибок Stripe
        print(f"Произошла ошибка при создании платежа: {e}")
        return None
