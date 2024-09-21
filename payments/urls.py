from django.urls import path
from .views import make_payment, revert_payment

urlpatterns = [
    path('make-payment/', make_payment, name='make-payment'),
    path('revert-payment/<int:payment_id>/', revert_payment, name='revert-payment'),
]
