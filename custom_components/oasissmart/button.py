"""Buttons for Oasis Smart Controller."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import OasisEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        [
            PrimePHButton(coordinator=entry.runtime_data),
        ]
    )


class PrimePHButton(ButtonEntity, OasisEntity):
    """Represents the Prime PH Button."""

    _attr_translation_key = "primeph"
    _attr_icon = "mdi:ph"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.api.set_value("primeph", True)
