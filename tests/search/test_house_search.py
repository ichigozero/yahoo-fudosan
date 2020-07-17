def test_extract_searchresult_count(house_search):
    assert house_search.extract_search_result_count() == 22
