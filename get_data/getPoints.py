# This script compute the x,y points given a private key
# We use it because the function in the wrpl.wallet library derive more than 1 time and so the private key doesn't match with the pubkey
# Take a seed in arguments and return an array of tuple [(int,int),int] -> [(x,y),SecretKey]

from xrpl.wallet import Wallet
from xrpl.utils import xrp_to_drops
import ecdsa
import math
import requests
import json

p = 2**256 - 2**32 - 977

def getPoints(seed):
    issuer_wallet = Wallet(seed=seed, sequence=0)
    issuer_private_key = issuer_wallet.private_key[2:]   
    private_key_int = int(issuer_private_key,16)
    num_bytes = math.ceil(private_key_int.bit_length() / 8)
    
    sk = ecdsa.SigningKey.from_string(private_key_int.to_bytes(num_bytes,byteorder='big'), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = vk.to_string()
    print(len(public_key))
    x = int.from_bytes(public_key[0:32], byteorder='big')
    y = int.from_bytes(public_key[33:64],  byteorder='big')
    return[(x,y),int(issuer_private_key,16)]

def getAccountBalance(treshold, seed): 

    issuer_wallet = Wallet(seed=seed, sequence=0)
    issuer_address =  issuer_wallet.classic_address
    print(issuer_address)
    url = "	https://s.altnet.rippletest.net:51234"
    payload = {
        "method": "account_info",
        "params": [
            {
                "account": issuer_address
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    print(result)
    balance = result['result']['account_data']['Balance']
    print(balance)
    print(xrp_to_drops(treshold))
    if (int(balance)>int(xrp_to_drops(treshold))):
          return True
    else : 
         return False


   
