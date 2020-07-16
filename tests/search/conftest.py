import os

import pytest
from selenium import webdriver

from yahoo_fudosan import RentSearch


def test_file_uri(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        filename
    )
    return ''.join(['file://', path])


@pytest.fixture(scope='module')
def error_page_uri():
    return test_file_uri('error_page.html')


@pytest.fixture(scope='module')
def rent_search_uri():
    return test_file_uri('rent_search.html')


@pytest.fixture(scope='module')
def rent_search(rent_search_uri):
    def _get_firefox_options():
        options = webdriver.firefox.options.Options()
        options.headless = True

        return options

    search = RentSearch()
    # Chromium works for single test but throws error on multi tests.
    # Test should  be performed without internet connections
    # since Firefox will try to fetch updated page
    search._webdriver = webdriver.Firefox(options=_get_firefox_options())
    search._webdriver.get(rent_search_uri)
    yield search
    search._webdriver.quit()
