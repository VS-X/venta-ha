"""Demo platform that has a couple of fake sensors."""
from __future__ import annotations

from typing import Any
from .ventaapi import VentaAPI

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity
from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    PERCENTAGE,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import CONF_HOST


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: dict[str, Any] | None = None,
) -> None:
    """Set up the Venta sensors."""
    host = config[CONF_HOST]
    api = VentaAPI(host)
    humidifier = api.get_humidifier()
    add_entities(
        [
            TemperatureSensor(humidifier),
            HumiditySensor(humidifier),
        ]
    )


class TemperatureSensor(SensorEntity):
    """Representation of a Demo sensor."""

    def __init__(self, humidifier) -> None:
        """Initialize the sensor."""
        self._humidifier = humidifier
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_name = "Temperature"
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_native_value = humidifier.temperature
        self._attr_state_class = STATE_CLASS_MEASUREMENT
        self._attr_unique_id = "venta_temperature"

        self._attr_device_info = {
            "identifiers": {("Venta", "venta_temperature")},
            "name": "Temperature",
        }

    def update(self):
        """Fetch new state data for this sensor."""
        self._humidifier.update()
        self._attr_native_value = self._humidifier.temperature


class HumiditySensor(SensorEntity):
    """Representation of a Demo sensor."""

    def __init__(self, humidifier) -> None:
        """Initialize the sensor."""
        self._humidifier = humidifier
        self._attr_device_class = DEVICE_CLASS_HUMIDITY
        self._attr_name = "Humidity"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_native_value = humidifier.humidity
        self._attr_state_class = STATE_CLASS_MEASUREMENT
        self._attr_unique_id = "venta_humidity"

        self._attr_device_info = {
            "identifiers": {("Venta", "venta_humidity")},
            "name": "Humidity",
        }

    def update(self):
        """Fetch new state data for this sensor."""
        self._humidifier.update()
        self._attr_native_value = self._humidifier.humidity
