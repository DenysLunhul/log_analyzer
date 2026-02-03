import json
from Faker import Faker

class JSONFaker(Faker):
    def __init__(self, header):
        super().__init__(header)

    def save_to_file(self, filepath, count, buffer_size = 10000):
        data_to_save = []
        for _ in range(count):
            data_to_save.append(self.generate_row())
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data_to_save, file, indent=4)
        except Exception as e:
            print(f"Error: {e} while creating json")


if __name__ == "__main__":
    base_header = ["timeStamp", "level", "service", "responseTime", "message"]
    faker = JSONFaker(base_header)
    faker.save_to_file("../input/json/logs.json", 100000)