import csv
from etl.core.baseClass import Component
from etl.core.decorators import track_stats

class CSVExtractor(Component):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    @track_stats
    def process(self, data):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    yield row
        except Exception as e:
            print(f"Error: {e}, while CSV extracting")