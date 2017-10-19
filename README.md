# Как начать пользоваться и разрабатывать

## Зарегистрировать собственного телеграм бота

Для этого в телеграме нужно написать боту \@BotFather и следовать его инструкциям.

В результате вы получите токен, его нужно записать в конфигурационный файл bot.cfg:
```
telegram_bot_token=<полученный токен>
```

## Настроить Yandex.Speechkit для распознавания голоса

Нужно получить ключ, следуя инструкциям, здесь: https://tech.yandex.ru/speechkit/cloud/

Вписать полученный ключ в конфигурационный файл bot.cfg:
```
speechkit_key=<полученный ключ>
```

## Установить необходимые инструменты

- git
- python
- docker

## Скачать код бота
В командной строке:
```sh
git clone https://github.com/subdir/yndx-astana-demo-bot.git
cd yndx-astana-demo-bot
```

## Собрать docker-образ
В командной строке:
```sh
docker build -t yndx-astana-demo-bot .
```

## Запуск бота

### Linux
В командной строке:
```sh
docker run --rm -ti --volume=$PWD:/yndx-astana-demo-bot yndx-astana-demo-bot
```

### Windows
В командной строке:
```sh
docker run --rm -ti --volume=%cd%:/yndx-astana-demo-bot yndx-astana-demo-bot
```
