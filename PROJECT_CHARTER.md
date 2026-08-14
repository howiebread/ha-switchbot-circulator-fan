# Project Charter and Development Plan

The full initial project charter is maintained in the project documentation
created for this repository. It will be expanded here as feature work is
completed.

## Current milestone

**CF-002 — Battery Circulator oscillation switches**

The PySwitchbot 2.2.0 API has been verified in its released source:

- `SwitchbotFan` represents the Battery Circulator Fan.
- `set_horizontal_oscillation(bool)` controls left/right oscillation.
- `set_vertical_oscillation(bool)` controls up/down oscillation.
- `get_horizontal_oscillating_state()` and
  `get_vertical_oscillating_state()` provide their respective cached states.

The two Home Assistant switches are implemented. Confirm their behavior against
the physical fan before release.
