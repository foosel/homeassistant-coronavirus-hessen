"""Support for getting current Corona data from the website of the Hessische Ministerium für Soziales und Integration."""
import logging

import voluptuous as vol

from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity

from . import get_coordinator
from .const import ATTRIBUTION, OPTION_TOTAL

_LOGGER = logging.getLogger(__name__)

ATTR_DEATHS = "deaths"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    coordinator = await get_coordinator(hass)

    async_add_entities([CoronaHessenSensor(coordinator, config_entry.data["county"])])

class CoronaHessenSensor(Entity):
    """Representation of a county with Corona cases."""

    def __init__(self, coordinator, county):
        """Initialize sensor."""
        self.coordinator = coordinator
        self.county = county
        if county == OPTION_TOTAL:
            self._name = f"Coronavirus Hessen"
        else:
            self._name = f"Coronavirus Hessen {county}"
        self._state = None

    @property
    def available(self):
        return self.coordinator.last_update_success and self.county in self.coordinator.data

    @property
    def name(self):
        return self._name
    
    @property
    def unique_id(self):
        return self._name
    
    @property
    def icon(self):
        return "mdi:biohazard"
    
    @property
    def unit_of_measurement(self):
        return "people"

    @property
    def state(self):
        return self.coordinator.data[self.county]["cases"]

    @property
    def device_state_attributes(self):
        return {ATTR_ATTRIBUTION: ATTRIBUTION,
                ATTR_DEATHS: self.coordinator.data[self.county]["deaths"]}

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)
