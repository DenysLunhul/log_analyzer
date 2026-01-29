from etl.core.baseClass import Component

class Count(Component):
    def __init__(self):
        super().__init__()

    def process(self, data):
        counter = 0
        for row in data:
            counter += 1
            yield row
        print({"TotalCount": counter})