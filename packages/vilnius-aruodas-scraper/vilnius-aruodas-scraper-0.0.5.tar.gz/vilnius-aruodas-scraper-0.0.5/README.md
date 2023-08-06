# The Aruodas Web-scraper
## Description

This web_scraper is designed to collect the following information for apartments listed on the [Aruodas website](https://en.aruodas.lt/).
* City
* Sub-district
* Description
* Link
* Building number
* Flat number
* Area
* Price per month
* Build year
* Building type
* Heating system
* Energy class
* Nearest kindergarten
* Nearest educational institution
* Nearest stop
* Nearest public transport stop

The scraper methods: Loops through webpages and scrapes data off the [aruodas.lt](https://en.aruodas.lt/) website.
The method has 4 parameters:
* no_room: this is used if only one type of apartment. FOr example, to search for only 2-room apartments
* room_min: this parameter is used to specify the minimum number of rooms to be included in the search results.
* room_max: this parameter is used to specify the maximum number of rooms to be included in the search results.
* num_houses: this parameter is used to indicate the number of apartments to be scraped.


### Usage
To use the scaper, pip install the package.
```python
pip install vilnius-aruodas-scraper

from aruodas_scraper import AruodasScraper

data = AruodasScraper()

# to scrape data for 100 apartments with 1 - 4 rooms
df = data.scrape(num_houses=100, room_min=1, room_max=4)

# to scrape data for 20 apartments with a minimum of 3 rooms
df = data.scrape(num_houses=20, room_min=3)

# to scrape data for 20 apartments with a maximum of 3 rooms
df = data.scrape(num_houses=20, room_max=3)

```

## License
The MIT License - Copyright (c) 2021 - Blessing Ehizojie-Philips
