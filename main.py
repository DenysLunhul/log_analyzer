from etl.core.pipeline import Pipeline
from etl.extractors.CSVExtractor import CSVExtractor
from etl.extractors.JSONExtractor import JSONExtractor
from etl.sinks.CSVSink import CSVSink
from etl.sinks.consoleSink import ConsoleSink
from etl.sinks.JSONSink import JSONSink
from etl.transformers.mapTransformer import MapTransformer
from etl.transformers.filterTransformer import FilterTransformer
from etl.transformers.typeCasterTransformer import TypeCasterTransformer
from etl.transformers.enricherTransformer import EnricherTransformer
from etl.aggregators.count import Count
from etl.aggregators.count_by import CountBy


pipeline = Pipeline()
pipeline.add(CSVExtractor("input/csv/logs.csv"))
pipeline.add(TypeCasterTransformer())
pipeline.add(MapTransformer(lambda row: {**row, "responseTime": round(row["responseTime"] / 60, 2)}))
pipeline.add(FilterTransformer(lambda row: row["level"] == "WARNING" or row["level"] == "CRITICAL"))
pipeline.add(EnricherTransformer())
pipeline.add(Count())
pipeline.add(CSVSink("output/csv/output.csv"))
pipeline.run()