from rest_framework import serializers
from .models import BTCtoLN_SwapInvoice

class BTCtoLN_InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BTCtoLN_SwapInvoice
        fields = (
                'refund_address',
                'bolt11_invoice',
                'lockduration',
                'preimage',
                'funding_transaction',
                'redemption_transaction',
                'htlc_p2sh',
                'final_address',
        )

