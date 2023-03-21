from __future__ import print_function

from binascii import hexlify
from Crypto.Hash import keccak
from utils import tobe256, bytes_to_int, randb256
import sys
sys.path.append('../bitcoin')
from main import encode_pubkey



def pack_signature(v, r, s):
	"""
	This saves a byte by using the last bit of `s` to store `v`
	This allows the signature to be packed into two 256bit words
	This is possible because `s` is mod `N`, and the highest bit 
	doesn't seem to be used...

	Having put it through a SAT solver it's 100% possible for this
	bit to be set, but in reality it's very unlikely that this
	fails, whereas packing it into the `r` value fails 50% of the
	time as you'd expect....
	"""
	assert v == 27 or v == 28
	v = (v - 27) << 255
	return tobe256(r), tobe256(s | v)


def unpack_signature(r, sv):
	sv = bytes_to_int(sv)
	if (sv & (1 << 255)):
		v = 28
		sv = sv ^ (1 << 255)
	else:
		v = 27
	return v, bytes_to_int(r), sv


def pubkey_to_ethaddr(pubkey):
	if isinstance(pubkey, tuple):
		assert len(pubkey) == 2
		pubkey = encode_pubkey(pubkey, 'bin')
	return hexlify(keccak.new(digest_bits=256,data=pubkey[1:]).digest()[12:])
