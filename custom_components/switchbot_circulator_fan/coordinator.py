"""Shared state coordinator for the SwitchBot Battery Circulator Fan."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from switchbot import SwitchbotFan

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SwitchBotCirculatorFanCoordinator(DataUpdateCoordinator[dict[str, bool | None]]):
    """Fetch the fan state once and share it with all fan entities."""

    def __init__(self, hass: HomeAssistant, fan: SwitchbotFan) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
            always_update=False,
        )
        self.fan = fan

    def _state(self) -> dict[str, bool | None]:
        """Return the two independent oscillation states from the fan cache."""
        return {
            "horizontal": self.fan.get_horizontal_oscillating_state(),
            "vertical": self.fan.get_vertical_oscillating_state(),
        }

    async def _async_update_data(self) -> dict[str, bool | None]:
        """Fetch a single current state snapshot from the fan."""
        cached_state = self._state()
        try:
            await self.fan.update()
        except Exception as err:
            if cached_state["horizontal"] is None and cached_state["vertical"] is None:
                raise UpdateFailed(
                    f"Unable to communicate with the fan: {err}"
                ) from err
            return cached_state

        state = self._state()
        if state["horizontal"] is None and state["vertical"] is None:
            if cached_state["horizontal"] is not None or cached_state["vertical"] is not None:
                return cached_state
            raise UpdateFailed("The fan did not return oscillation state")
        return state

    async def async_set_oscillation(self, axis: str, state: bool) -> None:
        """Set one axis and update entities without a second Bluetooth request."""
        setter = (
            self.fan.set_horizontal_oscillation
            if axis == "horizontal"
            else self.fan.set_vertical_oscillation
        )
        try:
            result = await setter(state)
        except Exception as err:
            raise UpdateFailed(f"Unable to set {axis} oscillation: {err}") from err

        if not result:
            raise UpdateFailed(f"The fan rejected the {axis} oscillation command")
        self.async_set_updated_data(self._state())
