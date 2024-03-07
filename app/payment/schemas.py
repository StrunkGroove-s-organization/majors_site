from pydantic.dataclasses import dataclass


@dataclass
class SubscriptionData:
    type_sub: str
    days: int
    amount: float
    currency: str


@dataclass
class PaymentData:
    token: str
    type_subscription: str
    currency: str
    amount: float