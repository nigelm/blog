---
title: 'York Bins API and Home Assistant'
date: 2020-04-20T17:05:43+01:00
categories:
  - Blog
  - 2020
tags:
  - Home-Assistant
  - Python
  - API
---

I have been using Home Assistant to automate various things at home.  One of
the things I thought would be useful was the ability for the system to inform
me of when the next bin collection is, and what sort of collection this would
be.

Thankfully York Council has an API telling you about their bin collections.
This is documented at [York Waste Collection
Lookup](https://data.yorkopendata.org/dataset/waste-collection-lookup)

## Home Assistant REST Sensors

Home Assistant helpfully can use REST sources as a sensor.  Unfortunately the
formatting of the data in the York API is not well arranged to be easy for
Home Assistant to use - in particular Home Assistant is not easily able to
handle returned data that is organised as an array of dictionaries.

People have made use of this in the past - for example see [this
example](https://community.home-assistant.io/t/sorting-rest-sensors-by-date/96786).
However this makes multiple calls to the API, which is unfriendly, and relies
on the API always returning its data in the same order in the arrya, which
appears to not be specified.

## Python Command Line Shim For Home Assistant

I decided it was better to put a shim in to pull the data from the API, do a
little processing on the data - specifically changing the date format into
something sane - and arrange these as a dictionary with some additional
overall collection data around it.

This shim can be found in the Github repository at
https://github.com/nigelm/york_bin_collection

A sample of using it would look like:-

    sensor:
      # York Bins Collection API - 3 sets, 1 for each bin
      - platform: command_line
        command: /config/york_bin_collection.py 100050567115
        name: Bin Collection
        scan_interval: 86400
        value_template: '{{ value_json.next_collection }}'
        json_attributes:
          - next_collection
          - next_collection_types
          - blackbin
          - greenbin
          - box
          - updated

and this would return the date of the next collection as the main value -
currently `2020-04-24` - and the state attributes (reported as YAML) then
looks like:-


    next_collection: '2020-04-24'
    next_collection_types:
      - blackbin
    blackbin:
      BinType: GREY 180
      BinTypeDescription: Grey Bin 180L
      CollectionDay: FRI
      CollectionDayFull: Friday
      CollectionDayOfWeek: 5
      CollectionFrequency: Alternate Weeks
      CollectionFrequencyShort: WEEK 2
      CollectionPoint: FRONT
      CollectionPointDescription: Edge of Property at Front
      CollectionPointLocation: null
      CollectionType: GREY BIN/SACK
      CollectionTypeDescription: Grey Bin/Black Sack Collection
      ImageName: blackbin
      Locality: null
      MaterialsCollected: General Domestic
      NumberOfBins: '1'
      WasteType: GREY BIN/SACK
      WasteTypeDescription: Grey Bin/Black Sack Collection
      last: '2020-04-10'
      next: '2020-04-24'
    greenbin:
      BinType: GREEN 180
      BinTypeDescription: Green Bin 180L
      CollectionDay: FRI
      CollectionDayFull: Friday
      CollectionDayOfWeek: 5
      CollectionFrequency: Alternate Weeks
      CollectionFrequencyShort: WEEK 1
      CollectionPoint: FRONT
      CollectionPointDescription: Edge of Property at Front
      CollectionPointLocation: null
      CollectionType: GREEN
      CollectionTypeDescription: Green Collection
      ImageName: greenbin
      Locality: null
      MaterialsCollected: Garden Waste
      NumberOfBins: '1'
      WasteType: GREEN
      WasteTypeDescription: Green Collection
      last: '2019-11-29'
      next: null
    box:
      BinType: BOX 55
      BinTypeDescription: Box 55L
      CollectionDay: FRI
      CollectionDayFull: Friday
      CollectionDayOfWeek: 5
      CollectionFrequency: Alternate Weeks
      CollectionFrequencyShort: WEEK 1
      CollectionPoint: FRONT
      CollectionPointDescription: Edge of Property at Front
      CollectionPointLocation: null
      CollectionType: KERBSIDE
      CollectionTypeDescription: Kerbside Collection
      ImageName: box
      Locality: null
      MaterialsCollected: 'Paper/Card : Plastic/Cans : Glass'
      NumberOfBins: '3'
      WasteType: KERBSIDE
      WasteTypeDescription: Kerbside Collection
      last: '2020-04-17'
      next: '2020-05-01'
    updated: '2020-04-20 16:25:55.918518'
    friendly_name: Bin Collection

This data can then be used in other automations - thats what I am going to
look at next.
