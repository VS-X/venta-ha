# Venta Home Assistant integration

Supports Venta LW73/74 with Wifi modules. Potentially supports other models

Exposes following entities:

- Humidifier
- Light
- Temperature and Humidity sensors

## Installation

- Clone the repo into `config/custom_components`
- Enable in the `configuration.yaml`:

```yaml
light:
  - platform: venta
    host: http://192.168.0.123 # Humidifier's IP

humidifier:
  - platform: venta
    host: http://192.168.0.123

sensor:
  - platform: venta
    host: http://192.168.0.123
```
