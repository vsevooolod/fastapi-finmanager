from fastapi import FastAPI

from .api import router


openapi_tags = [
    {
        'name': 'Auth',
        'description': 'Авторизация и регистрация пользователей',
    },
    {
        'name': 'Operations',
        'description': 'Работа с финансовыми операциями пользователя',
    },
    {
        'name': 'Reports',
        'description': 'Загрузка и выгрузка отчетов пользователя в CSV формате',
    }
]

app = FastAPI(
    title='FinManager',
    description='Store your money history by using FinManager',
    version='1.0.0',
    openapi_tags=openapi_tags,
)
app.include_router(router)
