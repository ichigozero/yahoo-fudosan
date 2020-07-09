import re

from .property import PropertyListing


def _ignore_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, IndexError, TypeError):
            return ''

    return wrapper


class HouseListing(PropertyListing):
    def extract_house_data(self):
        return {
            'house_price': self._extract_house_price(),
        }

    @_ignore_exceptions
    def _extract_house_price(self):
        return (
            self._soup
            .find('th', string=re.compile('価格'))
            .find_next_sibling('td')
            .find('span')
            .get_text(strip=True)
        )
