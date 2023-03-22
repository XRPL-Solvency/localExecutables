from __future__ import print_function
from binascii import unhexlify
from ring_signature.utils import hashs, bytes_to_int
from ring_signature.secp256k1 import *



"""
This implements AOS 1-out-of-n ring signature which require only `n+1`
scalars to validate in addition to the `n` public keys.

''Intuitively, this scheme is a ring of Schnorr signatures where each
challenge is taken from the previous step. Indeed, it is the Schnorr
signature scheme where n=1''

For more information, see:

 - https://www.iacr.org/cryptodb/archive/2002/ASIACRYPT/50/50.pdf

When verifying the ring only the initial seed value for `c` is provided
instead of supplying a value of `c` for each link in the ring. The hash
of the previous link is used as the next value of `c`.

The ring is successfully verified if the last value of `c` matches the
seed value.

For more information on turning this scheme into a linkable ring:

 - https://bitcointalk.org/index.php?topic=972541.msg10619684#msg10619684
 - https://eprint.iacr.org/2004/027.pdf

The Hacky version abuses the Ethereum `ecrecover` operator to perform
the Schnorr signature verifications.
"""


def hacky_schnorr_calc(xG, s, e, message):
	
	
	kG = hackymul(xG[0], xG[1], e, m=(((N - s) % N) * xG[0]) % N)
	#print(colored(kG,'red'))
	return hashs(xG[0], xG[1], bytes_to_int(unhexlify(kG)), message)


def haosring_randkeys(n=4):
	skeys = [randsn() for _ in range(0, n)]
	
	pkeys = [sbmul(sk) for sk in skeys]
	
	i = randint(0, n-1)
	return pkeys, (pkeys[i], skeys[i])


def haosring_sign(pkeys, mypair, tees=None, alpha=None, message=None):
	assert len(pkeys) > 0
	message = message or hashpn(*pkeys)
	mypk, mysk = mypair
	myidx = pkeys.index(mypk)

	tees = tees or [randsn() for _ in range(0, len(pkeys))]
	cees = [0 for _ in range(0, len(pkeys))]
	alpha = alpha or randsn()

	i = myidx
	n = 0
	while n < len(pkeys):
		idx = i % len(pkeys)
		c = alpha if n == 0 else cees[idx-1]
		
		cees[idx] = hacky_schnorr_calc(pkeys[idx], tees[idx], c, message)
		n += 1
		i += 1

	# Then close the ring, which proves we know the secret for one ring item
	# TODO: split into schnorr_alter
	alpha_gap = submodn(alpha, cees[myidx-1])
	tees[myidx] = addmodn(tees[myidx], mulmodn(mysk, alpha_gap))
	print(pkeys, tees, cees[-1])
	return pkeys, tees, cees[-1]


def convert_hex_to_int_pairs(hex_str):
     # split the input string into a list of hex strings
        hex_list = hex_str.split(',')

     # convert each hex string to an integer
        int_list = [int(hex_val, 16) for hex_val in hex_list]

        # group the integers into pairs
        int_pairs = [(int_list[i], int_list[i+1]) for i in range(0, len(int_list), 2)]
        print(int_pairs)
        return int_pairs

def haosring_check(pkeys, tees, seed, message=12):
	assert len(pkeys) > 0
	assert len(tees) == len(pkeys)
	message = message or hashpn(*pkeys)
	c = seed
	for i, pkey in enumerate(pkeys):
		c = hacky_schnorr_calc(pkey, tees[i], c, message)
	return c == seed

def hex_string_to_int_tuple(hex_str):
    hex_str_list = hex_str.split(',')
    int_tuple = tuple(int(x, 16) for x in hex_str_list)
    return int_tuple

def convertHexPubKeyToInt(_x,_y):
	x = int(_x,16)
	y = int(_y,16)
	return x,y
proof = ([(93883134863173215788731420728266254126131871086462193152802054603557726022467, 4983903805493604254066352911874397023198698806767810992210061217548711739371), (68933786060008225531266081621324705938856172874169463551105378089507126055818, 66967260465951208659776075538986596487654133630819954968837151702991554980137), (107297525979540163001814164980021665629461792361374027857966449285740942577901, 35363502556009482218540385130316680125936164044015092289675406112657791677120), (78231770735022344491913644720918860684395867430231623980286824317973133056125, 195909507431195278071335924137301534145369384136919107738678783654359924459)], [75105168075842879175766512301878260770671852173554425992338720241944658721567, 136589906420459119191801516190789167163693673805703536556042829491282242579, 7793946511354125792161457214176129630519689696363054112820155194773284667547, 99655241043502022979073981806439748058415312829016754127552484514822908465540], 89209207009142146437328932364716460187950090604014317432980023753671240974457)
print(haosring_check(*proof))