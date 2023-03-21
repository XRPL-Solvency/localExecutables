# This script imports all others. It then generates the proof and stores it on ipfs. The proof is then associated to an NFT, the URI being the ipfs link.
from ring_signature.hackyaosring import haosring_sign
import requests
from get_data.get_data import getRing
from get_data.getPoints import getPoints,getAccountBalance
from get_data.mint_nft import mintNFT

# function to send data to ipfs using infura gateway
def sendToIpfs(data):
    files = {
        'file': data
    }
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=files, auth=('2NEFcw6jsQRonyXpWguSouymY4o',"588a638882fff36f65b8c0c76aef28ce"))
    a = response.json()
    return a['Hash']

#function to generate the proof 
def getProof(treshold, seedprivate, seedpublic):
    a = getAccountBalance(seed=seedprivate,treshold=treshold)
    if(a):
       
        baseSet = getRing(treshold)
        points = getPoints(seedprivate)
        anonimtySet = [tup for tup in baseSet if tup[1] is not None]
        anonimtySet.append(points[0])
        print(anonimtySet)
        proof = haosring_sign(anonimtySet,points,message=12)
        hash = sendToIpfs(str(proof))
        print(hash)
        data = ('https://gateway.ipfs.io/ipfs/'+str(hash)).encode().hex()
        mintNFT(seedpublic,data=data)
        return True
    return False


     
