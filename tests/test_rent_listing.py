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

    check.equal(
        rent_data['facility']['features'],
        (
            '日当たり良好|'
            '24時間換気システム|'
            '角部屋|'
            '仲介手数料無料'
        )
    )
    check.equal(
        rent_data['facility']['popular_items'],
        (
            'バス・トイレ独立|'
            '洗濯機置き場|'
            'エアコン|'
            '洗面台|'
            'オートロック|'
            'フローリング|'
            'モニター付きインターホン|'
            'ベランダ'
        )
    )
    check.equal(
        rent_data['facility']['bath_toilet'],
        'バス・トイレ独立 / 浴室乾燥機 / 洗面台 / 独立洗面台'
    )
    check.equal(
        rent_data['facility']['kitchen'],
        'ガスコンロ可 / システムキッチン / コンロ3口以上'
    )
    check.equal(
        rent_data['facility']['storage'],
        'ウォークインクローゼット / シューズボックス/シューズクローク'
    )
    check.equal(rent_data['facility']['porch'], 'バルコニー')
    check.equal(
        rent_data['facility']['security'],
        'オートロック / モニター付きインターホン / 管理人巡回'
    )
    check.equal(
        rent_data['facility']['facility'],
        (
            '24時間換気システム / 都市ガス / エアコン / 宅配ボックス / '
            '駐輪場 / フローリング / 高温差湯式 / 室内洗濯機置き場'
        )
    )
    check.equal(
        rent_data['facility']['room_position'],
        '日当たり良好 / 角部屋'
    )
    check.equal(
        rent_data['facility']['communication'],
        'インターネット対応 / 光回線（光ファイバー）',
    )
    check.equal(rent_data['facility']['rent_condition'], '')
    check.equal(
        rent_data['facility']['other_facility'],
        '仲介手数料無料 / 10畳以上'
    )
