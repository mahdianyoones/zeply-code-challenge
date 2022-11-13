from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bitcoinlib.wallets import Wallet, wallets_exists
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.networks import NETWORK_DEFINITIONS

WALLET_NAME = "My Wallet"
DB_URI = "db.sqlite3"
NETWORK_NOT_SUPPORTED = False

def get_network_name(network_code):
    '''Converts BTC to bitcoin, LTC to litecoin, etc.'''
    for network_name, definitions in NETWORK_DEFINITIONS.items():
        if definitions["network_code"] == network_code:
            return network_name
    return NETWORK_NOT_SUPPORTED

def get_network_code(network_name):
    '''Converts bitcoin to BTC, litecoin to LTC, etc.'''
    if not network_name in NETWORK_DEFINITIONS:
        return NETWORK_NOT_SUPPORTED
    return NETWORK_DEFINITIONS[network_name]["currency_code"]

@api_view(['post'])
def generate(request):
    """Generates an output address for the given currency network.
    
    If no wallet exists yet, a new one is created using a random generated
    seed."""
    network_name = get_network_name(request.currency)
    if network_name == NETWORK_NOT_SUPPORTED:
        return Response(request.currency+" is not among supported currencies.")
    output = {}
    if wallets_exists("My wallet"):
        w = Wallet(WALLET_NAME, db_uri=DB_URI)
    else:
        mn = Mnemonic()
        passphrase = mn.generate()
        w = Wallet.create(WALLET_NAME, keys=passphrase, db_uri=DB_URI)
        output["passphrase"] = passphrase
        output["message"] = "A new wallet has been created for you."
        output["message"] += " Make a back of the return passphrase,"
        output["message"] += " or else, your future coins will be lost forever!"
    new_key = w.new_key(network=network_name)
    generated_address = new_key.address
    output["address"] = generated_address
    return Response(output)

@api_view(['get'])
def list(request):
    """Returns the list of all addresses for the given currency network."""
    if not wallets_exists(WALLET_NAME, db_uri=DB_URI):
        return Response("No wallet exists yet!")
    w = Wallet(WALLET_NAME, db_uri=DB_URI)
    generated_addresses = w.keys_networks()
    output = {}
    for ga in generated_addresses:
        network_code = get_network_code(ga.network_name)
        output[network_code] = {
            "address": ga.address,
            "id": ga.id
        }
    return Response(output)

@api_view(['get'])
def retrieve(request):
    if not wallets_exists(WALLET_NAME):
        return Response("No wallet exists yet!")
    w = Wallet(WALLET_NAME, db_uri=DB_URI)
    try:
        key = w.key(request.id)
    except Exception:
        return Response("Not found")
    # Preventing retrieval of provate keys!
    if key.is_private:
        return Response("Not found")
    return Response(key.address)