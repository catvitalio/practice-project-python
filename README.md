README
=====================

Этот README документирует описывает все шаги, необходимые для создания и запуска веб-приложения.


### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

##### Команды для запуска docker без sudo (для локалки)

* `sudo groupadd docker`
* `sudo gpasswd -a ${USER} docker`
* `newgrp docker`
* `sudo service docker restart`

##### Проверка работоспособности docker без sudo

* `docker run hello-world`

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

##### Команда для запуска docker-compose без sudo (для локалки)

* `sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`

### Fabric

Файл `fabfile.py` содержит ряд функций, которые помогают при локальной разработке.

##### Установка

* `sudo pip install Fabric3`

##### Команды fabric

* `fab dev` - запустить локально веб приложение
* `fab makemigrations` - создать файл миграций
* `fab migrate` - применить миграции
* `fab createsuperuser` - создать супер пользователя
* `fab shell` - зайти в shell django приложения
* `fab bash` - зайти в bash контейнера server
* `fab kill` - остановить все запущенные контейнеры

### Локальная разработка

##### Команды для первого запуска

* `docker-compose build` - создать контейнеры docker
* `fab dev` - зупустить веб приложение
* `fab migrate` - применить миграции

##### Команды для последующего запуска

* `fab dev` - зупустить веб приложение
* `fab migrate` - применить миграции

**Примечание**: при добавлении каких-либо зависимостей в проект или изменении Dockerfile, необходимо пересобрать контейнер с веб-приложением `docker-compose build server`

##### Доступ

* http://localhost:8000

### Развертывание веб-приложения на сервере (работа с nginx)

##### Команды

* `docker-compose -f docker-compose.prod.yml build` - сборка контейнеров 
* `docker-compose -f docker-compose.prod.yml up` - запуск контейнеров 

##### Доступ

* http://localhost
