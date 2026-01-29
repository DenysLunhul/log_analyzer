from etl.core.baseClass import Component
import datetime

class TypeCasterTransformer(Component):
    def process(self, data):
        for row in data:
            try:
                row["responseTime"] = int(row["responseTime"])
                date_str = row['timeStamp']
                row['timeStamp'] = datetime.datetime.strptime(
                    date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                yield row
            except (ValueError, KeyError) as e:
                print(f"Skipping corrupted row: {e}")
                continue