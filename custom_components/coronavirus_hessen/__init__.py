"""The corona_hessen component."""

from datetime import timedelta
import logging
import re

import async_timeout
import asyncio
import bs4

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, ENDPOINT, OPTION_TOTAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

HYPHEN_PATTERN = re.compile(r"- (.)")

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Coronavirus Hessen component."""
    # Make sure coordinator is initialized.
    coordinator = await get_coordinator(hass)

    async def handle_refresh(call):
        _LOGGER.info("Refreshing Coronavirus Hessen data...")
        await coordinator.async_refresh()
    
    hass.services.async_register(DOMAIN, "refresh", handle_refresh)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Coronavirus Hessen from a config entry."""

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    return unload_ok


async def get_coordinator(hass):
    """Get the data update coordinator."""
    if DOMAIN in hass.data:
        return hass.data[DOMAIN]

    async def async_get_data():
        with async_timeout.timeout(30):
            response = await aiohttp_client.async_get_clientsession(hass).get(ENDPOINT)
            raw_html = await response.text()

        data = bs4.BeautifulSoup(raw_html, "html.parser")
        
        result = dict()
        rows = data.select("article table:first-of-type tr")

        for row in rows[2:]:
            line = row.select("td")
            if len(line) != 7:
                continue

            try:
                county = line[0].get_text(" ", strip=True)
                cases = parse_num(line[1].get_text(" ", strip=True))
                hospitalized = parse_num(line[2].get_text(" ", strip=True))
                deaths = parse_num(line[3].get_text(" ", strip=True))
            except:
                _LOGGER.exception("Error processing line {}, skipping".format(line))
                continue

            county = sanitize_county(county)
            if county == "Gesamtergebnis":
                county = OPTION_TOTAL

            result[county] = dict(cases=cases, hospitalized=hospitalized, deaths=deaths)

        _LOGGER.debug("Corona Hessen: {!r}".format(result))
        return result

    hass.data[DOMAIN] = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_data,
        update_interval=timedelta(hours=6),
    )
    await hass.data[DOMAIN].async_refresh()
    return hass.data[DOMAIN]


def parse_num(s, t=int):
    if len(s) and s != "-":
        return t(s.replace(".", "").replace(",", "."))
    return 0

def sanitize_county(county):
    """
    Sanitizes the county.

    The ministry sadly does some horrid stuff to their HTML
    and has implemented hyphenation manually, leading to
    some county names now being split in weird ways after
    extraction.

    The following replacements takes place:

      * "- <upper case letter>" -> "-<upper case letter>"
      * "- <lower case letter>" -> "<lower case letter>"
    
    Examples:

        >>> sanitize_county("LK Main-Kinzig- Kreis")
        <<< "LK Main-Kinzig-Kreis"
        >>> sanitize_county("LK Wetterau- kreis")
        <<< "LK Wetteraukreis"
        >>> sanitize_county("SK Frankfurt am Main")
        <<< "SK Frankfurt am Main"
    """

    def replace(m):
        letter = m.group(1)
        if letter.islower():
            return letter
        else:
            return "-{}".format(letter)

    return HYPHEN_PATTERN.sub(replace, county)

