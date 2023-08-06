#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import re
import logging
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


def get_property_data_extractor(url):
    p = urlparse(url)

    if p.netloc == "www.habitaclia.com":
        return HabitacliaDataExtractor(url)
    elif p.netloc == "www.pisos.com":
        return PisosComDataExtractor(url)

    raise NotImplementedError()


class PropertyDataExtractor(object):

    url = None
    _site = None
    _soup = None

    def __init__(self, url):
        self.url = url

    def process(self):
        content = self.get_content()
        self._soup = BeautifulSoup(content, 'html.parser')

    def get_content(self):
        log.debug("Getting property content from '{}'".format(self.url))
        r = requests.get(self.url)
        return r.text

    def get_site(self):
        if self._site is None:
            raise NotImplementedError()

        return self._site

    def get_id(self):
        raise NotImplementedError()

    def get_title(self):
        raise NotImplementedError()

    def get_price(self):
        raise NotImplementedError()

    def get_surface(self):
        raise NotImplementedError()

    def get_bedrooms(self):
        raise NotImplementedError()

    def get_bathrooms(self):
        raise NotImplementedError()

    def get_zone_code(self):
        raise NotImplementedError()


class HabitacliaDataExtractor(PropertyDataExtractor):

    _site = "habitaclia"

    def get_id(self):
        return self._soup.select_one("#ficha")["data-id"]

    def get_property_type(self):
        try:
            value = self._soup.select_one("#ficha")["data-propertysubtype"].lower()
        except KeyError:
            return

        if value in ("single_family_semi_detached", "paired_house", "farmhouse"):
            value = "house"
        elif value in ("studio", "apartment", "loft"):
            value = "flat"

        return value

    def get_zone_code(self, parent=None):
        entry = self._soup.select_one("#js-nom-zona-buscador")
        return entry and entry["value"] or None

    def get_title(self):
        entry = self._soup.select_one("#js-detail-description-title")
        return entry.text

    def get_price(self):
        entry = self._soup.select_one(".price span[itemprop=price]")
        return int(entry.text.replace('.', '').replace('€', ''))

    def get_feature(self, units):
        features = self._soup.select("#js-feature-container .feature")
        surface = None
        for feature in features:
            if units in feature.text:
                return int(feature.find("strong").text.replace('.', ''))

    def get_surface(self):
        return self.get_feature("m2")

    def get_bedrooms(self):
        return self.get_feature("hab.")

    def get_bathrooms(self):
        return self.get_feature("baño") or self.get_feature("baños")


class PisosComDataExtractor(PropertyDataExtractor):

    _site = "pisos.com"

    def get_id(self):
        p = urlparse(self.url)
        for part in reversed(p.path.split("/")):
            if part:
                for key in reversed(part.split("-")):
                    if key:
                        return key

    def get_property_type(self):
        value = self.get_title().lower().split(" ")[0].strip()

        if value in ("piso", "loft", "apartamento"):
            return "flat"
        elif value in ("casa", "chalet"):
            return "house"
        elif value in ("ático",):
            return "penthouse"
        elif value in ("dúplex",):
            return "duplex"

        return value

    def get_zone_code(self, parent=None):
        zone = self._soup.select_one(".maindata-info .position").text
        return re.match("^\w+(-\w+)*( \w+)*", zone).group(0).lower()

    def get_title(self):
        return self._soup.select_one(".maindata-info .title").text

    def get_price(self):
        try:
            entry = self._soup.select_one(".priceBox-price")
            return int(entry.text.replace('.', '').replace('€', ''))
        except:
            return None

    def get_surface(self):
        try:
            entry = self._soup.select_one(".basicdata-info .basicdata-item .icon-superficie")
            return int(entry.parent.text.strip().split(" ")[0])
        except:
            return None

    def get_bedrooms(self):
        try:
            entry = self._soup.select_one(".basicdata-info .basicdata-item .icon-habitaciones")
            return int(entry.parent.text.strip().split(" ")[0])
        except:
            return None

    def get_bathrooms(self):
        try:
            entry = self._soup.select_one(".basicdata-info .basicdata-item .icon-banyos")
            return int(entry.parent.text.strip().split(" ")[0])
        except:
            return None

