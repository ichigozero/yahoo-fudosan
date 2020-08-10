import csv
import os


class CsvExporter:
    @staticmethod
    def export_listing_data_to_csv(input_data, output_path):
        output_data = {}
        output_exists = os.path.isfile(output_path)

        for key, value in input_data.items():
            if isinstance(value, dict):
                output_data.update(value)
            else:
                output_data[key] = value

        with open(output_path, 'a', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(output_data.keys())
            )

            if not output_exists:
                writer.writeheader()

            writer.writerow(output_data)
