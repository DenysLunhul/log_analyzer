import ijson
from etl.core.baseClass import Component

class JSONExtractor(Component):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def process(self, data):
        try:
            with open(self.filepath, "rb", encoding="utf-8") as file:
                parser = ijson.items(file, "item")
                for row in parser:
                    yield row
        except Exception as e:
            print(f"Error: {e}, while JSON extracting")