from check_goodwe.battery import BATTERY_PARSER


def test_battery_parser() -> None:
    assert BATTERY_PARSER.match("0.0V/0.0A/0.0W") is not None
    assert BATTERY_PARSER.match("-0.0V/10.0A/0.0W") is not None
    assert BATTERY_PARSER.match("10.0V/-0.0A/0.0W") is not None
    assert BATTERY_PARSER.match("10.0V/-0.0A/-90.0W") is not None
