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
            'house_location': self._extract_house_location(),
            'access': self._extract_access_to_public_transport(),
            'house_layout': self._extract_table_data('間取り'),
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

    def _extract_house_location(self):
        table_data = self._extract_table_data('所在地')
        return table_data[:table_data.find('\n')]

    @_ignore_exceptions
    def _extract_table_data(self, row_header_title):
        found_tag = self._soup.find('th', string=re.compile(row_header_title))
        if found_tag is None:
            found_tag = (
                self._soup
                .find('span', string=re.compile(row_header_title))
                .parent
            )

        return (
            found_tag
            .find_next_sibling('td')
            .get_text(strip=True)
        )

    @_ignore_exceptions
    def _extract_access_to_public_transport(self):
        found_tag = self._soup.find('th', string=re.compile('交通'))
        if not found_tag:
            found_tag = (
                self._soup
                .find('span', string=re.compile('交通'))
                .parent
            )

        li_tags = found_tag.find_next_sibling('td').find_all('li')
        extracts = [li_tag.get_text(strip=True) for li_tag in li_tags]

        return '|'.join(extracts)
