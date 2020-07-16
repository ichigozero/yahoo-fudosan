import copy
import re

from selenium.common.exceptions import NoSuchElementException

from .property import PropertyListing
from .property import PropertySearch


def _ignore_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, IndexError, TypeError):
            return ''

    return wrapper


class RentSearch(PropertySearch):
    def _is_page_target_page(self):
        try:
            self._webdriver.find_element_by_css_selector('h1.ttlLarge2')
            return True
        except (AttributeError, NoSuchElementException):
            return False

    def extract_search_result_count(self):
        try:
            css = 'div.toolSelect6 > p.number > span'
            return int(
                self._webdriver
                .find_element_by_css_selector(css)
                .text
                .replace(',', '')
            )
        except (AttributeError, NoSuchElementException):
            return 0


class RentListing(PropertyListing):
    def extract_rent_data(self):
        rent_data = {}

        rent_data['cost'] = {
            'rent_price': self._extract_rent_price(),
            'monthly_fee': self._extract_other_rental_cost(
                dl_tag_index=0, span_tag_index=0),
            'bond_deposit': self._extract_other_rental_cost(
                dl_tag_index=1, span_tag_index=0),
            'key_money': self._extract_other_rental_cost(
                dl_tag_index=1, span_tag_index=1),
            'security_deposit': self._extract_other_rental_cost(
                dl_tag_index=1, span_tag_index=2),
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

        rent_data['info'] = {
           'category': self._extract_table_data('物件種目'),
           'number_of_floors': self._extract_table_data('建物階'),
           'azimuth': self._extract_table_data('方位'),
           'building_structure': self._extract_table_data('構造'),
           'has_deduction': self._extract_table_data('敷引'),
           'has_parking': self._extract_table_data('駐車場'),
           'has_insurance': self._extract_table_data('保険'),
           'contract_period': self._extract_table_data('契約期間'),
           'available_date': self._extract_table_data('入居可能時期'),
           'misc_conditions': self._extract_table_data('条件等'),
           'special_note': self._extract_table_data('特記事項'),
           'discloser': self._extract_table_data('情報提供元'),
           'disclose_date': self._extract_table_data('情報公開日'),
           'update_date': self._extract_table_data('情報更新日'),
           'next_update_date': self._extract_table_data('次回更新予定日')
        }

        rent_data['url'] = self._requested_url

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
        li_tags = self._soup.find('ul', class_='listPict').find_all('li')
        extracts = [li_tag.get_text(strip=True) for li_tag in li_tags]

        return '|'.join(extracts)

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
