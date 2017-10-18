#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import os
import time
import uuid
import logging
from logging import info
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as etree

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from classify import *
from life import life_gif


telegram_token = "458834549:AAE1t-dLCmIIgv1BJA7f6oef4S9oBKf_lZg"
speechkit_key = "c1716921-c89f-4a01-80c0-70c4deb0d2ba"
speechkit_uuid = uuid.uuid1().hex


def start(bot, update):
    info("start")
    update.message.reply_text('Привет!')


def text(bot, update):
    info("text: " + update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Скажи что-нибудь голосом")


def voice(bot, update):
    info("voice: " + repr(update.message.voice.to_dict()))
    record = bot.get_file(update.message.voice["file_id"])
    with NamedTemporaryFile(prefix="voice-") as tmp:
        record.download(tmp.name)
        info("saved audio file: " + tmp.name)
        text = query_speechkit(tmp.name)
        if text is None:
            bot.send_message(chat_id=update.message.chat_id, text="Непонятно")
        elif text == u"игра жизнь":
            with NamedTemporaryFile(prefix="life-", suffix=".gif") as life:
                bot.send_message(chat_id=update.message.chat_id, text="Секундочку...")
                info("Generating...")
                life_gif(life.name, 20, 20, 10)
                info("Done: {}".format( os.path.getsize(life.name) ))
                bot.send_document(chat_id=update.message.chat_id, document=open(life.name))
                info("Sent")

        elif text == u"мальчик или девочка":
            wav = "{}-test.wav".format(tmp.name)
            save_wav(tmp.name, wav)
            if is_male(wav):
                bot.send_message(chat_id=update.message.chat_id, text="Мальчик.")
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Девочка.")

        elif text in (u"я мальчик", u"я девочка"):
            if text == u"я мальчик":
                save_wav(tmp.name, "male-{}.wav".format(os.path.basename(tmp.name)))
                bot.send_message(chat_id=update.message.chat_id, text="Ок. Ты мальчик.")
                bot.send_message(chat_id=update.message.chat_id, text="Всего голосов мальчиков: {}".format(len(male_voices())))
            if text == u"я девочка":
                save_wav(tmp.name, "female-{}.wav".format(os.path.basename(tmp.name)))
                bot.send_message(chat_id=update.message.chat_id, text="Ок. Ты девочка.")
                bot.send_message(chat_id=update.message.chat_id, text="Всего голосов девочек: {}".format(len(female_voices())))
            refresh_gmm_models()

        else:
            bot.send_message(chat_id=update.message.chat_id, text=text)


def query_speechkit(filename):
    url = "http://asr.yandex.net/asr_xml?uuid={uuid}&key={key}&topic=queries&lang=ru-RU".format(
        uuid = speechkit_uuid,
        key = speechkit_key
    )
    headers = {
        "Content-type": 'audio/ogg;codecs=opus'
    }

    payload = open(filename, 'rb').read()
    resp = requests.post(url, data=payload, headers=headers)
    info("speechkit resp: " + resp.text)
    for elem in etree.fromstring(resp.text.encode('utf8')).iter():
        if elem.tag == "variant":
            return elem.text

    return None


def main():
    logging.basicConfig(level=logging.INFO)

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher
    voice_handler = MessageHandler(Filters.voice, voice)
    text_handler = MessageHandler(Filters.text, text)

    dispatcher.add_handler((CommandHandler('start', start)))
    dispatcher.add_handler(voice_handler)
    dispatcher.add_handler(text_handler)

    updater.start_polling()
    info("Bot started, press CTRL+C to exit...")
    try:
        # WARNING! There is a bug in python-telegram-bot:
        # https://github.com/python-telegram-bot/python-telegram-bot/issues/881
        while True:
            time.sleep(100)
    finally:
        info("Exiting, please wait a few seconds...")
        updater.stop()

