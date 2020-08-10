import os

import pytest


def test_file(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        filename
    )


@pytest.fixture(scope='module')
def dummy_listing_csv():
    return test_file('dummy_listing.csv')
