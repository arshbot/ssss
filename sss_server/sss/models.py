import uuid
import json
from decimal import Decimal

from django.db import models
from django.conf import settings

from google.protobuf.json_format import MessageToJson as to_json
from bitcoin import rpc
from bitcoin.core import Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_IF, OP_ELSE, OP_ENDIF, \
    OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL, \
    OP_DROP, OP_CHECKLOCKTIMEVERIFY, OP_SHA256
from bitcoin.wallet import P2PKHBitcoinAddress, CBitcoinSecret, CBitcoinAddress

lnd = settings.LNDRPC

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

    is_finalized = models.BooleanField(default=False)

    @property
    def htlc_p2sh_address_balance(self) -> str:
        """ Lazy loading of live address received balance """
        bitcoind = rpc.Proxy()
        return str(Decimal(bitcoind.getreceivedbyaddress(self.htlc_p2sh)) * 10**-8)

    @property
    def htlc_p2sh(self) -> str:
        # We create connections on the fly because they'll time out quickly if
        # we don't
        bitcoind = rpc.Proxy()

        # We can decipher the hash of the preimage without explicitly asking
        # for it by taking it out of the payment request supplied
        decoded_pr = json.loads(to_json(
            lnd.decode_payment_request(self.bolt11_invoice))
        )
        hashed_preimage = decoded_pr['payment_hash']

        # Once these assignments are made, we want to lock them in so this
        # functions generates deterministically
        if not self.final_address_pubkey:
            final_address = bitcoind.getnewaddress()
            seckey = bitcoind.dumpprivkey(final_address)
            self.final_address_pubkey = seckey.pub.hex()

        if not self.redeemblock:
            curr_blockheight = bitcoind.getblockcount()
            self.redeemblock = curr_blockheight + self.lockduration

        # This is the HTLC locking script
        txin_redeemScript = CScript([
            OP_IF,
                OP_SHA256, bytes(hashed_preimage, 'utf8'), OP_EQUALVERIFY,OP_DUP, OP_HASH160,
                bytes(Hash160(bytes(self.final_address_pubkey, 'utf8'))),
            OP_ELSE,
                self.redeemblock, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP, OP_HASH160,
                bytes(Hash160(bytes(self.refund_address, 'utf8'))),
            OP_ENDIF,
                OP_EQUALVERIFY, OP_CHECKSIG
        ])

        self.save()

        # Generate a P2SH address from the locking script
        txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
        txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
        return str(txin_p2sh_address)

    @property
    def final_address(self):
        return str(P2PKHBitcoinAddress.from_pubkey(bytes.fromhex(self.final_address_pubkey)))

#     @property
#     def get_hashed_preimage(self):
#         pass
