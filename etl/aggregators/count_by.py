from etl.core.baseClass import Component

class CountBy(Component):
    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def process(self, data):
        result = {}
        for row in data:
            if row[self.keyword] not in result:
                result[row[self.keyword]] = 0
            result[row[self.keyword]] += 1
        for group, count in result.items():
            yield {"Group": group, "Count": count}