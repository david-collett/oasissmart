"""Binary sensor for Heat Pump State."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
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
    async_add_entities(
        [
            FilterPumpState(coordinator=entry.runtime_data),
            SanitiserState(coordinator=entry.runtime_data),
            WaterFeatureState(coordinator=entry.runtime_data),
            HeatPumpState(coordinator=entry.runtime_data),
        ]
    )


class StateBase(OasisEntity, BinarySensorEntity):
    """Represents the current state of the heat pump."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @callback
    def _handle_coordinator_update(self) -> None:
        if hasattr(self.coordinator.data, self._attr_translation_key):
            self._attr_is_on = getattr(
                self.coordinator.data, self._attr_translation_key
            )
            self.async_write_ha_state()


class FilterPumpState(StateBase):
    """Represents the current state of the filter pump."""

    _attr_translation_key = "filter_pump_state"
    _attr_icon = "mdi:air-filter"


class SanitiserState(StateBase):
    """Represents the current state of the filter pump."""

    _attr_translation_key = "sanitiser_state"
    _attr_icon = "mdi:lotion-plus"


class WaterFeatureState(StateBase):
    """Represents the current state of the filter pump."""

    _attr_translation_key = "water_feature_state"
    _attr_icon = "mdi:fountain"


class HeatPumpState(StateBase):
    """Represents the current state of the filter pump."""

    _attr_translation_key = "heat_pump_state"
    _attr_icon = "mdi:heat-pump"
