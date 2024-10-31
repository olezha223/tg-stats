# Backend

Перед началом работы установите и активируйте виртуальное окружение

```shell
python3 -m venv venv
```
Если у вас Linux или MacOS:
```shell 
source venv/bin/activate
```

Если у вас Windows:
```shell
venv\Scripts\activate
```
```shell
pip install -r requirements.txt
```

Для запуск Swagger:
```shell
uvicorn main:main --reload
```

Для работы с MongoDB можете ее поднять в контейнере или скачать десктоп версию