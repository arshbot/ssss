#!/usr/bin/env python3

import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import bitcoin
from bitcoin import rpc
from bitcoin import SelectParams
from bitcoin.core import b2x, lx, b2lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_IF, OP_ELSE, OP_ENDIF, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.script import OP_DROP, OP_CHECKLOCKTIMEVERIFY, OP_SHA256
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

import hashlib

SelectParams('regtest')
proxy = bitcoin.rpc.Proxy()

# Set the preimage. This is the secret Bob will need to redeem the htlc
preimage = bytes(b'preimage'.hex(), 'utf8')

# Hashed version of the preimage which we can safely store on the blockchain
# and use to verify against what Bob offers
h = hashlib.sha256(preimage).digest()

# Bob
recipientpubkey = proxy.getnewaddress()

# Alice
senderpubkey = proxy.getnewaddress()

# privkey of Bob, used to sign the redeemTx
seckey = proxy.dumpprivkey(recipientpubkey)

# How long the htlc will last until it times out
lockduration = 1
curr_blockheight = proxy.getblockcount()
redeemblocknum = curr_blockheight + lockduration

# We construct the locking script in the form of a standard bip199 htlc
txin_redeemScript = CScript([
    OP_IF,
        OP_SHA256, h, OP_EQUALVERIFY,OP_DUP, OP_HASH160, bytes(Hash160(seckey.pub)),
    OP_ELSE,
        redeemblocknum, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP, OP_HASH160, bytes(Hash160(seckey.pub)),
    OP_ENDIF,
        OP_EQUALVERIFY, OP_CHECKSIG
])

# Generate a P2SH address from the locking script
txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
p2sh = str(txin_p2sh_address)

# Load the htlc
amount = 1.0*COIN
fund_tx = proxy.sendtoaddress(txin_p2sh_address, amount)

# Construct the transaction which will redeem the htlc via the first payment route
txinfo = proxy.gettransaction(fund_tx)
txin = CMutableTxIn(COutPoint(fund_tx, txinfo['details'][0]['vout']))
default_fee = 0.001*COIN
txout = CMutableTxOut(amount - default_fee, recipientpubkey.to_scriptPubKey())
tx = CMutableTransaction([txin], [txout])

# Sign the redeem script with Bob's private key ( for whose address the first payment path
# is set up exclusively for )
sighash = SignatureHash(txin_redeemScript, tx, 0, SIGHASH_ALL)
sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

# Load the script sig of Bob's redemption transaction with the appropriate values
txin.scriptSig = CScript([sig, seckey.pub, preimage, preimage, txin_redeemScript])

# Verify
VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

# Fast forward time
proxy.generatetoaddress(lockduration, proxy.getnewaddress())

# Send
txid = proxy.sendrawtransaction(tx)

# Confirm
from ptpdb import set_trace
set_trace()
proxy.generatetoaddress(1, proxy.getnewaddress())
