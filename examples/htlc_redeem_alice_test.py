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
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH # VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

import hashlib
from utils import VerifyScript
from bitcoin.core.script import *
from bitcoin.core.scripteval import *
from bitcoin.core.scripteval import _CheckExec, _ISA_BINOP, _ISA_UNOP, _CastToBool, _CheckSig
from ptpdb import set_trace

# def _EvalScript(stack, scriptIn, txTo, inIdx, flags=()):
#     """Evaluate a script
# 
#     """
#     if len(scriptIn) > MAX_SCRIPT_SIZE:
#         raise EvalScriptError('script too large; got %d bytes; maximum %d bytes' %
#                                         (len(scriptIn), MAX_SCRIPT_SIZE),
#                               stack=stack,
#                               scriptIn=scriptIn,
#                               txTo=txTo,
#                               inIdx=inIdx,
#                               flags=flags)
# 
#     altstack = []
#     vfExec = []
#     pbegincodehash = 0
#     nOpCount = [0]
#     for (sop, sop_data, sop_pc) in scriptIn.raw_iter():
#         fExec = _CheckExec(vfExec)
# 
#         def err_raiser(cls, *args):
#             """Helper function for raising EvalScriptError exceptions
# 
#             cls   - subclass you want to raise
# 
#             *args - arguments
# 
#             Fills in the state of execution for you.
#             """
#             raise cls(*args,
#                     sop=sop,
#                     sop_data=sop_data,
#                     sop_pc=sop_pc,
#                     stack=stack, scriptIn=scriptIn, txTo=txTo, inIdx=inIdx, flags=flags,
#                     altstack=altstack, vfExec=vfExec, pbegincodehash=pbegincodehash, nOpCount=nOpCount[0])
# 
# 
#         if sop in DISABLED_OPCODES:
#             err_raiser(EvalScriptError, 'opcode %s is disabled' % OPCODE_NAMES[sop])
# 
#         if sop > OP_16:
#             nOpCount[0] += 1
#             if nOpCount[0] > MAX_SCRIPT_OPCODES:
#                 err_raiser(MaxOpCountError)
# 
#         def check_args(n):
#             if len(stack) < n:
#                 err_raiser(MissingOpArgumentsError, sop, stack, n)
# 
# 
#         if sop <= OP_PUSHDATA4:
#             if len(sop_data) > MAX_SCRIPT_ELEMENT_SIZE:
#                 err_raiser(EvalScriptError,
#                            'PUSHDATA of length %d; maximum allowed is %d' %
#                                 (len(sop_data), MAX_SCRIPT_ELEMENT_SIZE))
# 
#             elif fExec:
#                 stack.append(sop_data)
#                 continue
# 
#         elif fExec or (OP_IF <= sop <= OP_ENDIF):
# 
#             if sop == OP_1NEGATE or ((sop >= OP_1) and (sop <= OP_16)):
#                 v = sop - (OP_1 - 1)
#                 stack.append(bitcoin.core._bignum.bn2vch(v))
# 
#             elif sop in _ISA_BINOP:
#                 _BinOp(sop, stack, err_raiser)
# 
#             elif sop in _ISA_UNOP:
#                 _UnaryOp(sop, stack, err_raiser)
# 
#             elif sop == OP_2DROP:
#                 check_args(2)
#                 stack.pop()
#                 stack.pop()
# 
#             elif sop == OP_2DUP:
#                 check_args(2)
#                 v1 = stack[-2]
#                 v2 = stack[-1]
#                 stack.append(v1)
#                 stack.append(v2)
# 
#             elif sop == OP_2OVER:
#                 check_args(4)
#                 v1 = stack[-4]
#                 v2 = stack[-3]
#                 stack.append(v1)
#                 stack.append(v2)
# 
#             elif sop == OP_2ROT:
#                 check_args(6)
#                 v1 = stack[-6]
#                 v2 = stack[-5]
#                 del stack[-6]
#                 del stack[-5]
#                 stack.append(v1)
#                 stack.append(v2)
# 
#             elif sop == OP_2SWAP:
#                 check_args(4)
#                 tmp = stack[-4]
#                 stack[-4] = stack[-2]
#                 stack[-2] = tmp
# 
#                 tmp = stack[-3]
#                 stack[-3] = stack[-1]
#                 stack[-1] = tmp
# 
#             elif sop == OP_3DUP:
#                 check_args(3)
#                 v1 = stack[-3]
#                 v2 = stack[-2]
#                 v3 = stack[-1]
#                 stack.append(v1)
#                 stack.append(v2)
#                 stack.append(v3)
# 
#             elif sop == OP_CHECKMULTISIG or sop == OP_CHECKMULTISIGVERIFY:
#                 tmpScript = CScript(scriptIn[pbegincodehash:])
#                 _CheckMultiSig(sop, tmpScript, stack, txTo, inIdx, flags, err_raiser, nOpCount)
# 
#             elif sop == OP_CHECKSIG or sop == OP_CHECKSIGVERIFY:
#                 set_trace()
#                 check_args(2)
#                 vchPubKey = stack[-1]
#                 vchSig = stack[-2]
#                 tmpScript = CScript(scriptIn[pbegincodehash:])
# 
#                 # Drop the signature, since there's no way for a signature to sign itself
#                 #
#                 # Of course, this can only come up in very contrived cases now that
#                 # scriptSig and scriptPubKey are processed separately.
#                 tmpScript = FindAndDelete(tmpScript, CScript([vchSig]))
# 
#                 ok = _CheckSig(vchSig, vchPubKey, tmpScript, txTo, inIdx,
#                                err_raiser)
#                 if not ok and sop == OP_CHECKSIGVERIFY:
#                     err_raiser(VerifyOpFailedError, sop)
# 
#                 else:
#                     stack.pop()
#                     stack.pop()
# 
#                     if ok:
#                         if sop != OP_CHECKSIGVERIFY:
#                             stack.append(b"\x01")
#                     else:
#                         # FIXME: this is incorrect, but not caught by existing
#                         # test cases
#                         stack.append(b"\x00")
# 
#             elif sop == OP_CODESEPARATOR:
#                 pbegincodehash = sop_pc
# 
#             elif sop == OP_DEPTH:
#                 bn = len(stack)
#                 stack.append(bitcoin.core._bignum.bn2vch(bn))
# 
#             elif sop == OP_DROP:
#                 check_args(1)
#                 stack.pop()
# 
#             elif sop == OP_DUP:
#                 check_args(1)
#                 v = stack[-1]
#                 stack.append(v)
# 
#             elif sop == OP_ELSE:
#                 set_trace()
#                 if len(vfExec) == 0:
#                     err_raiser(EvalScriptError, 'ELSE found without prior IF')
#                 vfExec[-1] = not vfExec[-1]
# 
#             elif sop == OP_ENDIF:
#                 if len(vfExec) == 0:
#                     err_raiser(EvalScriptError, 'ENDIF found without prior IF')
#                 vfExec.pop()
# 
#             elif sop == OP_EQUAL:
#                 check_args(2)
#                 v1 = stack.pop()
#                 v2 = stack.pop()
# 
#                 if v1 == v2:
#                     stack.append(b"\x01")
#                 else:
#                     stack.append(b"")
# 
#             elif sop == OP_EQUALVERIFY:
#                 set_trace()
#                 check_args(2)
#                 v1 = stack[-1]
#                 v2 = stack[-2]
# 
#                 if v1 == v2:
#                     stack.pop()
#                     stack.pop()
#                 else:
#                     err_raiser(VerifyOpFailedError, sop)
# 
#             elif sop == OP_FROMALTSTACK:
#                 if len(altstack) < 1:
#                     err_raiser(MissingOpArgumentsError, sop, altstack, 1)
#                 v = altstack.pop()
#                 stack.append(v)
# 
#             elif sop == OP_HASH160:
#                 check_args(1)
#                 stack.append(bitcoin.core.serialize.Hash160(stack.pop()))
# 
#             elif sop == OP_HASH256:
#                 check_args(1)
#                 stack.append(bitcoin.core.serialize.Hash(stack.pop()))
# 
#             elif sop == OP_IF or sop == OP_NOTIF:
#                 set_trace()
#                 val = False
# 
#                 if fExec:
#                     check_args(1)
#                     vch = stack.pop()
#                     val = _CastToBool(vch)
#                     if sop == OP_NOTIF:
#                         val = not val
# 
#                 vfExec.append(val)
# 
# 
#             elif sop == OP_IFDUP:
#                 check_args(1)
#                 vch = stack[-1]
#                 if _CastToBool(vch):
#                     stack.append(vch)
# 
#             elif sop == OP_NIP:
#                 check_args(2)
#                 del stack[-2]
# 
#             elif sop == OP_NOP:
#                 pass
# 
#             elif sop >= OP_NOP1 and sop <= OP_NOP10:
#                 set_trace()
#                 if SCRIPT_VERIFY_DISCOURAGE_UPGRADABLE_NOPS in flags:
#                     err_raiser(EvalScriptError, "%s reserved for soft-fork upgrades" % OPCODE_NAMES[sop])
#                 else:
#                     pass
# 
#             elif sop == OP_OVER:
#                 check_args(2)
#                 vch = stack[-2]
#                 stack.append(vch)
# 
#             elif sop == OP_PICK or sop == OP_ROLL:
#                 check_args(2)
#                 n = _CastToBigNum(stack.pop(), err_raiser)
#                 if n < 0 or n >= len(stack):
#                     err_raiser(EvalScriptError, "Argument for %s out of bounds" % OPCODE_NAMES[sop])
#                 vch = stack[-n-1]
#                 if sop == OP_ROLL:
#                     del stack[-n-1]
#                 stack.append(vch)
# 
#             elif sop == OP_RETURN:
#                 err_raiser(EvalScriptError, "OP_RETURN called")
# 
#             elif sop == OP_RIPEMD160:
#                 check_args(1)
# 
#                 h = hashlib.new('ripemd160')
#                 h.update(stack.pop())
#                 stack.append(h.digest())
# 
#             elif sop == OP_ROT:
#                 check_args(3)
#                 tmp = stack[-3]
#                 stack[-3] = stack[-2]
#                 stack[-2] = tmp
# 
#                 tmp = stack[-2]
#                 stack[-2] = stack[-1]
#                 stack[-1] = tmp
# 
#             elif sop == OP_SIZE:
#                 check_args(1)
#                 bn = len(stack[-1])
#                 stack.append(bitcoin.core._bignum.bn2vch(bn))
# 
#             elif sop == OP_SHA1:
#                 check_args(1)
#                 stack.append(hashlib.sha1(stack.pop()).digest())
# 
#             elif sop == OP_SHA256:
#                 check_args(1)
#                 stack.append(hashlib.sha256(stack.pop()).digest())
# 
#             elif sop == OP_SWAP:
#                 check_args(2)
#                 tmp = stack[-2]
#                 stack[-2] = stack[-1]
#                 stack[-1] = tmp
# 
#             elif sop == OP_TOALTSTACK:
#                 check_args(1)
#                 v = stack.pop()
#                 altstack.append(v)
# 
#             elif sop == OP_TUCK:
#                 check_args(2)
#                 vch = stack[-1]
#                 stack.insert(len(stack) - 2, vch)
# 
#             elif sop == OP_VERIFY:
#                 check_args(1)
#                 v = _CastToBool(stack[-1])
#                 if v:
#                     stack.pop()
#                 else:
#                     raise err_raiser(VerifyOpFailedError, sop)
# 
#             elif sop == OP_WITHIN:
#                 check_args(3)
#                 bn3 = _CastToBigNum(stack[-1], err_raiser)
#                 bn2 = _CastToBigNum(stack[-2], err_raiser)
#                 bn1 = _CastToBigNum(stack[-3], err_raiser)
#                 stack.pop()
#                 stack.pop()
#                 stack.pop()
#                 v = (bn2 <= bn1) and (bn1 < bn3)
#                 if v:
#                     stack.append(b"\x01")
#                 else:
#                     # FIXME: this is incorrect, but not caught by existing
#                     # test cases
#                     stack.append(b"\x00")
# 
#             else:
#                 err_raiser(EvalScriptError, 'unsupported opcode 0x%x' % sop)
# 
#         # size limits
#         if len(stack) + len(altstack) > MAX_STACK_ITEMS:
#             err_raiser(EvalScriptError, 'max stack items limit reached')
# 
#     # Unterminated IF/NOTIF/ELSE block
#     if len(vfExec):
#         raise EvalScriptError('Unterminated IF/ELSE block',
#                               stack=stack,
#                               scriptIn=scriptIn,
#                               txTo=txTo,
#                               inIdx=inIdx,
#                               flags=flags)
# 
# 
# 
# def EvalScript(stack, scriptIn, txTo, inIdx, flags=()):
#     """Evaluate a script
#     stack    - Initial stack
#     scriptIn - Script
#     txTo     - Transaction the script is a part of
#     inIdx    - txin index of the scriptSig
#     flags    - SCRIPT_VERIFY_* flags to apply
#     """
# 
#     try:
#         _EvalScript(stack, scriptIn, txTo, inIdx, flags=flags)
#     except CScriptInvalidError as err:
#         raise EvalScriptError(repr(err),
#                               stack=stack,
#                               scriptIn=scriptIn,
#                               txTo=txTo,
#                               inIdx=inIdx,
#                               flags=flags)
# 
# def VerifyScript(scriptSig, scriptPubKey, txTo, inIdx, flags=()):
#     """Verify a scriptSig satisfies a scriptPubKey
#     scriptSig    - Signature
#     scriptPubKey - PubKey
#     txTo         - Spending transaction
#     inIdx        - Index of the transaction input containing scriptSig
#     Raises a ValidationError subclass if the validation fails.
#     """
#     stack = []
#     from bitcoin.core.scripteval import _CastToBool
#     set_trace()
#     EvalScript(stack, scriptSig, txTo, inIdx, flags=flags)
#     if SCRIPT_VERIFY_P2SH in flags:
#         stackCopy = list(stack)
#     print('stack ' + str(stack))
#     EvalScript(stack, scriptPubKey, txTo, inIdx, flags=flags)
#     if len(stack) == 0:
#         raise VerifyScriptError("scriptPubKey left an empty stack")
#     if not _CastToBool(stack[-1]):
#         print('fuckin hoes')
#         print(stack)
#         raise VerifyScriptError("scriptPubKey returned false")
# 
#     # Additional validation for spend-to-script-hash transactions
#     if SCRIPT_VERIFY_P2SH in flags and scriptPubKey.is_p2sh():
#         if not scriptSig.is_push_only():
#             raise VerifyScriptError("P2SH scriptSig not is_push_only()")
# 
#         # restore stack
#         stack = stackCopy
# 
#         # stack cannot be empty here, because if it was the
#         # P2SH  HASH <> EQUAL  scriptPubKey would be evaluated with
#         # an empty stack and the EvalScript above would return false.
#         assert len(stack)
# 
#         pubKey2 = CScript(stack.pop())
# 
#         EvalScript(stack, pubKey2, txTo, inIdx, flags=flags)
# 
#         if not len(stack):
#             raise VerifyScriptError("P2SH inner scriptPubKey left an empty stack")
# 
#         if not _CastToBool(stack[-1]):
#             raise VerifyScriptError("P2SH inner scriptPubKey returned false")
# 
#     if SCRIPT_VERIFY_CLEANSTACK in flags:
#         assert SCRIPT_VERIFY_P2SH in flags
# 
#         if len(stack) != 1:
#             raise VerifyScriptError("scriptPubKey left extra items on stack")


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

# privkey of Alice, used to sign the redeemTx
sender_seckey = proxy.dumpprivkey(senderpubkey)

# privkey of Bob, used to construct the htlc
recipient_seckey = proxy.dumpprivkey(recipientpubkey)

# How long the htlc will last until it times out
lockduration = 1
curr_blockheight = proxy.getblockcount()
redeemblocknum = curr_blockheight + lockduration

# We construct the locking script in the form of a standard bip199 htlc
txin_redeemScript = CScript([
    OP_IF,
        OP_SHA256, h, OP_EQUALVERIFY,OP_DUP, OP_HASH160, bytes(Hash160(recipient_seckey.pub)),
    OP_ELSE,
        redeemblocknum, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP, OP_HASH160, bytes(Hash160(sender_seckey.pub)),
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

# Construct the transaction which will redeem the htlc via the second payment route
txinfo = proxy.gettransaction(fund_tx)
txin = CMutableTxIn(COutPoint(fund_tx, txinfo['details'][0]['vout']))
# By default, python-bitcoinlib disables locktime via nSequence, so we must enable
txin.nSequence = 0xfffffffe

default_fee = 0.001*COIN

txout = CMutableTxOut(amount - default_fee, senderpubkey.to_scriptPubKey())
tx = CMutableTransaction([txin], [txout])
tx.nLockTime = redeemblocknum
# Sign the redeem script with Alice's private key ( for whose address the first payment path
# is set up exclusively for )
sighash = SignatureHash(txin_redeemScript, tx, 0, SIGHASH_ALL)
sig = sender_seckey.sign(sighash) + bytes([SIGHASH_ALL])

# Load the script sig of Bob's redemption transaction with the appropriate values
txin.scriptSig = CScript([sig, sender_seckey.pub, 0, txin_redeemScript])

# Verify
VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

# Fast forward time
proxy.generatetoaddress(lockduration, proxy.getnewaddress())

# Send
txid = proxy.sendrawtransaction(tx)

# Confirm
proxy.generatetoaddress(1, proxy.getnewaddress())
