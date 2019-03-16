### StakePi

Monitoring staking status with a Raspberry Pi. Also conveniently displays the current temperature.

#### Hardware

Can easily be varied.

- [Raspberry Pi 3 B+](https://www.sparkfun.com/products/14643)
- [Qwiic Hat](https://www.sparkfun.com/products/14459)
- [BME280](https://www.sparkfun.com/products/14348) (optional)
- [Qwiic LED Stick](https://www.sparkfun.com/products/14783) (optional)
- [Qwiic Micro OLED](https://www.sparkfun.com/products/14532)

#### Setup

[Python 2.7](https://www.python.org/) required.

```
pip2 install -r requirements.txt
```

#### Configuration

Update [config.yaml](config.yaml) with your validator information, e.g.:

```yaml
addresses:
  tezos: tz1eEnQhbwf6trb8Q8mPb2RaPkNk2rN7BKi8
  irisnet: iva1f3lapzxe7ugfex8358ufp5k8xg2yym5tpp2xje
  cosmos: cosmosvaloper1kj0h4kn4z5xvedu2nd9c4a9a559wvpuvu0h6qn
display:
  period: 2
```

#### Usage

```bash
./monitor.py
```

The I2C connections are occasionally finicky.

If you plan to run this headlessly a systemd service is recommended. See [stakepi.service](stakepi.service) for an example.
