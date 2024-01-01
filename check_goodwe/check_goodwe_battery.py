#!/usr/bin/env python3

""" dumps errors from goodwe """

import re
import sys
from pygoodwe import API

from check_goodwe import critical, load_config, ok


def main() -> None:
    """dumps the raw data"""
    config = load_config()
    if config is None:
        sys.exit(2)
    goodwe = API(
        system_id=config.system_id,
        account=config.account,
        password=config.password,
    )
    goodwe.getCurrentReadings()

    data = goodwe.data
    inverter = data.get("inverter", [])
    if len(inverter) == 0:
        critical("No inverter data found")

    battery_status = inverter[0].get("d", {}).get("battery")
    if battery_status is None:
        critical("No battery_status field in data")
    if battery_status.strip() == "":
        critical(f"Fault detected: {battery_status=}")

    parser = re.compile("^(?P<volts>[\d\.]+)V\/(?P<amps>[\d\.]+)A\/(?P<watts>[\d\.]+)W")
    res = parser.match(battery_status)
    if res is None:
        critical(f"Couldn't parse battery status: {battery_status=}")

    try:
        if 0.0 in [float(res["volts"]), float(res["amps"]), float(res["watts"])]:
            critical(f"Fault detected: {res['volts']=},{res['amps']=},{res['watts']=}")
    except Exception as error:
        critical(f"Couldn't parse battery status: {error=}")

    ok(f"No faults detected {res.groupdict()}")


if __name__ == "__main__":
    main()
