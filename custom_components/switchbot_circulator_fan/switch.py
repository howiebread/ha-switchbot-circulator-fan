"""Oscillation switch entities for SwitchBot Battery Circulator Fan."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import SwitchBotCirculatorFanCoordinator


@dataclass(frozen=True, kw_only=True)
class OscillationSwitchDescription(SwitchEntityDescription):
    """Describe one independent oscillation axis."""

    axis: str


SWITCHES: tuple[OscillationSwitchDescription, ...] = (
    OscillationSwitchDescription(
        key="horizontal_oscillation",
        translation_key="horizontal_oscillation",
        icon="mdi:arrow-left-right",
        axis="horizontal",
    ),
    OscillationSwitchDescription(
        key="vertical_oscillation",
        translation_key="vertical_oscillation",
        icon="mdi:arrow-up-down",
        axis="vertical",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Battery Circulator Fan oscillation switches."""
    coordinator: SwitchBotCirculatorFanCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        SwitchBotOscillationSwitch(entry, coordinator, description)
        for description in SWITCHES
    )


class SwitchBotOscillationSwitch(
    CoordinatorEntity[SwitchBotCirculatorFanCoordinator], SwitchEntity
):
    """Represent one axis of Battery Circulator Fan oscillation."""

    entity_description: OscillationSwitchDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: SwitchBotCirculatorFanCoordinator,
        description: OscillationSwitchDescription,
    ) -> None:
        """Initialize the oscillation switch."""
        super().__init__(coordinator)
        self.entity_description = description
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
        return self.coordinator.data[self.entity_description.axis]

    async def async_turn_on(self, **kwargs: object) -> None:
        """Start oscillation on this entity's axis."""
        await self.coordinator.async_set_oscillation(
            self.entity_description.axis, True
        )

    async def async_turn_off(self, **kwargs: object) -> None:
        """Stop oscillation on this entity's axis."""
        await self.coordinator.async_set_oscillation(
            self.entity_description.axis, False
        )
