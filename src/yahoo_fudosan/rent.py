from .property import PropertyListing


def _ignore_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, TypeError):
            return ''

    return wrapper


class RentListing(PropertyListing):
    def extract_rent_data(self):
        return {
            'cost': {
                'rent_price': self._extract_rent_price(),
            },
        }

    @_ignore_exceptions
    def _extract_rent_price(self):
        return (
            self._soup
            .find('dl', class_='priceData')
            .find('dd', class_='price')
            .get_text(strip=True)
        )
