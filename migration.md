# Migration to RESTful sensor

As of November 2021 I've replaced this integration in my own setup with a bunch of RESTful sensors
utilizing the excellent [rki-covid-api](https://github.com/marlon360/rki-covid-api) by @marlon360
as available on [api.corona-zahlen.org](https://api.corona-zahlen.org).

My sensor configuration is the following:

``` yaml
rest:
  # Germany
  - resource: "https://api.corona-zahlen.org/germany"
    sensor:
      - name: Coronavirus Germany Cases
        value_template: "{{ value_json.cases }}"
        unit_of_measurement: people
      - name: Coronavirus Germany Deaths
        value_template: "{{ value_json.deaths }}"
        unit_of_measurement: people
      - name: Coronavirus Germany Recovered
        value_template: "{{ value_json.recovered }}"
        unit_of_measurement: people
      - name: Coronavirus Germany Incidence
        value_template: "{{ value_json.weekIncidence | round(2) }}"
      - name: Coronavirus Germany R
        value_template: "{{ value_json.r.value | round(2) }}"
      - name: Coronavirus Germany Hospitalization
        value_template: "{{ value_json.hospitalization.incidence7Days | round(2) }}"

  # Hessen
  - resource: "https://api.corona-zahlen.org/states/HE"
    sensor: 
      - name: Coronavirus Hessen Cases
        value_template: "{{ value_json.data.HE.cases }}"
        unit_of_measurement: people
      - name: Coronavirus Hessen Deaths
        value_template: "{{ value_json.data.HE.deaths }}"
        unit_of_measurement: people
      - name: Coronavirus Hessen Recovered
        value_template: "{{ value_json.data.HE.recovered }}"
        unit_of_measurement: people
      - name: Coronavirus Hessen Incidence
        value_template: "{{ value_json.data.HE.weekIncidence | round(2) }}"
      - name: Coronavirus Hessen Hospitalization
        value_template: "{{ value_json.data.HE.hospitalization.incidence7Days | round(2) }}"
  
  # Districts
  - resource: "https://api.corona-zahlen.org/districts"
    sensor: 
      # LK Offenbach = AGS 06438
      - name: Coronavirus Hessen Offenbach Landkreis
        value_template: "{{ value_json.data['06438'].cases }}"
        unit_of_measurement: people
        json_attributes_path: "$.data['06438']"
        json_attributes:
          - cases
          - deaths
          - recovered
          - weekIncidence
      - name: Coronavirus Hessen Offenbach Landkreis Incidence
        value_template: "{{ value_json.data['06438'].weekIncidence | round(2) }}"

      # LK Main-Kinzig-Kreis = AGS 06435
      - name: Coronavirus Hessen Main Kinzig Kreis
        value_template: "{{ value_json.data['06435'].cases }}"
        unit_of_measurement: people
        json_attributes_path: "$.data['06435']"
        json_attributes:
          - cases
          - deaths
          - recovered
          - weekIncidence
      - name: Coronavirus Hessen Main Kinzig Kreis Incidence
        value_template: "{{ value_json.data['06435'].weekIncidence | round(2) }}"

      # LK Wetterau = AGS 06440
      - name: Coronavirus Hessen Wetteraukreis
        value_template: "{{ value_json.data['06440'].cases }}"
        unit_of_measurement: people
        json_attributes_path: "$.data['06440']"
        json_attributes:
          - cases
          - deaths
          - recovered
          - weekIncidence
      - name: Coronavirus Hessen Wetteraukreis Incidence
        value_template: "{{ value_json.data['06440'].weekIncidence | round(2) }}"

      # SK Frankfurt = AGS 06412
      - name: Coronavirus Hessen Frankfurt
        value_template: "{{ value_json.data['06412'].cases }}"
        unit_of_measurement: people
        json_attributes_path: "$.data['06412']"
        json_attributes:
          - cases
          - deaths
          - recovered
          - weekIncidence
      - name: Coronavirus Hessen Frankfurt Incidence
        value_template: "{{ value_json.data['06412'].weekIncidence | round(2) }}"
```

In order to figure out the AGS (Amtlicher Gemeinde Schlüssel) of the districts you are interested in, 
do a search in [api.corona-zahlen.org/districts](https://api.corona-zahlen.org/districts).

If you are only interested in one district, you can also switch your district endpoint to `https://api.corona-zahlen.org/districts/<ags>`.

Read more on RESTful sensors [in the Home Assistance docs](https://www.home-assistant.io/integrations/rest/).

Read more on the available API endpoints [in the api.corona-zahlen.org docs](https://api.corona-zahlen.org/docs/).