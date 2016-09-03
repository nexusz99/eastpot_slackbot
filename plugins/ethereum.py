# -*- coding: utf-8 -*-

from slackbot.bot import respond_to, listen_to
import re
import json
import requests
from subprocess import check_output

from bs4 import BeautifulSoup as Soup


@respond_to('mining', re.IGNORECASE)
def mining_status(message):
    url = 'http://ethermine.org/api/miner_new/71694c8f184b2133dd080c3dcb8e726e00194687'
    r = requests.get(url=url)
    data = r.json()
    ch = message.channel

    if 'name' in ch._body and ch._body['name'] != 'ethereum':
        message.send('이 명령어는 #ethereum 채널에서만 가능합니다.')
        return

    msg = '--------- 채굴 현황 --------\n'
    msg += '현재 HashRate    : %s\n' % data['hashRate']
    msg += '평균 HashRate    : %.1f MH/s\n' % (data['avgHashrate'] / 1000000)
    msg += '분당 채굴량       : %.8f ETH\n' % data['ethPerMin']
    msg += '채굴된 이더       : %.8f ETH' % (data['unpaid'] / 1000000000000000000)
    message.send(msg)


@respond_to('gpu')
def gpu_temperature(message):
    out = check_output(['sudo', 'aticonfig', '--odgc', '--odgt'])
    message.send(out)


@respond_to('korbit')
def korbit_status(message):
    response = requests.get('https://www.korbit.co.kr/eth_market')

    soup = Soup(response.text, 'lxml')
    order = soup.select_one('div[data-react-class=MarketDataBlock]')
    props_str = order['data-react-props']
    props = json.loads(props_str)
    current_price_str = props['market_data']['last_price']
    current_price = int(current_price_str)

    message.send('KORBIT 이더리움 현재가 : %d원' % current_price)


@respond_to('coinone')
def coinone_status(message):
    response = requests.get('https://api.coinone.co.kr/ticker/?type=ETH')
    data = response.json()
    response.close()
    message.send('COINONE 이더리움 현재가 : %s원' % data['last'])


@listen_to('브리핑')
def eth_breifing(message):
    mining_status(message)
    message.send('------------')
    gpu_temperature(message)
    message.send('------------')
    korbit_status(message)
    message.send('------------')
    coinone_status(message)
    message.send('------------')
    dao_price(message)
    message.send('------------')
    ether_dollar_price(message)


@respond_to('브리핑')
def eth_breifing(message):
    mining_status(message)
    message.send('------------')
    gpu_temperature(message)
    message.send('------------')
    korbit_status(message)
    message.send('------------')
    coinone_status(message)
    message.send('------------')
    dao_price(message)
    message.send('------------')
    ether_dollar_price(message)


@respond_to('시장가')
def respond_market_price(message):
    korbit_status(message)
    message.send('------------')
    coinone_status(message)
    message.send('------------')
    dao_price(message)
    message.send('------------')
    ether_dollar_price(message)


@listen_to('시장가')
def listen_market_price(message):
    korbit_status(message)
    message.send('------------')
    coinone_status(message)
    message.send('------------')
    dao_price(message)
    message.send('------------')
    ether_dollar_price(message)


def dao_price(message):
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/the-dao')
    data = response.json()
    price = data[0]['price_usd']
    message.send('DAO 현재 가격 : $ %f' % float(price))


def ether_dollar_price(message):
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
    data = response.json()
    price = data[0]['price_usd']
    message.send('해외 이더리움 가격 : $ %f' % float(price))
