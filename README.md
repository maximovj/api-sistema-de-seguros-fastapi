# CRUD API + FastAPI

Este es un sistema (API) de seguros con FastAPI y SQLite3 usando SQLAlchemy

## Estructura del proyecto

```shell
sistema-seguros/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── customers.py
│   │   ├── policies.py
│   │   ├── assets.py
│   │   └── payments.py
│   └── config.py
├── requirements.txt
├── .env
└── .gitignore
```


## Comandos 

Instalar todas las dependencias

```shell
$ .env/Scripts/active.bat # (En Windows)
$ pip install -r requirements.txt
```

Iniciar servidor

```shell
$ uvicorn app.main:app --reload
```

Crear datos de pruebas en SQLite

```shell
$ python init_db.py
```

## Vista Previa

![preview_01.png](/screenshots/preview_01.png)

![preview_02.png](/screenshots/preview_02.png)

![preview_03.png](/screenshots/preview_03.png)

![preview_04.png](/screenshots/preview_04.png)