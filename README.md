# Weather Forecast

Консольное приложение для просмотра текущей погоды в любой точке мира, с возможностью восстановления истории запросов. Формат вывода ответа на запрос о погоде:
```
* Local time:   10-12-2023 02:52:27 UTC+12:00
* City:         Anadyr, RU
* Weather:      Clear (clear sky)
* Temperature: -25°C
* Feels like   -32°C
* Wind speed:   6 m/sec
```
Для локального запуска необходимо:

1. Установить интепретатор python версии 3.11 или выше
2. Склонировать репозиторий с решением,
3. Убедиться, что все необходимые пакеты установлены (для этого нужно создать виртуальное окружение с помощью команды python -m venv venv, установить туда все необходимые для работы программы библиотеки командой  pip install -r requirements.txt)
4. Перейти в директорию с проектом,
5. Выполнить команду `chmod +x ./weather.py`.

После этого приложение готово к использованию. Команды можно исполнять после запуска скрипта `./weather.py`. Для получения краткой справки можно воспользоваться командой
```
help
```


# План выполнения

1. Данные о погоде будем получать с сайта [openweathermap](https://openweathermap.org/current). API данного сайтв предусматривает передачу координат города в качестве параметров запроса. Поэтому название города будем отображать в координаты при помощи предложенного на том же сайте [geocoding API](https://openweathermap.org/api/geocoding-api).

2. Для получения текущего местоположения будем пользоваться пакетом [geocoder](https://geocoder.readthedocs.io/), который предоставляет название города и координаты исходя из текущего ip адреса устройства.

3. История запросов будет храниться в простой "базе данных" --- в csv файле, содержащем текст запроса, его время и результат.

4. Само приложение будет представлять из себя исполняемый скрипт (weather.py), в бесконечном цикле принимающий в качестве ввода название команды и её аргументы, пока не получит на вход команду `exit`. Поддерживаемые команды: `get`, `history`, `help`, `exit`.
