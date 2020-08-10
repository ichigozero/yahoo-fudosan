import time
from collections import namedtuple

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from .property import PropertySearch


class CategorySearch(PropertySearch):
    def fetch_page(self, url, retry_count=0, max_retry=0, retry_delay=0):
        try:
            self._webdriver.get(url)
            self._page_is_ready = True
        except TimeoutException:
            if retry_count < max_retry:
                time.sleep(retry_delay)
                self.fetch_page(url, retry_count + 1, max_retry, retry_delay)
            else:
                self._page_is_ready = False

    def extract_property_search_pages(self):
        try:
            a_tags = (
                self._webdriver
                .find_elements_by_css_selector('span.iconCheckbox > a')
            )
            Page = namedtuple('Page', ('title', 'url'))
            return [
                Page(
                    a_tag.text,
                    a_tag.get_attribute('href')
                ) for a_tag in a_tags
            ]
        except (AttributeError, NoSuchElementException):
            pass
