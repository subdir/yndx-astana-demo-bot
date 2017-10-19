# Как начать пользоваться и разрабатывать

## Зарегистрировать нового телеграм бота

Для этого в телеграме нужно написать боту \@BotFather и следовать его инструкциям.
В результате вы получите токен, его нужно записать в конфигурационный файл bot.cfg
```
telegram_bot_token=<полученый токен>
```

## Настроить Yandex.Speechkit для распознавания голоса

Нужно получить ключ, следуя инструкциям, здесь: https://tech.yandex.ru/speechkit/cloud/
Вписать полученный ключ в конфигурационный файл bot.cfg
```
speechkit_key=<полученый ключ>
```

## Скачать код бота и установить зависимости:

### Linux:
```sh
apt-get install python python-pip git
git clone https://github.com/subdir/yndx-astana-demo-bot.git
cd yndx-astana-demo-bot
apt-get install libfreetype6-dev pkg-config
pip install -r requirements.txt
```

### Windows:
А вот не знаю.

## Запуск
```sh
python bot.py
```
