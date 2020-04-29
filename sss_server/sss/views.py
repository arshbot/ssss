from django.shortcuts import render
from django.db import transaction
from rest_framework import generics, mixins

from .models import BTCtoLN_SwapInvoice
from .serializers import BTCtoLN_InvoiceSerializer

class BTCtoLN_SwapInvoiceCreate(generics.ListCreateAPIView):
    queryset = BTCtoLN_SwapInvoice.objects.all()
    serializer_class = BTCtoLN_InvoiceSerializer

#     @transaction.atomic
#     def perform_create(self, serializer):
#         invoice = serializer.save()

class BTCtoLN_SwapInvoicePartialUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = BTCtoLN_SwapInvoice.objects.all()
    serializer_class = BTCtoLN_InvoiceSerializer

    def update(self):
        pass
