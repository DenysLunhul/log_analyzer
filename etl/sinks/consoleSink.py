from etl.core.baseClass import Component

class ConsoleSink(Component):
    def __init__(self):
        super().__init__()

    def process(self, data):
        for row in data:
            print(row)
            yield row