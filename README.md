# Blog API

Django REST Framework проект с постами и комментариями.

## Запуск проекта

```bash
cd /Users/nora/blog_api
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

## Документация

- Swagger: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## Пользователи

Регистрация:

```http
POST /api/v1/users/register/
```

Пример:

```json
{
  "username": "student",
  "password": "123456"
}
```

Вход:

```http
POST /api/v1/users/login/
```

Для запросов, где нужна авторизация, вставь token в Headers:

```http
Authorization: Token your_token
```

## Посты

```http
GET /api/v1/posts/
POST /api/v1/posts/
GET /api/v1/posts/{id}/
PUT /api/v1/posts/{id}/
DELETE /api/v1/posts/{id}/
```

Пример создания поста:

```json
{
  "title": "My post",
  "body": "Post text",
  "is_published": true
}
```

Гость видит только опубликованные посты.

## Комментарии

```http
GET /api/v1/posts/{id}/comments/
POST /api/v1/posts/{id}/comments/
GET /api/v1/comments/{id}/
PUT /api/v1/comments/{id}/
DELETE /api/v1/comments/{id}/
```

Пример комментария:

```json
{
  "body": "My comment"
}
```

Менять и удалять посты и комментарии может только их автор.
