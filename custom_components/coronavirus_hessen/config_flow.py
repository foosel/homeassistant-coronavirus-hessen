"""Config flow for Coronavirus Hessen integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries

from . import get_coordinator
from .const import DOMAIN, OPTION_TOTAL

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coronavirus Hessen."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    _options = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._options is None:
            self._options = {OPTION_TOTAL: "Gesamthessen"}
            coordinator = await get_coordinator(self.hass)
            for county in sorted(coordinator.data.keys()):
                if county == OPTION_TOTAL:
                    continue
                self._options[county] = county

        if user_input is not None:
            await self.async_set_unique_id(user_input["county"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=self._options[user_input["county"]], data=user_input
            )

        _LOGGER.debug("Showing config form, options is {!r}".format(self._options))
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("county"): vol.In(self._options)
            }),
        )
