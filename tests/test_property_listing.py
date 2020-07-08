import requests
import time

import pytest_check as check
from bs4 import BeautifulSoup


def test_get_soup(
        requests_mock,
        property_listing,
        rent_listing_html,
        dummy_url):
    requests_mock.get(dummy_url, content=rent_listing_html)
    property_listing.get_soup(dummy_url)

    expected = BeautifulSoup(rent_listing_html, 'html.parser')
    check.equal(property_listing._soup, expected)
    check.equal(property_listing._requested_url, dummy_url)


def test_failed_to_get_soup(
        mocker,
        requests_mock,
        sleep_mock,
        property_listing,
        dummy_url):
    spy_get_soup = mocker.spy(property_listing, 'get_soup')
    spy_sleep = mocker.spy(time, 'sleep')

    requests_mock.get(dummy_url, exc=requests.exceptions.HTTPError)
    property_listing.get_soup(
        url=dummy_url,
        retry_count=0,
        max_retry=5,
        retry_delay=5
    )

    check.equal(spy_get_soup.call_count, 6)
    check.equal(spy_sleep.call_count, 5)
    check.is_none(property_listing._soup)
    check.equal(property_listing._requested_url, dummy_url)
