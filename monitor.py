#!/usr/bin/env python2.7

import math
import requests
import yaml
import util
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

config = yaml.load(open('config.yaml'))

disp = Adafruit_SSD1306.SSD1306_64_48(rst = None, i2c_address = 0x3d)
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

font = ImageFont.load_default()

def autoformat(value):
    if value > 1e6:
        return str(round(value / 1e6, 2)) + 'm'
    if value > 1e3:
        return str(round(value / 1e3, 2)) + 'k'
    return round(value, 2)

def fetch_temperature():
    return util.readBME280All()[0]

def fetch_cmc_price(ticker):
    return float(requests.get('https://api.coinmarketcap.com/v1/ticker/' + ticker + '/').json()[0]['price_usd'])

def get_tezos_stake():
    staking_balance = requests.get('https://api1.tzscan.io/v3/staking_balance/{}'.format(config['addresses']['tezos'])).json()[0]
    return float(staking_balance) / 1e6

def get_irisnet_stake():
    staking_balance = requests.get('https://www.irisplorer.io/api/account/{}'.format(config['addresses']['irisnet'])).json()['deposits']['amount'] / 1e18
    return staking_balance

def get_cosmos_stake():
    staking_balance = float(requests.get('https://sgapi.certus.one/validator/{}'.format(config['addresses']['cosmos'])).json()['app_data']['tokens']) / 1e6
    return staking_balance

def display(text):
    draw.rectangle((0, 0, width, height), outline = 0, fill = 0)
    draw.text((8, -2), str(text), font = font, fill = 255)
    disp.image(image)
    disp.display()

def update_loop():
    stakes = [
        ('tezos', get_tezos_stake()),
        ('irisnet', get_irisnet_stake()),
        ('cosmos', get_cosmos_stake())
    ]
    prices = {
        'tezos': fetch_cmc_price('tezos'),
        'irisnet': 0,
        'cosmos': fetch_cmc_price('cosmos')
    }
    total_staked = sum(x[1] * prices[x[0]] for x in stakes)
    return (stakes, prices, total_staked)

print(update_loop())
print('Temp: {}'.format(fetch_temperature()))
display('testing')
