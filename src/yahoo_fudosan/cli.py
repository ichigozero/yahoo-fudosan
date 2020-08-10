import csv
import os
import time
import pickle

import click

from .rent import RentListing
from .csv import CsvExporter


@click.group()
def cmd():
    pass


@cmd.group()
def rent():
    pass


@rent.command()
@click.option('--pause', '-p', default=10)
@click.option('--max_retry', '-m', default=10)
@click.argument('input_path')
@click.argument('output_path')
def listing(pause, max_retry, input_path, output_path):
    scrape_rent_listing_data_to_csv(
        pause=pause,
        max_retry=max_retry,
        input_path=input_path,
        output_path=output_path
    )


def scrape_rent_listing_data_to_csv(
        pause,
        max_retry,
        input_path,
        output_path,
        file_count=1,
        file_counter=1
):
    with open(input_path, 'rb') as file:
        target_urls = pickle.load(file)

    # Allow user to resume scraping by looking up
    # the last fetched URL in the CSV file.
    try:
        with open(output_path, 'r') as file:
            fetched_listings = csv.DictReader(file)
            last_fetched_url = list(fetched_listings)[-1]['url']
            start_index = target_urls.index(last_fetched_url) + 1
    except OSError:
        start_index = 0

    progress_label = '({file_counter}/{file_count}) {input_file_name}'
    progress_label = progress_label.format(
        file_counter=file_counter,
        file_count=file_count,
        input_file_name=os.path.split(input_path)[1]
    )

    with click.progressbar(
            length=len(target_urls),
            label=progress_label
    ) as bar:
        bar.update(start_index)
        rent_listing = RentListing()

        for index, target_url in enumerate(target_urls[start_index:]):
            rent_listing.get_soup(target_url)

            error_occured = (
                rent_listing._soup is None or
                rent_listing.is_fetched_page_an_error_page()
            )

            if error_occured:
                print('Unable to scrape {}'.format(target_url))
                print('Terminating...')
                break

            CsvExporter.export_listing_data_to_csv(
                input_data=rent_listing.extract_rent_data(),
                output_path=output_path
            )
            bar.update(1)

            if index != len(target_urls) - 1:
                time.sleep(pause)
