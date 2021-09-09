from __future__ import annotations

from .ventaapi import VentaAPI

from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.humidifier.const import (
    DEVICE_CLASS_HUMIDIFIER,
)
from homeassistant.const import CONF_HOST


SUPPORT_FLAGS = 1
MODE_MANUAL = "manual"
MODE_SLEEP = "sleep"
MODE_AUTO = "automatic"
MODE_0 = "0"
MODE_1 = "1"
MODE_2 = "2"
MODE_3 = "3"
MODE_4 = "4"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Venta humidifier."""
    host = config[CONF_HOST]
    api = VentaAPI(host)

    humidifier = api.get_humidifier()
    add_entities([VentaHumidifier(humidifier)])


def find_mode(is_sleep_mode, is_auto_mode, fan_speed):
    if is_sleep_mode:
        return MODE_SLEEP
    elif is_auto_mode:
        return MODE_AUTO
    elif fan_speed == 0:
        return MODE_0
    elif fan_speed == 1:
        return MODE_1
    elif fan_speed == 2:
        return MODE_2
    elif fan_speed == 3:
        return MODE_3
    elif fan_speed == 4:
        return MODE_4


class VentaHumidifier(HumidifierEntity):
    """Representation of a demo humidifier device."""

    def __init__(self, humidifier) -> None:
        """Initialize the humidifier device."""
        self._humidifier = humidifier
        self._attr_name = "Venta"
        self._attr_is_on = humidifier.is_on
        self._attr_supported_features = SUPPORT_FLAGS
        self._attr_target_humidity = humidifier.target_humidity
        self._attr_max_humidity = 70
        self._attr_min_humidity = 30
        self._attr_mode = find_mode(
            humidifier.is_sleep_mode, humidifier.is_auto_mode, humidifier.fan_speed
        )
        self._attr_available_modes = [
            MODE_AUTO,
            MODE_SLEEP,
            MODE_0,
            MODE_1,
            MODE_2,
            MODE_3,
            MODE_4,
        ]
        self._attr_device_class = DEVICE_CLASS_HUMIDIFIER

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._attr_is_on = True
        self._humidifier.change_mode("on")

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._attr_is_on = False
        self._humidifier.change_mode("off")

    def set_humidity(self, humidity):
        """Set new humidity level."""
        self._attr_target_humidity = humidity
        self._humidifier.set_humidity(humidity)

    def set_mode(self, mode):
        """Update mode."""
        self._attr_mode = mode
        if self._attr_mode == MODE_SLEEP:
            self._humidifier.change_mode("sleep")
        elif self._attr_mode == MODE_AUTO:
            self._humidifier.change_mode("automatic")
        elif self._attr_mode == MODE_0:
            self._humidifier.change_mode("manual", 0)
        elif self._attr_mode == MODE_1:
            self._humidifier.change_mode("manual", 1)
        elif self._attr_mode == MODE_2:
            self._humidifier.change_mode("manual", 2)
        elif self._attr_mode == MODE_3:
            self._humidifier.change_mode("manual", 3)
        elif self._attr_mode == MODE_4:
            self._humidifier.change_mode("manual", 4)

    def update(self):
        """Fetch new state data for this humidifier."""
        self._humidifier.update()
        self._attr_is_on = self._humidifier.is_on
        self._attr_target_humidity = self._humidifier.target_humidity
        self._attr_mode = find_mode(
            self._humidifier.is_sleep_mode,
            self._humidifier.is_auto_mode,
            self._humidifier.fan_speed,
        )
