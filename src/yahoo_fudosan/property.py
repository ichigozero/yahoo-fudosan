import requests
import time

from bs4 import BeautifulSoup


class PropertyListing:
    def __init__(self):
        self._soup = None
        self._requested_url = ''

    def get_soup(self, url, retry_count=0, max_retry=0, retry_delay=0):
        try:
            content = requests.get(url).content
            self._soup = BeautifulSoup(content, 'html.parser')
        except requests.exceptions.RequestException:
            if retry_count < max_retry:
                time.sleep(retry_delay)
                self.get_soup(url, retry_count + 1, max_retry, retry_delay)
            else:
                # Prevent scraping same page
                # if subsequent URL requests fail
                self._soup = None

        self._requested_url = url
