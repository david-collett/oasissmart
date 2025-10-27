"""Numeric settings for Oasis Smart Controller."""

import logging

from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricPotential, UnitOfTemperature
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
            TargetTemp(coordinator=entry.runtime_data),
            TargetPH(coordinator=entry.runtime_data),
            TargetORP(coordinator=entry.runtime_data),
        ]
    )


class NumberBase(OasisEntity, NumberEntity):
    """Represents a number entry."""

    @callback
    def _handle_coordinator_update(self) -> None:
        if hasattr(self.coordinator.data, self._attr_translation_key):
            self._attr_native_value = getattr(
                self.coordinator.data, self._attr_translation_key
            )
            self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Set value."""
        await self.coordinator.api.set_value(self._attr_translation_key, int(value))


class TargetTemp(NumberBase):
    """Represents the target pool water temperature."""

    _attr_icon = "mdi:pool-thermometer"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_translation_key = "target_temp"
    _attr_native_max_value = 30
    _attr_native_min_value = 15
    _attr_native_step = 0.5


class TargetPH(NumberBase):
    """Represents the target pool PH level."""

    _attr_icon = "mdi:ph"
    _attr_device_class = NumberDeviceClass.PH
    _attr_translation_key = "target_ph"
    _attr_native_max_value = 8.5
    _attr_native_min_value = 6.5
    _attr_native_step = 0.5


class TargetORP(NumberBase):
    """Represents the target pool ORP level."""

    _attr_icon = "mdi:lotion-plus"
    _attr_device_class = NumberDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_translation_key = "target_orp"
    _attr_native_max_value = 800
    _attr_native_min_value = 600
    _attr_native_step = 10
