def test_fetch_page(monkeypatch, mocker, house_search, house_search_uri):
    def _mock_function(*args, **kwargs):
        pass

    monkeypatch.setattr(
        house_search,
        '_scroll_to_end_of_page',
        _mock_function
    )
    spy = mocker.spy(
        house_search,
        '_scroll_to_end_of_page'
    )

    scroll_pause_time = 0
    house_search.fetch_page(
        url=house_search_uri,
        scroll_pause_time=scroll_pause_time
    )

    spy.assert_called_once_with(scroll_pause_time)
    assert house_search._page_is_ready is True


def test_scroll_to_end_of_page(mocker, house_search):
    spy = mocker.spy(house_search._webdriver, 'execute_script')
    house_search._scroll_to_end_of_page(scroll_pause_time=0)

    assert spy.call_count == 3


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
