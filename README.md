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

After that, run the following commands in your terminal to generate some addresses:

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
