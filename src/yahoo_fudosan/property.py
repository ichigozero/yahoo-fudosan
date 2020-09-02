import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class PropertySearch:
    def __init__(self):
        self._webdriver = None
        self._page_is_ready = False

    def launch_browser(self):
        def _get_chrome_options():
            options = webdriver.ChromeOptions()

            options.add_argument('headless')
            options.add_argument("--incognito")
            options.add_experimental_option(
                'prefs',
                {'profile.managed_default_content_settings.images': 2}
            )

            return options

        self._webdriver = webdriver.Chrome(options=_get_chrome_options())

    def quit_browser(self):
        try:
            self._webdriver.quit()
        except AttributeError:
            pass


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

    def is_fetched_page_an_error_page(self):
        try:
            h1_text = self._soup.find('h1').get_text(strip=True)
            return '表示できません' in h1_text
        except AttributeError:
            return False

    def is_target_listing_available(self):
        try:
            p_text = (
                self._soup
                .find('div', class_='contents')
                .find('p')
                .get_text(strip=True)
            )
            return '掲載終了または削除されました' not in p_text
        except AttributeError:
            return False
