import pytest_check as check


def test_extract_rent_data(rent_listing):
    rent_data = rent_listing.extract_rent_data()

    check.equal(rent_data['cost']['rent_price'], '18.5万円')
    check.equal(rent_data['cost']['monthly_fee'], '11,000円')
    check.equal(rent_data['cost']['bond_deposit'], '18.5万円')
    check.equal(rent_data['cost']['key_money'], '18.5万円')
    check.equal(rent_data['cost']['security_deposit'], 'なし')
