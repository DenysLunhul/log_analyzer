from abc import ABC, abstractmethod
import random
import datetime

class Faker(ABC):
    def __init__(self, header):
        self.header = header
        self.current_time = datetime.datetime.now()

    def _generate_time_stamp(self):
        time_increment = datetime.timedelta(milliseconds=random.randint(50, 2000))
        self.current_time += time_increment
        return self.current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def generate_level(self):
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        weights = [20, 70, 6, 3, 1]
        return random.choices(levels, weights=weights, k=1)[0]

    def generate_service(self):
        services = ["Data_Ingestor", "Feature_Extractor", "Model_Inference_v1",
                    "Post_Processor", "System_Monitor", "API_Gateway"]
        return random.choice(services)

    def generate_response_time(self, service):
        ranges = {
            "API_Gateway": (10, 100),
            "System_Monitor": (10, 100),
            "Data_Ingestor": (100, 500),
            "Model_Inference_v1": (500, 3000),
            "Feature_Extractor": (150, 400),
            "Post_Processor": (150, 400)
        }
        low, high = ranges.get(service, (100, 500))
        return random.randint(low, high)

    def generate_message(self, level):
        messages = {
            "DEBUG": [
                "Internal state: variable _x set to 0.99",
                "Cache hit for key: user_session_88",
                "Data chunk 0x04 read successfully",
                "Initialization of subprocess complete"
            ],
            "INFO": [
                "User request processed successfully",
                "Model weights loaded into memory",
                "Batch job ID 9928 started",
                "Data synchronization complete",
                "API Heartbeat: Healthy"
            ],
            "WARNING": [
                "Memory usage at 85% capacity",
                "Slow response from database node 2",
                "Deprecated API endpoint called by client",
                "Feature scaling variance exceeds threshold"
            ],
            "ERROR": [
                "Failed to parse CSV header",
                "Timeout connecting to Model_v1_endpoint",
                "Inference failed: Input tensor shape mismatch",
                "Authorization token expired",
                "File not found: /data/raw/batch_01.csv"
            ],
            "CRITICAL": [
                "Out of Memory (OOM) - Killing process",
                "Database connection lost: No heartbeat",
                "Kernel panic in container runtime",
                "System shutdown initiated due to overheat"
            ]
        }
        options = messages.get(level, ["General system event"])
        return random.choice(options)

    def generate_row(self):
        time_stamp = self._generate_time_stamp()
        level = self.generate_level()
        service = self.generate_service()
        response_time = self.generate_response_time(service)
        message = self.generate_message(level)
        row = {"timeStamp" : time_stamp, "level": level,
               "service": service, "responseTime": response_time, "message": message}
        return row

    def generate_rows(self, count):
        for _ in range(count):
            yield self.generate_row()

    @abstractmethod
    def save_to_file(self, filepath, count, buffer_size = 10000):
        pass