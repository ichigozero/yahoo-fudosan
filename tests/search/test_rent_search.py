def test_is_page_target_page(rent_search, rent_search_uri):
    rent_search._webdriver.get(rent_search_uri)
    assert rent_search._is_page_target_page() is True


def test_page_is_not_target_page(rent_search, error_page_uri):
    rent_search._webdriver.get(error_page_uri)
    assert rent_search._is_page_target_page() is False
