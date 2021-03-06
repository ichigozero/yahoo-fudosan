import time


def test_fetch_page(monkeypatch, mocker, rent_search, rent_search_uri):
    def _mock_function(*args, **kwargs):
        pass

    monkeypatch.setattr(
        rent_search,
        '_unhide_hidden_rent_listing_hyperlinks',
        _mock_function
    )
    spy = mocker.spy(
        rent_search,
        '_unhide_hidden_rent_listing_hyperlinks'
    )

    rent_search.fetch_page(rent_search_uri)

    spy.assert_called_once()
    assert rent_search._page_is_ready is True


def test_is_page_target_page(rent_search):
    assert rent_search._is_page_target_page() is True


def test_unhide_hidden_rent_listing_hyperlinks(
        sleep_mock,
        mocker,
        rent_search
):
    spy = mocker.spy(time, 'sleep')
    rent_search._unhide_hidden_rent_listing_hyperlinks()

    assert spy.call_count == 4


def test_page_is_not_target_page(rent_search, error_page_uri):
    rent_search._webdriver.get(error_page_uri)

    assert rent_search._is_page_target_page() is False

    # Opens HTML page prior test for other test preparation
    rent_search._webdriver.execute_script('window.history.go(-1)')
    rent_search._webdriver.refresh()


def test_extract_searchresult_count(rent_search):
    assert rent_search.extract_search_result_count() == 9859


def test_extract_rent_listing_urls(rent_search):
    first_url = last_url = next(rent_search.extract_rent_listing_urls())

    for last_url in rent_search.extract_rent_listing_urls():
        pass

    assert (
        '/rent/detail/'
        '00000103535703e80fc7d1a5efa469728314ab34e79d/'
    ) in first_url

    assert (
        '/rent/detail/'
        '_000002895183574e6287fcfba5d82460ef3dc8bacb0d/_0301525842/'
    ) in last_url


def test_extract_next_page_url(rent_search):
    output = rent_search.extract_next_page_url()
    expected = '/rent/search/03/13/13109/?page=2'

    assert expected in output
