# Как запустить бота

## Зарегистрировать собственного телеграм бота

Для этого в телеграме нужно написать боту \@BotFather и следовать его инструкциям.

В результате вы получите токен, его нужно записать в конфигурационный файл bot.cfg:
```
telegram_bot_token=<полученный токен>
```

## Настроить Yandex.SpeechKit для распознавания голоса

Нужно получить ключ, следуя инструкциям, здесь: https://tech.yandex.ru/speechkit/cloud/

Вписать полученный ключ в конфигурационный файл bot.cfg:
```
speechkit_key=<полученный ключ>
```

## Установить необходимые инструменты

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [docker](https://docs.docker.com/engine/installation/)

## Скачать код бота
В командной строке:
```sh
git clone https://github.com/subdir/yndx-astana-demo-bot.git
cd yndx-astana-demo-bot
```

## Собрать docker-образ
В командной строке, находясь в папке с исходниками (yndx-astana-demo-bot):
```sh
docker build -t yndx-astana-demo-bot .
```

## Запуск бота

### Linux
В командной строке, находясь в папке с исходниками (yndx-astana-demo-bot):
```sh
docker run --rm -ti --volume=$PWD:/yndx-astana-demo-bot yndx-astana-demo-bot
```

### Windows
В командной строке, находясь в папке с исходниками (yndx-astana-demo-bot):
```sh
docker run --rm -ti --volume=%cd%:/yndx-astana-demo-bot yndx-astana-demo-bot
```
