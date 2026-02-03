from etl.core.baseClass import Component
from etl.core.decorators import track_stats

class MapTransformer(Component):
    def __init__(self, transform_function):
        super().__init__()
        self.transform_function = transform_function

    @track_stats
    def process(self, data):
        for row in data:
            yield self.transform_function(row)