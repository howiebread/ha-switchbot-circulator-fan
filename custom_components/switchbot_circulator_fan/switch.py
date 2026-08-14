"""Oscillation switch entities for SwitchBot Battery Circulator Fan."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Awaitable, Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from switchbot import SwitchbotFan, SwitchbotOperationError

from .const import DEFAULT_NAME, DOMAIN


@dataclass(frozen=True, kw_only=True)
class OscillationSwitchDescription(SwitchEntityDescription):
    """Describe one independent oscillation axis."""

    state_getter: Callable[[SwitchbotFan], bool | None]
    state_setter: Callable[[SwitchbotFan, bool], Awaitable[bool]]


SWITCHES: tuple[OscillationSwitchDescription, ...] = (
    OscillationSwitchDescription(
        key="horizontal_oscillation",
        translation_key="horizontal_oscillation",
        icon="mdi:arrow-left-right",
        state_getter=lambda fan: fan.get_horizontal_oscillating_state(),
        state_setter=lambda fan, state: fan.set_horizontal_oscillation(state),
    ),
    OscillationSwitchDescription(
        key="vertical_oscillation",
        translation_key="vertical_oscillation",
        icon="mdi:arrow-up-down",
        state_getter=lambda fan: fan.get_vertical_oscillating_state(),
        state_setter=lambda fan, state: fan.set_vertical_oscillation(state),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Battery Circulator Fan oscillation switches."""
    fan: SwitchbotFan = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        SwitchBotOscillationSwitch(entry, fan, description) for description in SWITCHES
    )


class SwitchBotOscillationSwitch(SwitchEntity):
    """Represent one axis of Battery Circulator Fan oscillation."""

    entity_description: OscillationSwitchDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        fan: SwitchbotFan,
        description: OscillationSwitchDescription,
    ) -> None:
        """Initialize the oscillation switch."""
        self.entity_description = description
        self._fan = fan
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            connections={(CONNECTION_BLUETOOTH, entry.unique_id)},
            name=DEFAULT_NAME,
            manufacturer="SwitchBot",
            model="Battery Circulator Fan",
        )

    @property
    def is_on(self) -> bool | None:
        """Return whether this oscillation axis is active."""
        return self.entity_description.state_getter(self._fan)

    @property
    def available(self) -> bool:
        """Return whether the fan has supplied a state."""
        return self._fan.get_horizontal_oscillating_state() is not None

    async def async_turn_on(self, **kwargs: object) -> None:
        """Start oscillation on this entity's axis."""
        await self._async_set_oscillation(True)

    async def async_turn_off(self, **kwargs: object) -> None:
        """Stop oscillation on this entity's axis."""
        await self._async_set_oscillation(False)

    async def async_update(self) -> None:
        """Fetch the latest state from the fan."""
        try:
            await self._fan.update()
        except SwitchbotOperationError:
            return

    async def _async_set_oscillation(self, state: bool) -> None:
        """Set this oscillation axis and refresh Home Assistant state."""
        await self.entity_description.state_setter(self._fan, state)
        self.async_write_ha_state()
