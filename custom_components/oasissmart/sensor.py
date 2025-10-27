"""Sensors for Oasis Smart Controller."""

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
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
    """Set up the sensor platform."""
    async_add_entities(
        [
            TempSensor(coordinator=entry.runtime_data),
            PHSensor(coordinator=entry.runtime_data),
            ORPSensor(coordinator=entry.runtime_data),
        ]
    )


class SensorBase(OasisEntity, SensorEntity):
    """Base class for oasis sensors."""

    @callback
    def _handle_coordinator_update(self) -> None:
        if hasattr(self.coordinator.data, self._attr_translation_key):
            self._attr_native_value = getattr(
                self.coordinator.data, self._attr_translation_key
            )
            self.async_write_ha_state()


class TempSensor(SensorBase):
    """Represents the current pool water temperature."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_translation_key = "temp"
    _attr_icon = "mdi:pool-thermometer"


class PHSensor(SensorBase):
    """Represents the current pool pH."""

    _attr_device_class = SensorDeviceClass.PH
    _attr_translation_key = "ph"
    _attr_icon = "mdi:ph"


class ORPSensor(SensorBase):
    """Represents the current pool water sanitisation (ORP)."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_translation_key = "orp"
    _attr_icon = "mdi:lotion-plus"
