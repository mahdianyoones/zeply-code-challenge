# Zeply Python Code Challenge

Run the following commands to install and run the project on your laptop:

```
sudo apt install -y libpq-dev libgmp-dev

git clone https://github.com/mahdianyoones/zeply-code-challenge.git

cd zeply-code-challenge

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

python3 manage.py migrate

python3 manage.py runserver
```