"""Platform for light integration."""
from .ventaapi import VentaAPI

# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_RGB_COLOR,
    COLOR_MODE_RGB,
    ATTR_BRIGHTNESS,
    LightEntity,
)
from homeassistant.const import CONF_HOST


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Venta light."""
    host = config[CONF_HOST]
    api = VentaAPI(host)
    light = api.get_light()
    add_entities([VentaLight(light)])


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def hex2rgb(hex):
    h = hex.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rgb_brightness(rgb, brightness):
    (r, g, b) = rgb
    return (
        round((r * (brightness / 255)) / 4),
        round((g * (brightness / 255)) / 4),
        round((b * (brightness / 255)) / 4),
    )


class VentaLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light):
        """Initialize an AwesomeLight."""
        self._attr_color_mode = COLOR_MODE_RGB
        self._attr_supported_color_modes = {COLOR_MODE_RGB}
        self._light = light
        self._name = "Venta"
        self._is_on = light.is_on
        self._brightness = 255
        self._color = hex2rgb(light.color)

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def rgb_color(self):
        return self._color

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._color = kwargs.get(ATTR_RGB_COLOR, self._color)
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness)

        self._light.control(
            True, rgb2hex(rgb_brightness(self._color, self._brightness))
        )

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.control(False, rgb2hex(self._color))

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._is_on = self._light.is_on
        # self._color = hex2rgb(self._light.color)
