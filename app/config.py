import os
from dotenv import load_dotenv

load_dotenv()

# CRM & Shipment Databases
CRM_DB_URI = os.getenv("NEON_CRM_DB_URI")  # CRM Database
SHIPMENT_DB_URI = os.getenv("NEON_SHIPMENT_DB_URI")  # Shipment Database

# OpenAI Config
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
