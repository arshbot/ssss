from django.urls import path, include
from . import views

urlpatterns = [
    path('btclnswap/', views.BTCtoLN_SwapInvoiceCreate.as_view()),
    path('btclnswap/<uuid:invoice_id>', views.BTCtoLN_SwapInvoicePartialUpdate.as_view()),
]
