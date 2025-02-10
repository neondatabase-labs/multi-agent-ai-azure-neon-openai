from langchain_community.utilities.sql_database import SQLDatabase
from app.config import CRM_DB_URI, SHIPMENT_DB_URI

# Establish database connections
crm_db = SQLDatabase.from_uri(CRM_DB_URI)
shipment_db = SQLDatabase.from_uri(SHIPMENT_DB_URI)
