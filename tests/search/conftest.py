import os

import pytest
from selenium import webdriver

from yahoo_fudosan import HouseSearch
from yahoo_fudosan import RentSearch


def test_file_uri(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        filename
    )
    return ''.join(['file://', path])


def firefox_webdriver():
    def _get_firefox_options():
        options = webdriver.firefox.options.Options()
        options.headless = True

        return options

    # Chromium works for single test but throws error on multi tests.
    # Test should  be performed without internet connections
    # since Firefox will try to fetch updated page
    return webdriver.Firefox(options=_get_firefox_options())


@pytest.fixture(scope='module')
def error_page_uri():
    return test_file_uri('error_page.html')


@pytest.fixture(scope='module')
def house_search_uri():
    return test_file_uri('house_search.html')


@pytest.fixture(scope='module')
def rent_search_uri():
    return test_file_uri('rent_search.html')


@pytest.fixture(scope='module')
def house_search(house_search_uri):
    search = HouseSearch()
    search._webdriver = firefox_webdriver()
    search._webdriver.get(house_search_uri)
    yield search
    search._webdriver.quit()


@pytest.fixture(scope='module')
def rent_search(rent_search_uri):
    search = RentSearch()
    search._webdriver = firefox_webdriver()
    search._webdriver.get(rent_search_uri)
    yield search
    search._webdriver.quit()
