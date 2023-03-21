#This script is use to retrieve the data needed to build our ring
#It goes in 4 stpes : 
#   - getLatestTx -> this function get the latest tx on the XRPL and return the address assiociated
#   - getAcountInfo -> this function retrieve the info on the address, if the balance of the address is superior to the treshold we will use this address in our ring
#   - getAccountKey -> this function retrieve the pubkey from an acount
#   - get_y_from_x -> This function compute the y coordinate by passing it the x coordinate (public key on XRPL)
import requests
import json
from ecdsa import curves, ecdsa
from xrpl.utils import xrp_to_drops

url = "	https://s.altnet.rippletest.net:51234"
p = 2**256 - 2**32 - 977

# get the latest tx from the ledger
# call tx_history API method from XRPL
# return account address
def getLatestTx():
    payload = {
        "method": "tx_history",
        "params": [
            {
                "start": 0
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    txs = result['result']['txs']
    accounts = []
    for i in range(len(txs)):
        accounts.append(txs[i]['Account'])
    print("Retrieve tx ok")
    return(accounts)

# get the account Info
# call the account_info API method from XRPL
# If the balance of the account is superior to treshold return the latest tx id to get the pub key
def getAccountInfo(treshold, account): 

    payload = {
        "method": "account_info",
        "params": [
            {
                "account": account
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    balance = result['result']['account_data']['Balance']
    if (int(balance) < int(xrp_to_drops(treshold))) :
        return ""
    return result['result']['account_data']['PreviousTxnID']

# return the pubkey (x points on secp256k1) from a tx hash
# call tx API method from XRPL 
# return the signing PubKey
def getAccountKey(txId):

    payload = {
       "method": "tx",
    "params": [
        {
            "transaction": txId
        }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    pubKey = result['result']['SigningPubKey'][2:]
    return pubKey
    
# get the couple x,y from an account
def get_y_from_x(hex_x):
    # Convert hex string to integer
    x = int(hex_x, 16)
    # Compute y-coordinate
    y = None
    try:
        y_squared = (x**3 +7) %p
        y = ecdsa.numbertheory.square_root_mod_prime(y_squared, p)
        
    except:
        print("Error computing y-coordinate.")
    if(type(y)!=None):
        return(x,y)
    

# function to build the ring for the signature
# take a treshold in parameters
# return the ring that will be use in the signature (an array of tuple) : [(int,int)]
def getRing(treshold):
    accountList = getLatestTx()
    tempoTxList=[]
    for i in range(len(accountList)): 
        tempo = getAccountInfo(treshold,accountList[i])
        if tempo !="" :
            tempoTxList.append(tempo)
    txList = list(set(tempoTxList))

    points = []
    for j in range(len(txList)): 
       
        tempoPoint = get_y_from_x(getAccountKey(txList[j]))
        print(tempoPoint[1])
        points.append(tempoPoint)
    print(points)
    return points



