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
        return str(round(value / 1e6, 3)) + 'm'
    if value > 1e3:
        return str(round(value / 1e3, 3)) + 'k'
    return round(value, 3)

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

def display(lines):
    print('Displaying {}'.format(lines))
    draw.rectangle((0, 0, width, height), outline = 0, fill = 0)
    x = 2
    for line in lines:
        draw.text((40, x), str(line), font = font, fill = 255)
        x += 8
    disp.image(image)
    disp.display()

def update_loop():
    stakes = [
        ('XTZ', get_tezos_stake()),
        ('IRIS', get_irisnet_stake()),
        ('ATOM', get_cosmos_stake())
    ]
    prices = {
        'XTZ': fetch_cmc_price('tezos'),
        'IRIS': 0,
        'ATOM': fetch_cmc_price('cosmos')
    }
    total_staked = sum(x[1] * prices[x[0]] for x in stakes)
    return (stakes, prices, total_staked)

while 1:
    (stakes, prices, total_staked) = update_loop()
    for stake in stakes:
        lines = [
            '{}'.format(autoformat(stake[1])),
            '{}'.format(stake[0]),
            'STAKED'
        ]
        display(lines)    
        time.sleep(2.0)
    lines = [
        '${}'.format(autoformat(total_staked)),
        'TOTAL',
        'STAKED'
    ]
    display(lines)
    time.sleep(2.0)
