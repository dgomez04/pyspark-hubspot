from pyspark.sql.datasource import DataSource, DataSourceReader
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, TimestampType
from urllib.parse import urlencode
import requests
from .schemas import SCHEMA_MAPPING

class HubspotDataSource(DataSource):
    """
    A PySpark 4.0 custom data source for reading data from HubSpot's CRM objects.
    
    Supported options:
    ------------------
    - object_type: "contacts", "companies", or "deals" (REQUIRED)
    - api_key: your private app token or OAuth2 token (REQUIRED)
    - properties: comma-separated string of desired fields
    - associations: comma-separated associated objects (e.g. "companies")
    - limit: page size (default = 100)
    - archived: "true" or "false" (default = false)
    """

    @classmethod
    def name(cls):
        return "hubspot"
    
    def schema(self): 
        object_type = self.options.get("object_type")
        if not object_type:
            raise ValueError("object_type is required")
        
        if object_type not in SCHEMA_MAPPING:
            raise ValueError(f"Unsupported object_type: {object_type}. Must be one of: {', '.join(SCHEMA_MAPPING.keys())}")
        
        properties = self.options.get("properties")
        return self._build_schema(object_type, properties)
    
    def reader(self, schema: StructType):
        return HubspotReader(schema, self.options)
    
    def _build_schema(self, object_type: str, properties: str) -> StructType:
        base_schema = SCHEMA_MAPPING[object_type]
        fields = list(base_schema.fields)
        
        if properties and properties.lower() != "all":
            custom_props = [p.strip() for p in properties.split(",")]
            existing_fields = {f.name for f in fields}
            for prop in custom_props:
                if prop not in existing_fields:
                    fields.append(StructField(prop, StringType(), True))
        
        return StructType(fields)

class HubspotReader(DataSourceReader):
    def __init__(self, schema, options):
        self.schema = schema
        self.options = options
        self.api_key = options.get("api_key")
        self.object_type = options.get("object_type")
        self.properties = options.get("properties")
        self.associations = options.get("associations")
        self.limit = options.get("limit", 100)
        self.archived = options.get("archived", "false")

    def read(self):
        return self._read_data()
    
    def _read_data(self):
        url = f"https://api.hubapi.com/crm/v3/objects/{self.object_type}"
        
        headers = { "Authorization": f"Bearer {self.api_key}" }

        params = {
            "limit": self.limit,
            "archived": self.archived.lower() == "true",
        }

        if self.properties and self.properties.lower() != "all":
            params["properties"] = [p.strip() for p in self.properties.split(",")]
        
        if self.associations:
            params["associations"] = [a.strip() for a in self.associations.split(",")]

        after = None

        while True:
            request_url = url + urlencode(params, doseq=True)
            if after:
                request_url += f"&after={after}"
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])

            for obj in results:
                row = {
                    "id": obj.get("id"),
                    "archived": obj.get("archived"),
                    "createdAt": obj.get("createdAt"),
                    "updatedAt": obj.get("updatedAt"),
                }

                # Add properties from the response
                for k, v in obj.get("properties", {}).items():
                    row[k] = v
                
                yield tuple(row.get(f.name, None) for f in self.schema.fields)
            
            paging = data.get("paging", {}).get("next", {})
            after = paging.get("after")

            if not after: 
                break
        