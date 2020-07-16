def test_is_page_target_page(rent_search):
    assert rent_search._is_page_target_page() is True


def test_page_is_not_target_page(rent_search, error_page_uri):
    rent_search._webdriver.get(error_page_uri)

    assert rent_search._is_page_target_page() is False

    # Opens HTML page prior test for other test preparation
    rent_search._webdriver.execute_script('window.history.go(-1)')
    rent_search._webdriver.refresh()


def test_extract_searchresult_count(rent_search):
    assert rent_search.extract_search_result_count() == 9859
