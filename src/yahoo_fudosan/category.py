from collections import namedtuple

from selenium.common.exceptions import NoSuchElementException

from .property import PropertySearch


class CategorySearch(PropertySearch):
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
