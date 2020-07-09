import pytest_check as check


def test_extract_house_data(house_listing_ag):
    house_data = house_listing_ag.extract_house_data()

    check.equal(house_data['house_price'], '2,580万円')
    check.equal(house_data['house_location'], '千葉県船橋市緑台2丁目')
    check.equal(
        house_data['access'],
        (
            '新京成電鉄 「高根公団」駅 徒歩23分|'
            '新京成電鉄 「滝不動」駅 徒歩29分|'
            '東葉高速鉄道 「飯山満」駅 徒歩32分'
        )
    )


def test_extract_alternative_house_data(house_listing_corp):
    house_data = house_listing_corp.extract_house_data()

    check.equal(house_data['house_price'], '3,880万円')
    check.equal(house_data['house_location'], '千葉県船橋市東船橋3丁目')
    check.equal(
        house_data['access'],
        (
            '総武線 「東船橋」駅 徒歩10分|'
            '総武線 「船橋」駅 バス7分 東船橋三丁目 バス停下車 徒歩2分|'
            '新京成電鉄 「前原」駅 徒歩25分'
        )
    )
