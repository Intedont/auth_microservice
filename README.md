# auth_microservice

# Запуск
> docker-compose up -d

Чтобы выполнить миграции бд при первом запуске:
> docker exec -it <имя контейнера с веб приложением> sh
> 
Далее в консоли:
> cd app
> 
> alembic upgrade head
> 
Вы великолепны!
