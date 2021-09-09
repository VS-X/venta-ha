import time


class Light:
    """Class that represents a light object in the Venta API."""

    def __init__(self, request):
        """Initialize a light object."""
        self.state = {}
        self.request = request

        self.update()

    @property
    def is_on(self) -> bool:
        """Return if the light is on."""
        return self.state["Action"]["LEDStripActive"]

    @property
    def color(self) -> str:
        """Return color of the light."""
        return self.state["Action"]["LEDStrip"]

    def control(self, status: bool, color: str):
        """Control the light."""
        """The response contains the old data, not the updated data.
        Uses update (with some delay) to get the updated data"""
        self.request(json={"Action": {"LEDStripActive": status, "LEDStrip": color}})
        time.sleep(0.3)
        self.update()

    def update(self):
        """Fetch the light data."""
        res = self.request()
        self.state = res.json()
