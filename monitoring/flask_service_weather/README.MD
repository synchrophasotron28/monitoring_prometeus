# Техническое задание:

### 1)    Написать конфигурацию для L7 балансировщика (любого) для сервиса погоды
### 2)    Развернуть сервис на 2-х виртуальных машинах в любом облаке
### 3)   На отдельной виртуальной машине поднять балансировщик и настроить его на проксирование на сервис погоды (на поднятые выше виртуальные машины)

## Шаги, установки:

> выполнить команду для создания образа:
> 
>> docker build -t ubuntu/archhightload_laba5_1 -f dockerfile1 .
> 
> выполнить команду для сборки образа:
> 
>> docker build -t ubuntu/archhightload_laba5_2 -f dockerfile2 .
> 
> команда для создания докер контейнера из образа:
> 
>> docker run -it --name laba5_1_archHL -p 0.0.0.0:5020:8000 ubuntu/archhightload_laba5_1
> 
> команда для создания докер контейнера из образа:
> 
>> docker run -it --name laba5_2_archHL -p 0.0.0.0:5030:8000 ubuntu/archhightload_laba5_2
> 
> необходимо установить Nginx 
> 
>> [как установить nginx](https://losst.pro/ustanovka-nginx-ubuntu-16-04)   sudo apt install nginx
>
>> в файле nginx.txt указана конфигуркция которую вам нужно прописать в /etc/nginx/nginx.config
> 
> Потом выполнить команду перезапуска Nginx'а: 
> 
>> nginx -s reload

## Запуск:
> Перейти в postman и выполнить запросы:
>
>> http://127.0.0.1:60/forecast_weather?city=Moscow&dt=2023-04-10_18:00
>
>> http://127.0.0.1:60/current_weather?city=Minsk

### Если возникнут проблемы, связанные с ошибкой:
>You have to remove (or rename) that container to be able to reuse that name :
> выполнить команды:
> 
> docker start [id] для запуска контейнеров
>> docker start 49c8648f8c92