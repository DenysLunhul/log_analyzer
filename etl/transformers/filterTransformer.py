from etl.core.baseClass import Component
from etl.core.decorators import track_stats

class FilterTransformer(Component):
    def __init__(self, filter_functions):
        super().__init__()
        self.filter_functions = filter_functions

    @track_stats
    def process(self, data):
        for row in data:
            if self.filter_functions(row):
                yield row