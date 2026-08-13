# SwitchBot Circulator Fan

A Home Assistant custom integration for SwitchBot Battery Circulator Fan controls.

## Project status

This project is in early development. The initial scaffolding is complete; the
first planned feature is support for horizontal and vertical oscillation.

## Planned support

- Battery Circulator Fan horizontal oscillation
- Battery Circulator Fan vertical oscillation
- Future investigation of the fan's night-light feature
- Regression protection for existing Standing Fan behavior

No device controls are exposed until their PySwitchbot behavior has been
verified against a physical device.

## Development setup

The integration lives at:

```text
custom_components/switchbot_circulator_fan/
```

For local Home Assistant testing, copy that directory into the
`custom_components` folder in a non-production Home Assistant configuration.
Restart Home Assistant, then add **SwitchBot Circulator Fan** from
**Settings → Devices & services → Add integration**. The setup form currently
requests the fan's Bluetooth MAC address.

## Roadmap

See [PROJECT_CHARTER.md](PROJECT_CHARTER.md) for the project plan, stories,
testing strategy, and roadmap.

## Support and contributions

Please use GitHub Issues for bugs, confirmed device behavior, and feature
requests. Never include account credentials, access tokens, or other sensitive
information in an issue.
