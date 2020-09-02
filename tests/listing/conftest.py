import os

import pytest
from bs4 import BeautifulSoup

from yahoo_fudosan import PropertyListing
from yahoo_fudosan import HouseListing
from yahoo_fudosan import RentListing


def test_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
    )
    with open(os.path.join(path, filename), 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def dummy_url():
    return 'http://localhost'


@pytest.fixture(scope='module')
def error_page_html():
    return test_file('error_page.html').encode('utf-8')


@pytest.fixture(scope='module')
def listing_removed_html():
    return test_file('listing_removed.html').encode('utf-8')


@pytest.fixture(scope='module')
def rent_listing_html():
    return test_file('rent_listing.html').encode('utf-8')


@pytest.fixture(scope='module')
def house_listing_ag_html():
    return test_file('house_listing_ag.html').encode('utf-8')


@pytest.fixture(scope='module')
def house_listing_corp_html():
    return test_file('house_listing_corp.html').encode('utf-8')


@pytest.fixture
def property_listing(rent_listing_html):
    return PropertyListing()


@pytest.fixture
def rent_listing(rent_listing_html, dummy_url):
    listing = RentListing()
    listing._soup = BeautifulSoup(rent_listing_html, 'html.parser')
    listing._requested_url = dummy_url

    return listing


@pytest.fixture
def house_listing_ag(house_listing_ag_html, dummy_url):
    listing = HouseListing()
    listing._soup = BeautifulSoup(house_listing_ag_html, 'html.parser')
    listing._requested_url = dummy_url

    return listing


@pytest.fixture
def house_listing_corp(house_listing_corp_html, dummy_url):
    listing = HouseListing()
    listing._soup = BeautifulSoup(house_listing_corp_html, 'html.parser')
    listing._requested_url = dummy_url

    return listing
