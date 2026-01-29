from etl.core.baseClass import Component

class FilterTransformer(Component):
    def __init__(self, filter_functions):
        super().__init__()
        self.filter_functions = filter_functions

    def process(self, data):
        for row in data:
            if self.filter_functions(row):
                yield row