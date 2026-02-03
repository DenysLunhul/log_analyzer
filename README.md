# LogAnalyzer

A flexible, high-performance ETL (Extract, Transform, Load) pipeline for log analysis and processing. Built with a modular, component-based architecture using Python generators for memory-efficient stream processing of large datasets.

## 🚀 Features

- **Modular ETL Pipeline**: Chain multiple components together to build custom data processing workflows
- **Stream Processing**: Memory-efficient processing using Python generators - handles millions of rows with minimal memory
- **Performance Monitoring**: Built-in decorator system for tracking processing statistics (rows/sec, execution time)
- **Multiple Data Sources**: Support for CSV and JSON log files with streaming parsers
- **Rich Transformations**: Filter, map, type cast, and enrich log data
- **Aggregation**: Count and group log entries by various criteria
- **Multiple Output Formats**: Export results to CSV, JSON, or console
- **Extensible Architecture**: Easy to create custom components using the abstract base class
- **Decorator System**: Apply cross-cutting concerns (stats tracking, error handling, etc.) to all components

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Components](#components)
- [Advanced Usage](#advanced-usage)
- [Creating Custom Components](#creating-custom-components)
- [Performance Monitoring](#performance-monitoring)
- [Architecture](#architecture)
- [Examples](#examples)
- [License](#license)

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DenysLunhul/log_analyzer.git
   cd LogAnalyzer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Quick Start

### Basic Example

```python
from etl.core.pipeline import Pipeline
from etl.extractors.CSVExtractor import CSVExtractor
from etl.transformers.filterTransformer import FilterTransformer
from etl.sinks.consoleSink import ConsoleSink

# Create pipeline
pipeline = Pipeline()

# Add components
pipeline.add(CSVExtractor("input/csv/logs.csv"))
pipeline.add(FilterTransformer(lambda row: row["level"] == "ERROR"))
pipeline.add(ConsoleSink())

# Execute
pipeline.run()
```

### With Performance Tracking

```python
from etl.core.pipeline import Pipeline
from etl.extractors.CSVExtractor import CSVExtractor
from etl.transformers.typeCasterTransformer import TypeCasterTransformer
from etl.transformers.filterTransformer import FilterTransformer
from etl.sinks.CSVSink import CSVSink

pipeline = Pipeline()
pipeline.add(CSVExtractor("input/csv/logs.csv"))
pipeline.add(TypeCasterTransformer())  # Uses @track_stats decorator
pipeline.add(FilterTransformer(lambda row: row["level"] in ["WARNING", "ERROR"]))
pipeline.add(CSVSink("output/csv/filtered_logs.csv"))
pipeline.run()

# Output will show:
# Process: CSVExtractor            | Rows:   100000 | Time:   0.1234s
# Process: TypeCasterTransformer   | Rows:   100000 | Time:   0.0567s
# Process: FilterTransformer       | Rows:    15234 | Time:   0.0123s
# Process: CSVSink                 | Rows:    15234 | Time:   0.0456s
```

## 📁 Project Structure

```
LogAnalyzer/
├── etl/                          # Core ETL framework
│   ├── core/
│   │   ├── baseClass.py          # Abstract Component base class
│   │   ├── pipeline.py           # Pipeline orchestrator
│   │   └── decorators.py         # Performance tracking decorators
│   ├── extractors/               # Data source readers
│   │   ├── CSVExtractor.py       # CSV file reader
│   │   └── JSONExtractor.py      # Streaming JSON reader (ijson)
│   ├── transformers/             # Data transformation components
│   │   ├── filterTransformer.py      # Filter rows by condition
│   │   ├── mapTransformer.py         # Apply custom transformations
│   │   ├── typeCasterTransformer.py  # Cast data types (int, datetime)
│   │   └── enricherTransformer.py    # Add computed/derived fields
│   ├── aggregators/              # Data aggregation components
│   │   ├── count.py              # Count total rows
│   │   └── count_by.py           # Group and count by field
│   └── sinks/                    # Data output destinations
│       ├── CSVSink.py            # Write to CSV
│       ├── JSONSink.py           # Write to JSON
│       └── consoleSink.py        # Print to console
├── faker/                        # Test data generators
│   ├── Faker.py                  # Base faker class
│   ├── CSVFaker.py               # Generate test CSV data
│   └── JSONFaker.py              # Generate test JSON data
├── input/                        # Input data directory
│   ├── csv/
│   └── json/
├── output/                       # Output data directory
│   ├── csv/
│   └── json/
├── main.py                       # Example pipeline implementation
├── requirements.txt              # Project dependencies
├── LICENSE                       # MIT License
└── README.md                     # This file
```
## 🧩 Components

### Extractors (Data Sources)

#### **CSVExtractor**
Reads CSV files with automatic header detection.

```python
CSVExtractor("path/to/file.csv")
```

**Features:**
- Automatic header parsing
- Memory-efficient row-by-row reading
- UTF-8 encoding support
- Error handling for malformed files

#### **JSONExtractor**
Streams JSON arrays using ijson for memory efficiency.

```python
JSONExtractor("path/to/file.json")
```

**Features:**
- Streaming parser (handles files larger than RAM)
- Processes JSON arrays element by element
- Low memory footprint

---

### Transformers (Data Processing)

#### **TypeCasterTransformer**
Converts string data to proper Python types.

```python
TypeCasterTransformer()
```

**Conversions:**
- `responseTime`: string → int
- `timeStamp`: string → datetime object
- Skips corrupted rows with error messages

#### **MapTransformer**
Applies custom transformation functions to each row.

```python
MapTransformer(lambda row: {
    **row,
    "responseTime_minutes": row["responseTime"] / 60
})
```

**Use Cases:**
- Field calculations
- Field renaming
- Data normalization
- Custom transformations

#### **FilterTransformer**
Filters rows based on custom conditions.

```python
FilterTransformer(lambda row: row["level"] == "ERROR")
```

**Use Cases:**
- Remove unwanted data
- Extract specific log levels
- Filter by time range
- Complex boolean conditions

#### **EnricherTransformer**
Adds computed or derived fields to rows.

```python
EnricherTransformer(slow=1000)  # slow threshold in ms
```

**Added Fields:**
- `isSlow`: boolean - indicates if responseTime exceeds threshold
- `is_critical_service`: boolean - flags critical services (API_Gateway, Model_Inference_v1)

**Customizable threshold for performance analysis**

---

### Aggregators (Data Analysis)

#### **Count**
Counts total number of rows passing through.

```python
Count()
```

**Output:**
Prints total count: `{"TotalCount": 42}`

#### **CountBy**
Groups data by a field and counts occurrences.

```python
CountBy("level")  # Group by log level
```

**Output:**
Yields rows like:
```python
{"Group": "ERROR", "Count": 123}
{"Group": "WARNING", "Count": 456}
```

---

### Sinks (Data Outputs)

#### **CSVSink**
Writes data to CSV files.

```python
CSVSink("output/csv/results.csv")
```

**Features:**
- Automatic header writing
- UTF-8 encoding
- Creates output directories if needed

#### **JSONSink**
Writes data to JSON files as array.

```python
JSONSink("output/json/results.json")
```

**Features:**
- Properly formatted JSON arrays
- UTF-8 encoding
- Pretty-printed output

#### **ConsoleSink**
Prints each row to console (useful for debugging).

```python
ConsoleSink()
```

**Features:**
- Real-time output
- Pass-through component (yields rows to next component)

---

## 🎯 Advanced Usage

### Complete Log Analysis Pipeline

```python
from etl.core.pipeline import Pipeline
from etl.extractors.CSVExtractor import CSVExtractor
from etl.transformers.typeCasterTransformer import TypeCasterTransformer
from etl.transformers.mapTransformer import MapTransformer
from etl.transformers.filterTransformer import FilterTransformer
from etl.transformers.enricherTransformer import EnricherTransformer
from etl.aggregators.count import Count
from etl.sinks.CSVSink import CSVSink

pipeline = Pipeline()

# Extract
pipeline.add(CSVExtractor("input/csv/logs.csv"))

# Transform data types
pipeline.add(TypeCasterTransformer())

# Convert response time to minutes
pipeline.add(MapTransformer(lambda row: {
    **row,
    "responseTime": round(row["responseTime"] / 60, 2)
}))

# Filter for warnings and critical issues
pipeline.add(FilterTransformer(lambda row:
    row["level"] == "WARNING" or row["level"] == "CRITICAL"
))

# Add analysis flags
pipeline.add(EnricherTransformer())

# Count results
pipeline.add(Count())

# Export to CSV
pipeline.add(CSVSink("output/csv/output.csv"))

# Run pipeline
pipeline.run()
```

### Chaining Multiple Filters

```python
pipeline.add(FilterTransformer(lambda row: row["level"] == "ERROR"))
pipeline.add(FilterTransformer(lambda row: row["responseTime"] > 5000))
pipeline.add(FilterTransformer(lambda row: "API" in row["service"]))
```

### Multiple Output Destinations

```python
pipeline.add(CSVSink("output/csv/results.csv"))
pipeline.add(JSONSink("output/json/results.json"))
pipeline.add(ConsoleSink())  # Also print to console
```

### Aggregation Example

```python
from etl.aggregators.count_by import CountBy

pipeline.add(CSVExtractor("input/csv/logs.csv"))
pipeline.add(CountBy("level"))  # Group by log level
pipeline.add(ConsoleSink())

# Output:
# {"Group": "INFO", "Count": 45000}
# {"Group": "WARNING", "Count": 3500}
# {"Group": "ERROR", "Count": 1200}
# {"Group": "CRITICAL", "Count": 85}
```

---

## Creating Custom Components

All components inherit from the `Component` base class:

```python
from etl.core.baseClass import Component

class MyCustomComponent(Component):
    def __init__(self, param):
        super().__init__()
        self.param = param

    def process(self, data):
        for row in data:
            # Transform or process row
            yield modified_row
```

## Architecture

The pipeline uses a **generator-based streaming architecture**:
- Each component yields data one row at a time
- Memory-efficient for large datasets
- Components are chained together through the Pipeline class
- Data flows through: Extractor → Transformers → Aggregators → Sinks

## Dependencies

- `ijson`: Streaming JSON parser for large files

## License

MIT License
