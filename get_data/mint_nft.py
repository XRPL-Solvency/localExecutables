# This script is use to mint nft 

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.models.requests import AccountNFTs
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Memo

# Mint an NFT on the XRPL via a NFTokenMint transaction
# https://xrpl.org/nftokenmint.html#nftokenmint


# Connect to a testnet node
print("Connecting to Testnet...")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)


# Function to mint an nft, take in argument a seed and some data (uri)
def mintNFT(seed, data):
    issuer_wallet = Wallet(seed=seed, sequence=0)
    issuerAddr = issuer_wallet.classic_address
    issuerpk = issuer_wallet.private_key
    print(issuerpk)

    print(f"\nIssuer Account: {issuerAddr}")
    print(f"          Seed: {issuer_wallet.seed}")

    # Construct NFTokenMint transaction to mint 1 NFT
    print(f"Minting a NFT...")
    mint_tx = NFTokenMint (
        account=issuerAddr,
        nftoken_taxon=1,
        flags=NFTokenMintFlag.TF_BURNABLE,
        uri=data
    )

    # Sign mint_tx using the issuer account
    mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet, client=client)
    mint_tx_signed = send_reliable_submission(transaction=mint_tx_signed, client=client)
    mint_tx_result = mint_tx_signed.result

    print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
    print(f"     Tx response: {mint_tx_result}")

    for node in mint_tx_result['meta']['AffectedNodes']:
        if "CreatedNode" in list(node.keys())[0]:
            print(f"\n - NFT metadata:"
                f"\n        NFT ID: {node['CreatedNode']['NewFields']['NFTokens'][0]['NFToken']['NFTokenID']}"
                f"\n  Raw metadata: {node}")

    # Query the minted account for its NFTs
    get_account_nfts = client.request(
        AccountNFTs(account=issuerAddr)
    )

    nft_int = 1
    print(f"\n - NFTs owned by {issuerAddr}:")
    for nft in get_account_nfts.result['account_nfts']:
        print(f"\n{nft_int}. NFToken metadata:"
            f"\n    Issuer: {nft['Issuer']}"
            f"\n    NFT ID: {nft['NFTokenID']}"
            f"\n NFT Taxon: {nft['NFTokenTaxon']}")
        nft_int += 1


