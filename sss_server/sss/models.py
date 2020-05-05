import uuid

from django.db import models

class BTCtoLN_SwapInvoice(models.Model):

    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    refund_address = models.CharField(max_length=35)

    bolt11_invoice = models.CharField(max_length=1000)

    lockduration = models.IntegerField(default=1)

    redeemblock = models.IntegerField(null=True)

    # Address that ssss will use to sweep funds from the htlc upon completion
    final_address_pubkey = models.CharField(max_length=35, null=True)

    preimage = models.CharField(max_length=500, null=True)

    funding_transaction = models.CharField(max_length=1000, null=True)

    redemption_transaction = models.CharField(max_length=1000, null=True)

    @property
    def htlc_p2sh(self):
        return "fuck u"

#     @property
#     def get_hashed_preimage(self):
#         pass
