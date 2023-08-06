from requests_html import HTMLSession
import pandas as pd
from typing import TypeVar, List, Union

HTML = TypeVar('HTML')


class AruodasScraper:
    """
    AruodasScraper - scrapes house data from aruodas and returns a dataframe or csv file.

    Methods
    --------
    scrape(num_houses, room_min, room_max):
        Loops through webpages and scrapes data off the aruodas website
    """

    def __init__(self):
        self.page_number = 1
        self.results = []

    def _search_url(self, no_room: int = None, room_min: int = None, room_max: int = None) -> str:
        """
        fetches the url to be searched for results
        :param no_room: number of rooms for apartment in search results. Cannot be used with room_min and/or room_max
        :param room_min:minimum number of rooms for apartments in search results.
        :param room_max:maximum number of rooms for apartments in search results
        :return: search url
        """
        if no_room is None and room_min is None and room_max is None:
            return f"https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/{self.page_number}/"
        if no_room is not None:
            room_min = no_room
            room_max = no_room
        elif room_min is None:
            room_min = 1
        elif room_max is None:
            room_max = 50
        return f"https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/{self.page_number}/?FRoomNumMin={room_min}&FRoomNumMax={room_max}"

    @staticmethod
    def _load_page(url: str, **kwargs) -> HTML:
        """
        loads a webpage and renders all HTML
        :param url: url of page to be loaded
        :param kwargs: other parameters to load the page
        :return: HTML page
        """
        session = HTMLSession()
        page = session.get(url)
        page_html = page.html
        page_html.render(**kwargs)
        return page_html

    @staticmethod
    def _get_links(page_html: HTML) -> List[str]:
        """
        get the links of all apartment listings on a page
        :param page_html: html page to get links off
        :return: lost of apartments url
        """
        links = []
        link_container = page_html.find('td.list-adress')
        for item in link_container:
            links.extend(item.absolute_links)
        return links

    @staticmethod
    def _load_apartment(page_html: HTML) -> Union[dict, None]:
        """
        scrapes data off apartment page
        :param page_html: apartment page to be scraped
        :return: dictionary of scraped data or None
        """
        page_data = {}
        name_tag = page_html.find("h1.obj-header-text", first=True)
        if name_tag is not None and name_tag.html:
            name = name_tag.text.strip().replace('\n', '').replace(':', '')
            addr = name.split(', ')
            page_data['city'] = addr[0]
            page_data['division'] = addr[1]
            page_data['description'] = name
            page_data['link'] = page_html.url
            table = page_html.find('dl.obj-details', first=True)
            raw = table.text.replace(':', '')
            other_attrs = raw.split('\n')
            for i in range(0, len(other_attrs), 2):
                page_data[other_attrs[i]] = other_attrs[i + 1]

            energy = page_html.find('span.energy-class-tooltip', first=True)
            if energy is not None:
                page_data['energy_class'] = energy.text

            divs = page_html.find('div.statistic-info-cell-main')
            if len(divs) != 0:
                for div in divs:
                    feature = div.text
                    attr = feature.split("\n~ ")
                    page_data[attr[0]] = attr[1]
            return page_data
        return None

    def scrape(self, no_room: int = None, room_min: int = None, room_max: int = None, num_houses: int = 10) -> pd.DataFrame:
        """
        scrapes data for apartments from aruodas website
        :param no_room: used to scrape apartments with only one number of rooms. Do not use with room_min and/or room_max
        :param room_min: minimum number of rooms for apartments to be scraped
        :param room_max: maximum number of rooms for apartments to be scraped
        :param num_houses: number of apartments to get
        :return: dataframe of scraped data
        """
        while len(self.results) < num_houses:
            url = self._search_url(no_room=no_room, room_min=room_min, room_max=room_max)
            landing_page = self._load_page(url)
            if self.page_number == 1 or landing_page.url == url:
                apartment_links = self._get_links(landing_page)
                for link in apartment_links:
                    if len(self.results) < num_houses:
                        page_html = self._load_page(link, scrolldown=6, timeout=80)
                        page_data = self._load_apartment(page_html)
                        if page_data is not None:
                            self.results.append(page_data)
                print(f'Scraped {self.page_number} page(s)')
            self.page_number += 1
        df = pd.DataFrame(self.results, columns=['city', 'division', 'description', 'link', 'House No.', 'Flat No.',
                                                 'Area', 'Price per month', 'Number of rooms ', 'Floor',
                                                 'No. of floors', 'Build year', 'Building type', 'Heating system',
                                                 'energy_class', 'Nearest kindergarten',
                                                 'Nearest educational institution', 'Nearest shop',
                                                 'Public transport stop'])
        print(f'{len(self.results)} results scarped!')
        return df
