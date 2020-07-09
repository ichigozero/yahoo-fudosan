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
    check.equal(house_data['house_layout'], '4LDK')
    check.equal(house_data['land_size'], '133.77m2（登記）')
    check.equal(house_data['house_size'], '101.02m2（登記）')
    check.equal(
        house_data['building_to_floor_ratio'],
        '建ぺい率：60/容積率：200'
    )
    check.equal(house_data['completion_date'], '2020年8月予定')
    check.equal(house_data['available_date'], '2020年8月下旬予定')
    check.equal(house_data['connecting_road'], '一方')
    check.equal(house_data['road_contribution'], '私道負担:なし')
    check.equal(house_data['number_of_floors'], '地上2階建')
    check.equal(house_data['building_status'], '未入居')
    check.equal(house_data['building_condition'], '未完成')
    check.equal(house_data['use_district'], '第一種中高層住居専用地域')
    check.equal(house_data['house_structure'], '木造')
    check.equal(house_data['land_rights'], '所有権のみ')
    check.equal(house_data['has_parking'], '有')
    check.equal(
        house_data['house_facilities'],
        '設計住宅性能評価付き|駐車場2台以上|床下収納'
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
    check.equal(house_data['house_layout'], '3LDK')
    check.equal(house_data['land_size'], '100.3m2（登記）')
    check.equal(house_data['house_size'], '92.74m2（登記）')
    check.equal(
        house_data['building_to_floor_ratio'],
        '建ぺい率：50％/容積率：150％'
    )
    check.equal(house_data['completion_date'], '2020年5月竣工済み')
    check.equal(house_data['available_date'], '即入居可')
    check.equal(house_data['connecting_road'], '一方（北東 私道 幅員5.0m）')
    check.equal(house_data['road_contribution'], '無し')
    check.equal(house_data['number_of_floors'], '地上2階建')
    check.equal(house_data['building_status'], '新築')
    check.equal(house_data['building_condition'], '完成済み')
    check.equal(house_data['use_district'], '第一種低層住居専用地域 (市街化)')
    check.equal(house_data['house_structure'], '木造')
    check.equal(house_data['land_rights'], '所有権のみ')
    check.equal(house_data['has_parking'], '有')
    check.equal(
        house_data['house_facilities'],
        (
            '分譲地内|'
            '平坦地|'
            '床暖房|'
            'トイレ２か所|'
            'リビングダイニング15畳以上|'
            '独立型キッチン|'
            '対面キッチン|'
            '浴室乾燥機あり|'
            'ウォークインクローゼット|'
            '床下収納'
        )
    )
