### Команда для сборки контейнера:

```commandline
docker build -t guess-melody-api .
```

### Команда сохранения контейнера (для его переноса на другой хост):

```commandline
docker save -o guess-melody-api.tar guess-melody-api
```

### Команда для развертывания контейнера на другом хосте (на сервере):

```commandline
docker load -i guess-melody-api.tar
```

### Команда для запуска compose файла

```commandline
docker compose up
```
или если запускаем конкретный .yaml файл
```commandline
docker compose -f путь_к_файлу.yaml
```