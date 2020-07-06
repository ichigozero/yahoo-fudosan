import os
import time

import pytest
from bs4 import BeautifulSoup

from yahoo_fudosan import (
    PropertyListing,
    RentListing,
)


def test_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
    )
    with open(os.path.join(path, filename), 'r') as f:
        return f.read()


@pytest.fixture
def sleep_mock(monkeypatch):
    def sleep(seconds):
        pass

    monkeypatch.setattr(time, 'sleep', sleep)


@pytest.fixture(scope='module')
def rent_listing_html():
    return test_file('rent_listing.html').encode('utf-8')


@pytest.fixture
def property_listing(rent_listing_html):
    return PropertyListing()


@pytest.fixture
def rent_listing(rent_listing_html):
    listing = RentListing()
    listing._soup = BeautifulSoup(rent_listing_html, 'html.parser')

    return listing
