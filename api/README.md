## Backend - Flask app

### Setup

**Requeriments**

- [virtualenv](https://virtualenv.pypa.io/en/latest/)

**Create virtual env**

`virtualenv .venv --python=python3.8`

**Activate virtual env**

`source .venv/bin/activate`

**Install dependencies**

`pip install -r requirements.txt`

---

### Start to develop

**Add the next variables on .venv/bin/activate**
```
export FLASK_APP="api.entrypoint:app"
export FLASK_ENV="development"
export APP_SETTINGS_MODULE="api.config.default"
```

**Activate virtual env**

`source .venv/bin/activate`

**Deactivate virtual env**

`deactivate`
