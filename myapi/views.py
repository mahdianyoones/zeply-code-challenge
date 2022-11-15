from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bitcoinlib.wallets import Wallet, wallet_exists
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.networks import NETWORK_DEFINITIONS

WALLET_NAME = "My Wallet"
DB_URI = "db.sqlite3"
NETWORK_NOT_SUPPORTED = False

def get_network_name(network_code):
    '''Converts BTC to bitcoin, LTC to litecoin, etc.'''
    for network_name, definitions in NETWORK_DEFINITIONS.items():
        if definitions["currency_code"] == network_code:
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
    if not "currency" in request.data:
        return Response("currency is not given")
    network_name = get_network_name(request.data["currency"])
    if network_name == NETWORK_NOT_SUPPORTED:
        return Response(NETWORK_DEFINITIONS)
        return Response(request.data["currency"]+" is not among supported currencies.")
    output = {}
    if wallet_exists(WALLET_NAME, db_uri=DB_URI):
        wallet = Wallet(WALLET_NAME, db_uri=DB_URI)
    else:
        mn = Mnemonic()
        passphrase = mn.generate()
        wallet = Wallet.create(WALLET_NAME, keys=passphrase, db_uri=DB_URI, network=network_name)
        output["passphrase"] = passphrase
        output["message"] = "A new wallet has been created for you."
        output["message"] += " Make a back of the return passphrase,"
        output["message"] += " or else, your future coins will be lost forever!"
    new_key = wallet.new_key(network=network_name)
    generated_address = new_key.address
    output["id"] = new_key.key_id
    output["address"] = generated_address
    return Response(output)

@api_view(['get'])
def list(request):
    """Returns the list of all addresses for the given currency network."""
    if not wallet_exists(WALLET_NAME, db_uri=DB_URI):
        return Response("No wallet exists yet!")
    w = Wallet(WALLET_NAME, db_uri=DB_URI)
    generated_addresses = w.keys(as_dict=True)
    output = {}
    for ga in generated_addresses:
        network_code = get_network_code(ga["network_name"])
        if not network_code in output:
            output[network_code] = []
        output[network_code].append({
            "address": ga["address"],
            "id": ga["id"],
            "balance": ga["balance"]
        })
    output["total"] = len(generated_addresses)
    return Response(output)

@api_view(['post'])
def retrieve(request):
    """Returns address and balance of the given id."""
    if not wallet_exists(WALLET_NAME, db_uri=DB_URI):
        return Response("No wallet exists yet!")
    wallet = Wallet(WALLET_NAME, db_uri=DB_URI)
    if not "id" in request.data:
        return Response("Please specify an address ID.")
    try:
        key = wallet.key(request.data["id"]).as_dict()
    except Exception:
        return Response("Not found")
    output = {
        "address": key["address"],
        "currency": get_network_code(key["network"]),
        "balance": key["balance_str"]
    }
    return Response(output)