import pytest_check as check


def test_extract_rent_data(rent_listing):
    rent_data = rent_listing.extract_rent_data()

    check.equal(rent_data['cost']['rent_price'], '18.5万円')
    check.equal(rent_data['cost']['monthly_fee'], '11,000円')
    check.equal(rent_data['cost']['bond_deposit'], '18.5万円')
    check.equal(rent_data['cost']['key_money'], '18.5万円')
    check.equal(rent_data['cost']['security_deposit'], 'なし')

    check.equal(rent_data['summary']['location'], '東京都品川区西五反田5')
    check.equal(
        rent_data['summary']['access'],
        (
            '不動前駅/東急目黒線 徒歩1分以内|'
            '五反田駅/山手線 徒歩13分|'
            '目黒駅/山手線 徒歩13分'
        )
    )
    check.equal(
        rent_data['summary']['room_layout'],
        '2LDK (洋5.7 洋4.9 LDK12.3)'
    )
    check.equal(rent_data['summary']['build_date'], '築18年(2002年09月)')
    check.equal(rent_data['summary']['room_size'], '57.22m2')
    check.equal(rent_data['summary']['floor_number'], '1階部分')
