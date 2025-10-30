#!/usr/bin/env python3

"""dumps errors from goodwe"""

import logging
import sys

from pygoodwe import API

from check_goodwe import critical, load_config, ok, unknown


def main() -> None:
    """dumps the raw data"""
    if "--debug" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    config = load_config()
    if config is None:
        unknown("Failed to load config")
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

    fault_code = inverter[0].get("fault_message")
    if fault_code is None:
        critical("No fault_message field in data")
    if fault_code.strip() != "":
        critical(f"Fault detected: {fault_code}")
    ok("No faults detected")


if __name__ == "__main__":
    main()
