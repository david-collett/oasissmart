"""Mode selector for Oasis Smart Controller."""

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import OasisEntity
from .oasis import OasisState

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        [
            FilterPumpMode(coordinator=entry.runtime_data),
            SanitiserMode(coordinator=entry.runtime_data),
            WaterFeatureMode(coordinator=entry.runtime_data),
            HeatPumpMode(coordinator=entry.runtime_data),
        ]
    )


class ModeBase(OasisEntity, SelectEntity):
    """Represents the operating mode of an entity."""

    _attr_options = OasisState.modes
    _attr_current_option = _attr_options[0]

    @callback
    def _handle_coordinator_update(self) -> None:
        if hasattr(self.coordinator.data, self._attr_translation_key):
            self._attr_current_option = getattr(
                self.coordinator.data, self._attr_translation_key
            )
            self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Set mode."""
        await self.coordinator.api.set_value(self._attr_translation_key, option)


class FilterPumpMode(ModeBase):
    """Represents the operating mode of the filter pump."""

    _attr_icon = "mdi:air-filter"
    _attr_translation_key = "filter_pump_mode"


class SanitiserMode(ModeBase):
    """Represents the operating mode of the sanitiser."""

    _attr_icon = "mdi:lotion-plus"
    _attr_translation_key = "sanitiser_mode"


class WaterFeatureMode(ModeBase):
    """Represents the operating mode of the filter pump."""

    _attr_icon = "mdi:fountain"
    _attr_translation_key = "water_feature_mode"


class HeatPumpMode(ModeBase):
    """Represents the operating mode of the filter pump."""

    _attr_icon = "mdi:heat-pump"
    _attr_translation_key = "heat_pump_mode"
