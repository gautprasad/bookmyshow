from django.urls import path
from .views import make_payment, revert_payment, get_all_payments

urlpatterns = [
    path('make-payment/', make_payment, name='make_payment'),
    path('revert-payment/<int:payment_id>/', revert_payment, name='revert_payment'),
    path('get-all-payments/', get_all_payments, name='get_all_payments'),
]
