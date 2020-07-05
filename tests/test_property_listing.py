import requests
import time

import pytest_check as check
from bs4 import BeautifulSoup

DUMMY_URL = 'http://localhost'


def test_get_soup(requests_mock, property_listing, rent_listing_html):
    requests_mock.get(DUMMY_URL, content=rent_listing_html)
    property_listing.get_soup(DUMMY_URL)

    expected = BeautifulSoup(rent_listing_html, 'html.parser')
    check.equal(property_listing._soup, expected)
    check.equal(property_listing._requested_url, DUMMY_URL)


def test_failed_to_get_soup(
        mocker,
        requests_mock,
        sleep_mock,
        property_listing):
    spy_get_soup = mocker.spy(property_listing, 'get_soup')
    spy_sleep = mocker.spy(time, 'sleep')

    requests_mock.get(DUMMY_URL, exc=requests.exceptions.HTTPError)
    property_listing.get_soup(
        url=DUMMY_URL,
        retry_count=0,
        max_retry=5,
        retry_delay=5
    )

    check.equal(spy_get_soup.call_count, 6)
    check.equal(spy_sleep.call_count, 5)
    check.is_none(property_listing._soup)
    check.equal(property_listing._requested_url, DUMMY_URL)
