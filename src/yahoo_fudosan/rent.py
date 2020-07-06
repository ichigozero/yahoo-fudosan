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
