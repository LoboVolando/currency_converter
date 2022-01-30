##Запуск ежедневной фоновой задачи:
```redis-sever```

```celery -A four_currencies worker -l info```

```celery -A four_currencies beat -l info```