def test_extract_searchresult_count(house_search):
    assert house_search.extract_search_result_count() == 22


def test_extract_house_listing_urls(house_search):
    first_url = last_url = next(house_search.extract_house_listing_urls())

    for last_url in house_search.extract_house_listing_urls():
        pass

    assert first_url == (
        'https://realestate.yahoo.co.jp/'
        'new/house/detail_corp/b0015497640/'
    )

    assert last_url == (
        'https://realestate.yahoo.co.jp/'
        'new/house/detail_corp/b0015533403/'
    )
