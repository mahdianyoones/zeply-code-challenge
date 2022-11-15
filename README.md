# Zeply Python Code Challenge

Run the following commands to install and run the project on your laptop:

```
sudo apt install -y libpq-dev libgmp-dev curl

git clone https://github.com/mahdianyoones/zeply-code-challenge.git

cd zeply-code-challenge

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

python3 manage.py runserver
```

*The APIs in this project, are indeed wrappers to the cryptocurrency library **bitcoinlib**. This library implements a full HD vallet with optional automatic saving into a database of your choise. The database engine of choice in this project is sqlite3 which is passed as a parameter to the library functions and classes; the rest is handled gracefully by it. However, we can extend the functionality of this library by dealing with the database, making it a multi-user online wallet for instance. Furthermore, we may only work with individual classes of this library, such as mnemonic and key, and do the rest in our own way.*

To add support for other coins, networks.json under `env/lib/python3.9/site-packages/bitcoinlib/config` must be edited to contain the following entry:

```
  "ethereum":
  {
    "description": "Ethereum",
    "currency_name": "ether",
    "currency_name_plural": "ethers",
    "currency_symbol": "Ξ",
    "currency_code": "ETH",
    "prefix_address": "00",
    "prefix_address_p2sh": "05",
    "prefix_bech32": "bc",
    "prefix_wif": "80",
    "prefixes_wif": [
      ["0488B21E", "xpub", "public",  false, "legacy",      "p2pkh"],
      ["0488B21E", "xpub", "public",  true,  "legacy",      "p2sh"],
      ["0488ADE4", "xprv", "private", false, "legacy",      "p2pkh"],
      ["0488ADE4", "xprv", "private", true,  "legacy",      "p2sh"],
      ["049D7CB2", "ypub", "public",  false, "p2sh-segwit", "p2sh_p2wpkh"],
      ["0295B43F", "Ypub", "public",  true,  "p2sh-segwit", "p2sh_p2wsh"],
      ["049D7878", "yprv", "private", false, "p2sh-segwit", "p2sh_p2wpkh"],
      ["0295B005", "Yprv", "private", true,  "p2sh-segwit", "p2sh_p2wsh"],
      ["04B24746", "zpub", "public",  false, "segwit",      "p2wpkh"],
      ["02AA7ED3", "Zpub", "public",  true,  "segwit",      "p2wsh"],
      ["04B2430C", "zprv", "private", false, "segwit",      "p2wpkh"],
      ["02AA7A99", "Zprv", "private", true,  "segwit",      "p2wsh"]
    ],
    "bip44_cointype": 60,
    "denominator": 0.00000001,
    "dust_amount": 1000,
    "fee_default": null,
    "fee_min": 1000,
    "fee_max": 1000000,
    "priority": 17
  }
```

This is a dirty hack though! The library does not provide any meaninful way to support other coins through its interfaces. A better solution is to either switch to another library or upgrade the library and contribute to its development.

Run the following commands in your terminal to generate some addresses:

**Note: The first call to /generate endpoint, generates a fresh random passphrase which is the master key to be backed up. If the database gets corrupted or lost, addresses and transactions can be fully recovered only by having this passphrase.**

Bitcoin:

```
curl -X POST -H "Content-Type: application/json" \
    -d '{"currency": "BTC"}' \
    http://127.0.0.1:8000/generate | python3 -m json.tool
```

Litecoin:

```
curl -X POST -H "Content-Type: application/json" \
    -d '{"currency": "LTC"}' \
    http://127.0.0.1:8000/generate | python3 -m json.tool
```

Dash:

```
curl -X POST -H "Content-Type: application/json" \
    -d '{"currency": "DASH"}' \
    http://127.0.0.1:8000/generate | python3 -m json.tool
```

which will give you an output like this:

```
{
    "id": 20,
    "address": "1QEA7HVxjzXWej7XYT1zyYZ8wfaHkTCrJq"
}
```

Then, to view the list of all generated addresses, issue:

```
curl -X GET http://127.0.0.1:8000/list | python3 -m json.tool
```

which will give you an output like this:

```
{
    "BTC": [
        {
            "address": "1BWVhGETw3hW7rmCgbpsUtEbnd6P3UHDr",
            "id": 1,
            "balance": 0
        },
        {
            "address": "12wqb9wnuZVycjhYMZin8oHNKhHwCr82sN",
            "id": 2,
            "balance": 0
        },
    ],
    "LTC": [
        {
            "address": "LRLsnBaP1AeQkffzLL5XhT6whqeZJHeag2",
            "id": 9,
            "balance": 0
        },
    ],
    "DASH": [
        {
            "address": "Xggae45vHj2NaZoh24J94uL13txCfyshGq",
            "id": 14,
            "balance": 0
        },
    ],
    "total": 4
}
```

To retrieve an address by id, replace `replace_me_with_an_id` with an id and issue:

```
curl -X POST -H "Content-Type: application/json" \
    -d '{"id": replace_me_with_an_id}' \
    http://127.0.0.1:8000/retrieve | python2 -m json.tool
```
