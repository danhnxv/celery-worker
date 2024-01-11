# Celery

## Create virtual environment
```
cd current directory
virtualenv .venv --python=python3.9
```

## Install packages
```
source .venv/bin/activate
pip install -r requirements.txt
```

## Update requirements file:
```
pip freeze > requirements.txt

```

## Unitest
```
cp .env-example .test.env
pytest -x
```

## Run API
```
uvicorn app.main:app --reload
```