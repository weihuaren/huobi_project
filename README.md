# Huobi Project

Requires Python 3.7.0 +

Run locally
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Build and Push Container Image

For example:
```
docker build --tag huobi-swap-valid-until-01-06-2021 .

docker tag huobi-swap-valid-until-01-06-2021:latest gcr.io/huobi-project/huobi-swap-valid-until-01-06-2021:v1.0.0

docker push gcr.io/huobi-project/huobi-swap-valid-until-01-06-2021:v1.0.0
```