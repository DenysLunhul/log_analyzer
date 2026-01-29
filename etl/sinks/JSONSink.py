import json
from etl.core.baseClass import Component

class JSONSink(Component):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def process(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write("[\n")
                is_first_row = True
                for row in file:
                    if not is_first_row:
                        file.write(",\n")
                    json_row = json.dumps(row, indent=4)
                    file.write(json_row)
                file.write("\n]")
        except Exception as e:
            print(f"Error {e} while sinking to CSV")