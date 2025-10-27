"""Switches for Oasis Smart Controller."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import OasisEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities([PrimePHSwitch(coordinator=entry.runtime_data)])


class PrimePHSwitch(OasisEntity, SwitchEntity):
    """Represents Prime PH Switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_translation_key = "primeph"
    _attr_icon = "mdi:ph"

    @callback
    def _handle_coordinator_update(self) -> None:
        if hasattr(self.coordinator.data, self._attr_translation_key):
            self._attr_is_on = getattr(
                self.coordinator.data, self._attr_translation_key
            )
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Prime PH."""
        await self.coordinator.api.set_value("primeph", True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop Prime PH."""
        await self.coordinator.api.set_value("primeph", False)
