class Pipeline:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def run(self):
        data = None
        for component in self.components:
            data = component.process(data)

        for _ in data:
            pass