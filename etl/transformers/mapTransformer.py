from etl.core.baseClass import Component

class MapTransformer(Component):
    def __init__(self, transform_function):
        super().__init__()
        self.transform_function = transform_function

    def process(self, data):
        for row in data:
            yield self.transform_function(row)