# Settings backend

# Deploy

## dev

```sh
$ docker-compose -f docker-compose.dev.yml up -d --build
```

## prod
```sh
$ docker-compose up -d --build
```
## Enter to container
```sh
$ docker exec -it <id container or name> bash
$ docker exec -it <id container or name> <command>
```
## Database dump/load
```sh
$ python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.Permission --indent 4 > default_data.json

$ python manage.py loaddata default_data.json
```

# TODO
1. Определиться с архитектурой:
1.1 распределенные микросервисы под каждую платформу с отдельными реализациями диалогов и обработкой сообщений, общий REST API; 
1.2 делаем REST API(хранение данных), общий брокер сообщений (отдельным микросервисом) - прием сообщей от все платформ(отдельными микросервисами), обработка, выдача ответом единым стандартом, 
Отдельные микросервисы под платформы для получение апдейтов и передачи в брокер
1.3 делать монолитом на django apps прием сообщений ответы через urlpatterns, бизнеслогику внутри оставить.

2. Переписать utils - геенерация свободных дат для записи в календарь
3. создать в бд модель - временнный instance записи(хранение полученных данных с диалогов) для последующего рандомного выбора вопроса по недостающей информации для полной записи в календарь
4. написать тесты для апи (чтоб без запуска сервера и ручных проверки :-( )
5. CI/CD (переехать на Gitlab, автоматическое деплой - развертывание, версионирование контейнеров)
6. Настройка Celery: брокер задач - рассылка email, хранение очереди сообщений(для нагруженных ботов)
7. настройка ssl сертификатов и обратного прокси с nginx (в репозитории фронтенда)
8. Мониторинг Celery, API - Flower, Prometheus ....
9. Обработка ошибок и исключений в коде - логгирование, оповещение
10. 
