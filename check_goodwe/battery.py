import re

BATTERY_PARSER = re.compile(
    "^(?P<volts>[-\d\.]+)V\/(?P<amps>[-\d\.]+)A\/(?P<watts>[-\d\.]+)W"
)
