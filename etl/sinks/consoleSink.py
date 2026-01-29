from etl.core.baseClass import Component

class ConsoleSink(Component):
    def __init__(self):
        super().__init__()

    def process(self, data):
        for _ in data:
            print(_)