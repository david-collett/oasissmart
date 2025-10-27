"""Oasis Smart Controller DataUpdateCoordinator."""

import contextlib
from datetime import timedelta
import logging

from homeassistant.const import CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_CACERT_PATH, CONF_CERT_PATH, CONF_KEY_PATH, DOMAIN
from .oasis import MessageListener, OasisState, Oasis

_LOGGER = logging.getLogger(__name__)


class OasisMessageListener(MessageListener):
    """Process incoming messages."""

    def __init__(self, coordinator) -> None:
        """Initialise listener."""
        self.coordinator = coordinator

    def on_message(self, state: OasisState) -> None:
        """Handle incoming messages."""
        with contextlib.suppress(AttributeError):
            self.coordinator.set_update_interval(fast=state.pump or state.power)
        self.coordinator.async_set_updated_data(state)


class OasisCoordinator(DataUpdateCoordinator[OasisState]):
    """Class to fetch data from Oasis Heat Pump Controller."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            always_update=False,
        )

        self.api = Oasis(
            int(self.config_entry.data[CONF_UNIQUE_ID]),
            self.config_entry.data[CONF_CACERT_PATH],
            self.config_entry.data[CONF_CERT_PATH],
            self.config_entry.data[CONF_KEY_PATH],
        )

        self.api.connect(OasisMessageListener(self))
        self._fast_updates = False
        self._cancel_updates = None

        self.set_update_interval(fast=False)

    def set_update_interval(self, fast: bool) -> None:
        """Adjust the update interval."""

        # timer is already correct
        if self._cancel_updates and self._fast_updates == fast:
            return

        # cancel existing timer and start a new one
        if self._cancel_updates:
            self._cancel_updates()

        self._cancel_updates = async_track_time_interval(
            self.hass,
            self._async_request_update,
            timedelta(seconds=30 if fast else 300),
            cancel_on_shutdown=True,
        )
        self._fast_updates = fast

    async def _async_request_update(self, _):
        await self.api.request_update()

    async def shutdown(self):
        """Shutdown the API."""
        if self.api:
            await self.api.disconnect()
