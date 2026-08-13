"""Switch entities for SwitchBot Circulator Fan.

CF-002 will add the horizontal and vertical oscillation entities here after the
PySwitchbot 2.2.0 command and state interfaces are verified against hardware.
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up oscillation switches when device support is implemented."""
    # Deliberately empty: no unverified controls are exposed to users.
