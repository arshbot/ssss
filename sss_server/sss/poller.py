import pusher
from bitcoin import rpc

from django.utils.timezone import now, timedelta

from .models import BTCtoLN_SwapInvoice

class Poller():

    def __init__(cls):
        self.bitcoind = rpc.Proxy()
        self.pusher_client = pusher.Pusher(app_id, key, secret, cluster=u'cluster')
        return cls

    def start():
        while True:
            # Very simple, inefficient way of polling addresses from bitcoind.
            # If different swap types are implemented, I'd subclass 
            # BTCtoLN_SwapInvoice with SwapInvoice and query against the parent
            for invoice in BTCtoLN_SwapInvoice.objects.filter(
                created_at=now-timedelta(hours=1),
                is_paid=False,
                is_finalized=False, # Should be redundant but eh
            ):
                amt = self.bitcoind.getreceivedbyaddress(invoice.htlc_p2sh)

                invoice.amount_to_swap = amt
                invoice.is_paid = True
                invoice.save()

                self.pusher_client.trigger(
                        [u'address_updates'],
                        invoice.htlc_p2sh,
                        {u'amount': invoice.amount_to_swap})

