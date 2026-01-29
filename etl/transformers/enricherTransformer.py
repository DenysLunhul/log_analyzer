from etl.core.baseClass import Component

class EnricherTransformer(Component):
    def __init__(self, slow = 1000):
        super().__init__()
        self.slow = slow

    def process(self, data):
        for row in data:
            row['isSlow'] = row['responseTime'] > self.slow
            row['is_critical_service'] = row['service'] in ["API_Gateway", "Model_Inference_v1"]
            yield row