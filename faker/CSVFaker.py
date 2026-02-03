import csv
from Faker import Faker


class CSVFaker(Faker):
    def __init__(self, header):
        super().__init__(header)

    def save_to_file(self, filepath, count, buffer_size = 10000):
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.header)
                writer.writeheader()
                buffer = []
                for row in self.generate_rows(count):
                    buffer.append(row)
                    if len(buffer) >= buffer_size:
                        writer.writerows(buffer)
                        buffer = []
                if buffer:
                    writer.writerows(buffer)
        except Exception as e:
            print(f"Error: {e} while creating csv")


if __name__ == "__main__":
    base_header = ["timeStamp", "level", "service", "responseTime", "message"]
    faker = CSVFaker(base_header)
    faker.save_to_file("../input/csv/logs.csv", 100000)