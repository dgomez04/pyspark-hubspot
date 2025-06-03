from pyspark.sql.types import StructType, StructField, StringType, BooleanType, TimestampType, LongType, DoubleType

# Common fields for all objects
COMMON_FIELDS = [
    StructField("id", StringType(), True),
    StructField("archived", BooleanType(), True),
    StructField("createdAt", TimestampType(), True),
    StructField("updatedAt", TimestampType(), True),
]

# Base fields for Contacts
CONTACT_FIELDS = COMMON_FIELDS + [
    StructField("email", StringType(), True),
    StructField("firstname", StringType(), True),
    StructField("lastname", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("company", StringType(), True),
    StructField("website", StringType(), True),
    StructField("lifecyclestage", StringType(), True),
]

# Base fields for Companies
COMPANY_FIELDS = COMMON_FIELDS + [
    StructField("name", StringType(), True),
    StructField("domain", StringType(), True),
    StructField("industry", StringType(), True),
    StructField("type", StringType(), True),
    StructField("website", StringType(), True),
    StructField("lifecyclestage", StringType(), True),
]

# Base fields for Deals
DEAL_FIELDS = COMMON_FIELDS + [
    StructField("dealname", StringType(), True),
    StructField("pipeline", StringType(), True),
    StructField("dealstage", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("closedate", TimestampType(), True),
    StructField("dealtype", StringType(), True),
]

# Schema mapping for each object type
SCHEMA_MAPPING = {
    "contacts": StructType(CONTACT_FIELDS),
    "companies": StructType(COMPANY_FIELDS),
    "deals": StructType(DEAL_FIELDS),
} 