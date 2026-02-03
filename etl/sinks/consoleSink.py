from etl.core.baseClass import Component
from etl.core.decorators import track_stats

class ConsoleSink(Component):
    def __init__(self):
        super().__init__()

    @track_stats
    def process(self, data):
        for row in data:
            print(row)
            yield row