class Pipeline:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def run(self):
        data = None
        for component in self.components:
            data = list(component.process(data)) if data is not None else component.process(data)