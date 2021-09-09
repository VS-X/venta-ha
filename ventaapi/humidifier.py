class Humidifier:
    """Class that represents a humidifier object in the Venta API."""

    def __init__(self, request):
        """Initialize a humidifier object."""
        self.state = {}
        self.request = request

        self.update()

    # Note: each property name maps the name in the returned data

    @property
    def mac(self) -> int:
        """Return the Mac of the humidifier."""
        return self.state["Header"]["MacAdress"]

    @property
    def temperature(self) -> int:
        """Return current temperature."""
        return self.state["Measure"]["Temperature"]

    @property
    def humidity(self) -> int:
        """Return current humidity."""
        return self.state["Measure"]["Humidity"]

    @property
    def dust(self) -> int:
        """Return current dust."""
        return self.state["Measure"]["Dust"]

    @property
    def target_humidity(self) -> int:
        """Return target_humidity."""
        return self.state["Action"]["TargetHum"]

    @property
    def fan_speed(self) -> int:
        """Return the fan speed."""
        return self.state["Action"]["FanSpeed"]

    @property
    def is_on(self) -> bool:
        """Return if the humidifier is running."""
        return self.state["Action"]["Power"]

    @property
    def is_sleep_mode(self) -> bool:
        """Return if the humidifier is in Sleep mode."""
        return self.state["Action"]["SleepMode"]

    @property
    def is_auto_mode(self) -> bool:
        """Return if the humidifier is in Auto mode."""
        return self.state["Action"]["Automatic"]

    def set_humidity(self, humidity: int):
        res = self.request(json={"Action": {"TargetHum": humidity}})
        self.state = res.json()

    def change_mode(self, mode: str, speed: int = 0):
        turn_off = {"Action": {"Power": False}}

        turn_on = {"Action": {"Power": True}}

        sleep_mode = {"Action": {"Power": True, "SleepMode": True, "Automatic": False}}

        automatic_mode = {
            "Action": {"Power": True, "SleepMode": False, "Automatic": True}
        }

        def fan_speed_mode(speed):
            return {
                "Action": {
                    "Power": True,
                    "SleepMode": False,
                    "Automatic": False,
                    "FanSpeed": speed,
                }
            }

        if mode == "off":
            action = turn_off
        elif mode == "on":
            action = turn_on
        elif mode == "sleep":
            action = sleep_mode
        elif mode == "automatic":
            action = automatic_mode
        elif mode == "manual":
            print("speed", speed)
            action = fan_speed_mode(speed)

        res = self.request(json=action)
        self.state = res.json()

    def update(self):
        """Update the humidifier data."""
        res = self.request()
        self.state = res.json()
