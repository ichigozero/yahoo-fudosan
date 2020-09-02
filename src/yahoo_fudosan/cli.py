import csv
import os
import time
import pickle
import urllib.parse

import click

from .category import CategorySearch
from .rent import RentListing
from .rent import RentSearch
from .csv import CsvExporter


HOSTNAME = 'https://realestate.yahoo.co.jp'


@click.group()
def cmd():
    pass


@cmd.group()
def rent():
    pass


@rent.command()
@click.option('--pause', '-p', default=5)
@click.option('--max_retry', '-m', default=10)
@click.option('--output_dir', '-o', default=os.getcwd())
@click.argument('rent_category_search_url')
def listing_urls_batch(
        pause,
        max_retry,
        output_dir,
        rent_category_search_url
):
    category_search = CategorySearch()
    category_search.launch_browser()
    category_search.fetch_page(
        url=rent_category_search_url,
        max_retry=max_retry,
        retry_delay=pause
    )
    pages = category_search.extract_property_search_pages()

    for index, page in enumerate(pages, start=1):
        rent_search_url = urllib.parse.urljoin(HOSTNAME, page.url)
        output_path = os.path.join(
            output_dir,
            'rent_{}.pkl'.format(page.title)
        )

        scrape_rent_listing_urls_to_pickle(
            pause=pause,
            max_retry=max_retry,
            rent_search_url=rent_search_url,
            output_path=output_path,
            file_count=len(pages),
            file_counter=index
        )


@rent.command()
@click.option('--pause', '-p', default=5)
@click.option('--max_retry', '-m', default=10)
@click.argument('rent_search_url')
@click.argument('output_path')
def listing_urls(pause, max_retry, rent_search_url, output_path):
    scrape_rent_listing_urls_to_pickle(
        pause=pause,
        max_retry=max_retry,
        rent_search_url=rent_search_url,
        output_path=output_path
    )


def scrape_rent_listing_urls_to_pickle(
    pause,
    max_retry,
    rent_search_url,
    output_path,
    file_count=1,
    file_counter=1
):
    progress_label = '({file_counter}/{file_count}) {output_file_name}'
    progress_label = progress_label.format(
        file_counter=file_counter,
        file_count=file_count,
        output_file_name=os.path.split(output_path)[1]
    )

    with click.progressbar(length=100, label=progress_label) as bar:
        rent_search = RentSearch()
        rent_search.launch_browser()

        rent_listing_urls = []
        total_progress = 0
        has_page_to_scrape = True

        while has_page_to_scrape:
            rent_search.fetch_page(
                url=rent_search_url,
                max_retry=max_retry,
                retry_delay=pause
            )

            if not rent_search._page_is_ready:
                print('Unable to fetch {}'.format(rent_search_url))
                print('Terminating...')
                break

            for url in rent_search.extract_rent_listing_urls():
                rent_listing_urls.append(urllib.parse.urljoin(HOSTNAME, url))

            rent_search_url = rent_search.extract_next_page_url()
            if rent_search_url:
                rent_search_url = urllib.parse.urljoin(
                    HOSTNAME,
                    rent_search_url
                )
                fetched_url_count = len(rent_listing_urls)
                total_url_count = rent_search.extract_search_result_count()

                new_total_progress = int(
                    round(fetched_url_count / total_url_count * 100))
                progress_increment = new_total_progress - total_progress
                total_progress = new_total_progress

                bar.update(progress_increment)
                time.sleep(pause)
            else:
                has_page_to_scrape = False
                bar.update(100 - total_progress)

        rent_search.quit_browser()

        with open(output_path, 'wb') as file:
            pickle.dump(obj=rent_listing_urls, file=file)


@rent.command()
@click.option('--pause', '-p', default=10)
@click.option('--max_retry', '-m', default=10)
@click.argument('input_path')
@click.argument('output_path')
def listing_data(pause, max_retry, input_path, output_path):
    scrape_rent_listing_data_to_csv(
        pause=pause,
        max_retry=max_retry,
        input_path=input_path,
        output_path=output_path
    )


@rent.command()
@click.option('--pause', '-p', default=10)
@click.option('--max_retry', '-m', default=10)
@click.option('--prefix', '-P', default='rent_')
@click.option('--input_dir', '-i', default=os.getcwd())
@click.option('--output_dir', '-o', default=os.getcwd())
def listing_data_batch(pause, max_retry, prefix, input_dir, output_dir):
    input_file_names = []

    for file_name in sorted(os.listdir(input_dir)):
        if (file_name.startswith(prefix)
                and file_name.endswith('.pkl')):
            input_file_names.append(file_name)

    for index, input_file_name in enumerate(input_file_names, start=1):
        output_file_name = '{}.csv'.format(
            os.path.splitext(input_file_name)[0])

        scrape_rent_listing_data_to_csv(
            pause=pause,
            max_retry=max_retry,
            input_path=os.path.join(input_dir, input_file_name),
            output_path=os.path.join(output_dir, output_file_name),
            file_count=len(input_file_names),
            file_counter=index
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

            if not rent_listing.is_target_listing_available():
                continue

            CsvExporter.export_listing_data_to_csv(
                input_data=rent_listing.extract_rent_data(),
                output_path=output_path
            )
            bar.update(1)

            if index != len(target_urls) - 1:
                time.sleep(pause)
