def test_extract_property_search_pages(category_search):
    pages = category_search.extract_property_search_pages()

    first_page = pages[0]
    assert first_page.title == '千葉市 中央区'
    assert '/rent/search/03/12/12101/' in first_page.url

    last_page = pages[-1]
    assert last_page.title == '夷隅郡御宿町'
    assert '/rent/search/03/12/12443/' in last_page.url
