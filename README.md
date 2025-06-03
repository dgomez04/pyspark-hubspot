# PySpark HubSpot Connector

A PySpark 4.0 custom data source for reading data from HubSpot's CRM objects. This connector allows you to easily load HubSpot data into PySpark DataFrames.

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pyspark-hubspot.git
cd pyspark-hubspot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

4. Build the wheel file:
```bash
python setup.py bdist_wheel
```

The wheel file will be created in the `dist/` directory.

### Using pip

You can install the package directly from the wheel file:
```bash
pip install dist/pyspark_hubspot-0.1.0-py3-none-any.whl
```

## Usage

Here's a basic example of how to use the connector:

```python
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("HubSpot Connector Example") \
    .getOrCreate()

# Read contacts from HubSpot
contacts_df = spark.read \
    .format("hubspot") \
    .option("object_type", "contacts") \
    .option("api_key", "your_hubspot_api_key") \
    .option("properties", "firstname,lastname,email") \
    .option("limit", "100") \
    .load()

# Show the data
contacts_df.show()
```

### Available Options

- `object_type` (REQUIRED): The type of HubSpot object to read ("contacts", "companies", or "deals")
- `api_key` (REQUIRED): Your HubSpot private app token or OAuth2 token
- `properties`: Comma-separated list of desired fields (default: all properties)
- `associations`: Comma-separated list of associated objects (e.g., "companies")
- `limit`: Page size for API requests (default: 100)
- `archived`: Whether to include archived records ("true" or "false", default: "false")
