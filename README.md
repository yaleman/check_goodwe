# check_goodwe

Nagios checks for goodwe things.

Please feel free to submit issues/requests!

## Commands

- `check_goodwe_faults` - check for fault codes being reported
- `check_goodwe_battery` - check non-zero volts/watts/amps/state of charge on the battery

## Configuration

Checks the following paths:

- ./check_goodwe.json
- $HOME/.config/check_goodwe.json
- /etc/check_goodwe.json

Copy the `check_goodwe.json.template` file and fill out the details. Your system ID is the end of the URL that starts with `https://www.semsportal.com/powerstation/powerstatussnmin/<here is your system id>`.

