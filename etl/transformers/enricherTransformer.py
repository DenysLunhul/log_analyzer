from etl.core.baseClass import Component

class EnricherTransformer(Component):
    def __init__(self, slow = 1000):
        super().__init__()
        self.slow = slow

    def process(self, data):
        data_list = list(data)  # Convert generator to list
        if data_list:
            headers = data_list[0].keys()  # Get headers if needed
        for row in data_list:
            row['isSlow'] = row['responseTime'] > self.slow
            row['is_critical_service'] = row['service'] in ["API_Gateway", "Model_Inference_v1"]
            yield row