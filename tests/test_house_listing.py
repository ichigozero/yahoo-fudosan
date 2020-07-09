import pytest_check as check


def test_extract_house_data(house_listing_ag):
    house_data = house_listing_ag.extract_house_data()

    check.equal(house_data['house_price'], '2,580万円')


def test_extract_alternative_house_data(house_listing_corp):
    house_data = house_listing_corp.extract_house_data()

    check.equal(house_data['house_price'], '3,880万円')
