"""SwitchBot Circulator Fan integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.components import bluetooth
from switchbot import SwitchbotFan
from switchbot import parse_advertisement_data

from .const import DOMAIN
from .coordinator import SwitchBotCirculatorFanCoordinator

PLATFORMS: list[Platform] = [Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SwitchBot Circulator Fan from a config entry."""
    address = entry.data[CONF_MAC]
    if not (
        ble_device := bluetooth.async_ble_device_from_address(
            hass, address, connectable=True
        )
    ):
        raise ConfigEntryNotReady(
            f"SwitchBot Circulator Fan {address} is not currently reachable by Bluetooth"
        )

    service_info = bluetooth.async_last_service_info(
        hass, address, connectable=True
    )
    if service_info is None:
        raise ConfigEntryNotReady(
            f"No Bluetooth advertisement is available for SwitchBot Circulator Fan {address}"
        )

    fan = SwitchbotFan(ble_device)
    if not (
        advertisement := parse_advertisement_data(
            service_info.device, service_info.advertisement
        )
    ):
        raise ConfigEntryNotReady(
            f"Unable to read SwitchBot Circulator Fan advertisement for {address}"
        )
    fan.update_from_advertisement(advertisement)

    coordinator = SwitchBotCirculatorFanCoordinator(hass, fan)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a SwitchBot Circulator Fan config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
