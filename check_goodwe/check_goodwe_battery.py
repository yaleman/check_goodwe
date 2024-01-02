#!/usr/bin/env python3

""" dumps errors from goodwe """

import sys
from typing import Any, Dict, List
from pygoodwe import API

from check_goodwe import critical, load_config, ok
from check_goodwe.battery import BATTERY_PARSER

MIN_SOC_VALUE = 0.0


def get_battery_soc(inverter: List[dict[str, Any]]) -> dict[str, float]:
    """parse out the battery volts/watts/amps"""

    soc = inverter[0].get("invert_full", {}).get("soc")
    if soc is None:
        critical("No soc field in invert_full data")
    try:
        data = {"soc": float(soc)}
        if data["soc"] <= MIN_SOC_VALUE:
            critical(f"SOC or lower! soc={data['soc']}")
        return data
    except Exception as error:
        critical(f"Failed to parse {soc=} as float: {error=}")
        return {}


def get_battery_status(inverter: List[Dict[str, Any]]) -> dict[str, Any]:
    """parse out the battery volts/watts/amps"""

    battery_status = inverter[0].get("d", {}).get("battery")
    if battery_status is None:
        critical("No battery_status field in data")
    if battery_status.strip() == "":
        critical(f"Fault detected: {battery_status=}")

    res = BATTERY_PARSER.match(battery_status)
    if res is None:
        critical(f"Couldn't parse battery status: {battery_status=}")
        return {}
    groups: dict[str, str] = res.groupdict()

    try:
        if 0.0 in [
            float(groups["volts"]),
            float(groups["amps"]),
            float(groups["watts"]),
        ]:
            critical(
                f"Fault detected: {groups['volts']=},{groups['amps']=},{groups['watts']=}"
            )
    except Exception as error:
        critical(f"Couldn't parse battery status: {error=}")
    return groups


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

    battery_data = get_battery_status(inverter)

    battery_data.update(get_battery_soc(inverter))

    ok(f"No faults detected {battery_data}")


if __name__ == "__main__":
    main()
