# -*- coding: utf-8 -*-

from slackbot.bot import respond_to, listen_to
import re


@respond_to('안녕', re.IGNORECASE)
def hi(message):
    message.reply('어 그래 안녕')


@respond_to('help')
def help(message):
    msg = "[ 명령어 ]\n" \
          "mining : 채굴 정보\n" \
          "gpu : GPU 상태"
    message.send(msg)


@listen_to('노예야')
def hey_bot(message):
    if message.body['user'] == 'U1AQ7QS1Z':
        message.send("예 주인님")
    else:
        message.reply("넌 뭐냐")
