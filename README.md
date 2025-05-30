# PySpark HubSpot DataSource Connector

This project provides a **custom PySpark 4.0 DataSource** to ingest data from HubSpot's CRM REST API into Spark. 

Supports batch reading of the following HubSpot objects:
- `contacts`
- `deals`
- `companies`

- Supports common query params:
  - `properties`
  - `limit`
  - `associations`
  - `archived`
- Paginates automatically
