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
            'land_size': self._extract_other_table_data('土地面積'),
            'house_size': self._extract_other_table_data('建物面積'),
            'building_to_floor_ratio': (
                self._extract_other_table_data('建ぺい率/容積率')),
            'completion_date': self._extract_other_table_data('完成時期'),
            'available_date': self._extract_other_table_data('入居可能時期'),
            'connecting_road': self._extract_other_table_data('接道'),
            'road_contribution': self._extract_other_table_data('私道負担'),
            'number_of_floors': self._extract_other_table_data('建物階'),
            'building_status': self._extract_other_table_data('建物状況'),
            'building_condition': self._extract_other_table_data('建物現況'),
            'use_district': self._extract_other_table_data('用途地域'),
            'house_structure': self._extract_other_table_data('構造・工法'),
            'land_rights': self._extract_other_table_data('土地権利形態'),
            'has_parking': self._extract_other_table_data('駐車場・車庫'),
            'house_facilities': self._extract_house_facilities(),
            'url': self._requested_url
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
    def _extract_other_table_data(self, row_header_title):
        found_tag = self._soup.find('th', string=re.compile(row_header_title))
        if found_tag:
            return (
                found_tag
                .find_next_sibling('td')
                .get_text(strip=True)
            )
        else:
            return (
                self._soup
                .find('dt', string=re.compile(row_header_title))
                .find_next_sibling('dd')
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

    @_ignore_exceptions
    def _extract_house_facilities(self):
        ul_tag = self._soup.find('ul', class_='DetailFacility')
        if not ul_tag:
            ul_tag = self._soup.find('ul', class_='listPictRow')

        extracts = [
            li_tag.get_text(strip=True) for li_tag in ul_tag.find_all('li')
        ]
        return '|'.join(extracts)
