# Как начать пользоваться и разрабатывать

## Зарегистрировать собственного телеграм бота

Для этого в телеграме нужно написать боту \@BotFather и следовать его инструкциям.

В результате вы получите токен, его нужно записать в конфигурационный файл bot.cfg:
```
telegram_bot_token=<полученый токен>
```

## Настроить Yandex.Speechkit для распознавания голоса

Нужно получить ключ, следуя инструкциям, здесь: https://tech.yandex.ru/speechkit/cloud/

Вписать полученный ключ в конфигурационный файл bot.cfg:
```
speechkit_key=<полученый ключ>
```

## Установить необходимые инструменты

- git
- python
- docker

## Скачать код бота

```sh
git clone https://github.com/subdir/yndx-astana-demo-bot.git
cd yndx-astana-demo-bot
```

## Собрать docker-образ

```sh
docker build -t yndx-astana-demo-bot .
```

## Запуск бота

```sh
docker run --rm -ti --volume=$PWD:/yndx-astana-demo-bot yndx-astana-demo-bot
```
