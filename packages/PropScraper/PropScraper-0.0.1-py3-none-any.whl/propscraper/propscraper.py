#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import time
import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from propscraper.propertydataextractor import (
    HabitacliaDataExtractor,
    PisosComDataExtractor
)

log = logging.getLogger(__name__)


def get_propscraper(url):
    p = urlparse(url)

    if p.netloc == "www.habitaclia.com":
        return HabitacliaPropScraper(url)
    elif p.netloc == "www.pisos.com":
        return PisosComPropScraper(url)

    raise NotImplementedError()


class PropScraper(object):

    url = None
    _soup = None

    def __init__(self, url):
        self.url = url

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()


class HabitacliaPropScraper(PropScraper):

    _entries = None

    def get_entries(self):
        if not self._entries:
            # Update URL if list is exhausted
            if self._entries is not None:
                self.set_next_url()

            if self.url:
                log.debug("Listing entries from '{}'".format(self.url))
                r = requests.get(self.url)
                self._soup = BeautifulSoup(r.text, 'html.parser')
                self._entries = self._soup.select(".list-item .list-item-title a")

    def set_next_url(self):
        nav = self._soup.select_one("#js-nav li.next a")
        if nav:
            self.url = nav["href"]
        else:
            self.url = None

    def __next__(self):
        self.get_entries()
        if self._entries:
            entry = self._entries.pop(0)
            return HabitacliaDataExtractor(entry["href"])
        else:
            raise StopIteration()


class PisosComPropScraper(PropScraper):

    def __init__(self, url):
        self.url = url
        self.urlparse = urlparse(self.url)

    _entries = None

    def get_entries(self):
        if not self._entries:
            # Update URL if list is exhausted
            if self._entries is not None:
                self.set_next_url()

            if self.url:
                log.debug("Listing entries from '{}'".format(self.url))
                r = requests.get(self.url)
                self._soup = BeautifulSoup(r.text, 'html.parser')
                self._entries = self._soup.select(".row[data-navigate-ref]")

    def set_next_url(self):
        nav = self._soup.select_one("#lnkPagSig")
        if nav:
            self.url = requests.compat.urljoin(
                "%s://%s" % (self.urlparse.scheme, self.urlparse.netloc),
                nav["href"]
            )
        else:
            self.url = None

    def __next__(self):
        self.get_entries()
        if self._entries:
            entry = self._entries.pop(0)
            url = requests.compat.urljoin(
                "%s://%s" % (self.urlparse.scheme, self.urlparse.netloc),
                entry["data-navigate-ref"]
            )
            return PisosComDataExtractor(url)
        else:
            raise StopIteration()

