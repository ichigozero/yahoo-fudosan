import filecmp

from yahoo_fudosan import CsvExporter


def test_export_listing_data_to_csv(tmp_path, dummy_listing_csv):
    input_data = {
        'cost': {
            'rent_price': '18.5万円',
            'monthly_fee': '11,000円',
            'security_deposit': 'なし',
        },
        'url': 'http://localhost',
    }
    output_path = tmp_path / 'output.csv'

    CsvExporter.export_listing_data_to_csv(
        input_data=input_data,
        output_path=output_path
    )

    filecmp.cmp(
        f1=output_path,
        f2=dummy_listing_csv
    )
