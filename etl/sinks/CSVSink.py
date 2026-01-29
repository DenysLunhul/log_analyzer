import csv
from etl.core.baseClass import Component

class CSVSink(Component):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def process(self, data):
        try:
            writer = None
            with open(self.filepath, "w", encoding="utf-8") as file:
                for row in data:
                    if writer is None:
                        fieldnames = list(row.keys())
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                    writer.writerow(row)
                    yield row
        except Exception as e:
            print(f"Error {e} while sinking to CSV")