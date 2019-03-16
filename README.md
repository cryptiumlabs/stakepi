### StakePi

Monitoring staking status with a Raspberry Pi

#### Hardware

Can easily be varied.

- [Raspberry Pi 3 B+](https://www.sparkfun.com/products/14643)
- [Qwiic Hat](https://www.sparkfun.com/products/14459)
- [BME280](https://www.sparkfun.com/products/14348)
- [Qwiic LED Stick](https://www.sparkfun.com/products/14783)
- [Micro OLED](https://www.sparkfun.com/products/14532)

#### Setup

```
pip2 install -r requirements.txt
```

And install [this fork](https://github.com/cwgoes/Adafruit_Python_SSD1306) of the SSD1306 library.

#### Usage

```bash
./monitor.py
```
