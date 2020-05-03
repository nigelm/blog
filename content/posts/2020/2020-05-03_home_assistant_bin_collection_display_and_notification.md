---
title: "Home Assistant - Bin Collection Display and Notification"
date: 2020-05-03T11:28:55+01:00
categories:
  - Blog
  - 2020
tags:
  - Home-Assistant
  - Jinja2
  - YAML
  - API
---

[Previously](/2020/04/20/york-bins-api-and-home-assistant/) I had built a
[[shim](https://github.com/nigelm/york_bin_collection) to make it much easier
[to import data from the [York Bin Collections
[API](https://data.yorkopendata.org/dataset/waste-collection-lookup) into Home
[Assistant

I am making use of this data in two ways:-

- Making a display card in [Lovelace](https://www.home-assistant.io/lovelace/)
  to display information about the next bin collection.
- Making a notification to prod me to put the right bins out.

## Lovelace Display

This is currently a prototype - and I need to spend more time on working out
exactly what I want from the Home Assistant display - I may move to building a
substantially minimised display for use with a spare Nook that I have - in a
similar way to [Turn an old eReader into an Information Screen (Nook
STR)](https://shkspr.mobi/blog/2020/02/turn-an-old-ereader-into-an-information-screen-nook-str/)

The display card looks like this ![Lovelace Card](/images/blog/2020/lovelace_bin_card.png)

And this is the result of adding a [Markdown
card](https://www.home-assistant.io/lovelace/markdown/), setting the title to
`Bin Collection` and filling the card in with some content.   The overall YAML
definition of the card (click the `Show Code Editor` link on the card editor)
is:

```yaml
content: >2-
   {% set bin = 'sensor.bin_collection' %}
   {% set nextdate = strptime(states(bin),'%Y-%m-%d') %}

  Next collection on {{ nextdate.strftime("%A (%-d %B, %Y)  ") }} {%- if
  'blackbin' in state_attr(bin, 'next_collection_types') %}<ha-icon
  icon="mdi:delete"></ha-icon>{% endif %} {%- if 'box' in state_attr(bin,
  'next_collection_types') %}<ha-icon icon="mdi:recycle"></ha-icon>{% endif %}
  {%- if 'greenbin' in state_attr(bin, 'next_collection_types') %}<ha-icon
  icon="mdi:pine-tree"></ha-icon>{% endif %}


  Items collected:- {% for set in state_attr(bin, 'next_collection_types') %} {%
  set thing = state_attr(bin, set) %}

  - {{ thing.MaterialsCollected }} {% endfor %}
title: Bin Collection
type: markdown
```

It is *incredibly* sensitive to initial spacing and indents...

The first two lines of the content:-

    {% set bin = 'sensor.bin_collection' %}
    {% set nextdate = strptime(states(bin),'%Y-%m-%d') %}

set the initial config up.

The next block outputs the next collection date in a reasonable format,
followed by icons for the appropriate bin type(s) - this is rather complex in
setting up the right icon to display.

The final chunk lists the types of material being collected this week - it
iterates through the types of collection for this week, and pulls the
information this collection into the `thing` variable.  Thats then used to
fill in the list elements.

This chunk may well be made more detailed in the future, but for now its a
prototype, and theres a lot of other things than can be built on this should
someone desire a different presentation.

## Bins Out Notification

The intention here was to send a nudge, on the evening before the bins are
collected, to remind me to put the appropriate bin out.

Notifications in Home Assistant are most easily handled by an
[Automation](https://www.home-assistant.io/docs/automation/). I tend to use
[Pushover](https://pushover.net/) notifications, but there are various other
[Home Assistant
Notifcations](https://www.home-assistant.io/integrations/#notifications).

The complete automation used looks like this:-

```yaml
- id: '1588360498442'
  alias: Bin Day Tomorrow Notification
  description: Tell me about bin day tomorrow
  trigger:
  - at: '19:15'
    platform: time
  condition:
  - condition: template
    value_template: '{{ as_timestamp(now())+86400 > as_timestamp(states(''sensor.bin_collection''))
      }}'
  action:
  - data_template:
      message: '{% set bin = ''sensor.bin_collection'' %}

        Items collected:- {% for set in state_attr(bin, ''next_collection_types'')
        %} {% set thing = state_attr(bin, set) %}

        - {{ thing.MaterialsCollected }} {% endfor %}

        '
      title: Bin Day Tomorrow - {{ ', '.join(state_attr('sensor.bin_collection', 'next_collection_types'))
        }}.
    service: notify.pushover
```

So this is an automation that runs every day at 19:15 (the `trigger:`
section), with a condition to check if the collection is tomorrow (see if now
as a Unix timestamp with 1 days worth of seconds added, is greater than the
timestamp version of the bin collection date - this is in the `condition:`
section).

The `action:` section calls up the Pushover notification with a message and
title mostly based on the Lovelace card information shown above.
