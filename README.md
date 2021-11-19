> ✋ **Unmaintained and replaced**
>
> Having to constantly adapt to changes in the scraped HTML structure got annoying when there are better 
> options available now. Thus, as of November 2021 I've replaced this integration in my own setup with 
> a bunch of RESTful sensors utilizing the excellent [rki-covid-api](https://github.com/marlon360/rki-covid-api) 
> by @marlon360 as available on [api.corona-zahlen.org](https://api.corona-zahlen.org).
>
> Take a look at [Migration](https://github.com/foosel/homeassistant-coronavirus-hessen/blob/master/migration.md)
> if you want to do the same switch.

# Coronavirus Hessen

[Home Assistant](https://www.home-assistant.io/) component to scrape the current SARS-CoV-2 data for the German state of Hessen from the [website of the Hessisches Ministerium für Soziales und Integration](https://soziales.hessen.de/gesundheit/infektionsschutz/coronavirus-sars-cov-2/taegliche-uebersicht-der-bestaetigten-sars-cov-2-faelle-hessen).

![Screenshot of an example configuration using the integration](https://raw.githubusercontent.com/foosel/homeassistant-coronavirus-hessen/master/screenshot.png)

For a look-and-feel as displayed in the screenshot above you'll need to install [lovelace-multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row) (available on HACS), create a bunch of sensors and then use a configuration similar to this for each sensor:

``` yaml
- type: custom:multiple-entity-row
  entity: sensor.coronavirus_hessen
  entities:
    - attribute: cases
      name: Cases
    - attribute: deaths
      name: Deaths
    - attribute: incidence
      name: Incidence
  show_state: false
  icon: 'mdi:biohazard'
  name: Hessen
  secondary_info: last-changed
```

## Setup

There are two ways to set this up:

### 1. Using HACS

Open your HACS Settings and add

    https://github.com/foosel/homeassistant-coronavirus-hessen

as custom repository URL.

Then install the "Coronavirus Hessen" integration.

If you use this method, your component will always update to the latest version.

### 2. Manual

Copy the folder `custom_components/coronavirus_hessen` to `<ha_config_dir>/custom_components/`. When you are done you should have `<ha_config_dir>/custom_components/coronavirus_hessen/__init__.py`, `<ha_config_dir>/custom_components/coronavirus_hessen/sensor.py` and so on.

If you use this method then you'll need to keep an eye on this repository to check for updates.

## Configuration

In Home Assistant:

1. Enter configuration menu
2. Select "Integrations"
3. Click the "+" in the bottom right
4. Choose "Coronavirus Hessen"
5. Choose the county you wish to monitor (or "Gesamthessen" for all of Hessen)
6. Save

## Services

The integration offers one servce, `coronavirus_hessen.refresh`, which you may use to manually refresh the data from the web. It takes no arguments.

## TODO

  * [x] Find out why the created sensors don't show up in the integration overview
  * [ ] Find out if there's a possibility to select more than one county during configuration to have all created sensors under *one* integration entry
  * [x] Make this thing work with HACS for easier installation/updating

*This is my first integration for Home Assistant ever and I basically learned how to even begin to do this stuff while writing this. I'm happy for any pointers as to how to improve things.*
