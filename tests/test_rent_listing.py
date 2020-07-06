import pytest_check as check


def test_extract_rent_data(rent_listing):
    rent_data = rent_listing.extract_rent_data()

    check.equal(rent_data['cost']['rent_price'], '18.5万円')
