import copy
import re

from .property import PropertyListing


def _ignore_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, IndexError, TypeError):
            return ''

    return wrapper


class RentListing(PropertyListing):
    def extract_rent_data(self):
        rent_data = {}

        rent_data['cost'] = {
            'rent_price': self._extract_rent_price(),
            'monthly_fee': self._extract_other_rental_cost(0, 0),
            'bond_deposit': self._extract_other_rental_cost(1, 0),
            'key_money': self._extract_other_rental_cost(1, 1),
            'security_deposit': self._extract_other_rental_cost(1, 2),
        }

        rent_data['summary'] = {
            'location': self._extract_table_data('所在地'),
            'access': self._extract_access_to_public_transport(),
            'room_layout': self._extract_table_data('間取り'),
            'build_date': self._extract_table_data('築年数（築年月）'),
            'room_size': self._extract_table_data('専有面積'),
            'floor_number': self._extract_table_data('所在階')
        }

        rent_data['facility'] = {
            'features': self._extract_rent_features(),
            'popular_items': self._extract_popular_facilities(),
            'bath_toilet': self._extract_table_data('バス・トイレ'),
            'kitchen': self._extract_table_data('キッチン'),
            'storage': self._extract_table_data('収納'),
            'porch': self._extract_table_data('ベランダ'),
            'security': self._extract_table_data('セキュリティ'),
            'facility': self._extract_table_data('設備'),
            'room_position': self._extract_table_data('位置'),
            'communication': self._extract_table_data('通信'),
            'rent_condition': self._extract_table_data('入居条件'),
            'other_facility': self._extract_table_data('その他'),
        }

        return rent_data

    @_ignore_exceptions
    def _extract_rent_price(self):
        return (
            self._soup
            .find('dl', class_='priceData')
            .find('dd', class_='price')
            .get_text(strip=True)
        )

    @_ignore_exceptions
    def _extract_other_rental_cost(self, dl_tag_index, span_tag_index):
        return (
            self._soup
            .find_all('dl', class_='priceData')[dl_tag_index]
            .find('dd', class_='sub')
            .find_all('span')[span_tag_index]
            .get_text(strip=True)
        )

    @_ignore_exceptions
    def _extract_access_to_public_transport(self):
        extract = []
        li_tags = (
            self._soup
            .find('th', string=re.compile('交通'))
            .find_next_sibling('td')
            .find_all('li')
        )

        for li_tag in li_tags:
            # Prevent the original tree from being modified
            # when calling extract() method
            li_tag_copy = copy.copy(li_tag)
            li_tag_copy.extract()
            extract.append(li_tag_copy.get_text(strip=True))

        return '|'.join(extract)

    @_ignore_exceptions
    def _extract_rent_features(self):
        extract = []
        li_tags = self._soup.find('ul', class_='listPict').find_all('li')

        for li_tag in li_tags:
            extract.append(li_tag.get_text(strip=True))

        return '|'.join(extract)

    @_ignore_exceptions
    def _extract_popular_facilities(self):
        extract = []
        li_tags = (
            self._soup
            .find('ul', class_='listPict2')
            .find_all('li', class_='')
        )

        for li_tag in li_tags:
            # Prevent the original tree from being modified
            # when calling extract() method
            tmp = copy.copy(li_tag)
            tmp.extract()
            extract.append(tmp.get_text(strip=True))

        return '|'.join(extract)

    @_ignore_exceptions
    def _extract_table_data(self, row_header_title):
        return (
            self._soup
            .find('th', string=re.compile(row_header_title))
            .find_next_sibling('td')
            .get_text(strip=True)
        )
