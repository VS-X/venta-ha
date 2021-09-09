import requests
from .light import Light
from .humidifier import Humidifier


class VentaAPI:
    """
    Venta fucked up the "api":
    1) Everything is a post
    2) Control responses contain the old data
    3) Have to request an update after a delay to fix #2
    4) RGB colors are clamped to 64:
        #ffffff = (21,21,21)
        #ff0000 = (64,0,0)
        #ffff00 = (32,32,0)
    """

    def __init__(self, host: str):
        self.host = host

    def get_light(self) -> Light:
        """Get light instance"""
        light = Light(self.request)
        return light

    def get_humidifier(self) -> Humidifier:
        """Get humidifier instance"""
        humidifier = Humidifier(self.request)
        return humidifier

    def request(self, **kwargs) -> requests.Response:
        return requests.request(
            "POST",
            f"{self.host}/datastructure",
            **kwargs,
        )
