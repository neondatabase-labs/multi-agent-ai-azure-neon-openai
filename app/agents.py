import autogen
from app.database import crm_db, shipment_db
from app.schema_functions import (
    get_schema_info,
    add_customer,
    send_shipment,
)
from langchain_openai import AzureChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from app.config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT

# Azure OpenAI Model
azure_llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-10-21",
    deployment_name=AZURE_OPENAI_DEPLOYMENT,
)

# LLM Config
llm_config = {
    "config_list": [
        {
            "model": AZURE_OPENAI_DEPLOYMENT,
            "temperature": 0.7,
            "api_key": AZURE_OPENAI_KEY,
            "azure_endpoint": AZURE_OPENAI_ENDPOINT,
            "api_type": "azure",
            "api_version": "2024-10-21",
        }
    ],
    "seed": 42,
    "functions": [
        {
            "name": "query_shipment",
            "description": "Queries the Shipment database based on the provided query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute on the shipment database",
                    }
                },
                "required": ["query"],
            },
        },
        {
            "name": "query_crm",
            "description": "Queries the CRM database based on the provided query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute on the CRM database",
                    }
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_schema_info",
            "description": "Retrieves the database schema and referential integrity information. Only use 'get_schema_info' to retrieve schema information and store it. Do not do anything else",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_shared_schema_info",
            "description": "Provides the stored schema information to other agents.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "add_customer",
            "description": "Adds a customer to the CRM database by executing the 'add_customer' stored procedure with the provided parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure_name": {
                        "type": "string",
                        "description": "The name of the stored procedure to execute (should be 'add_customer')",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "A dictionary of parameters to pass to the stored procedure, including 'name', 'email', 'phone', and 'address'.",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "address": {"type": "string"},
                        },
                        "required": ["name", "email", "phone", "address"],
                    },
                },
                "required": ["procedure_name", "parameters"],
            },
        },
        {
            "name": "send_shipment",
            "description": "Sends a shipment by executing the 'send_shipment' stored procedure with the provided parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure_name": {
                        "type": "string",
                        "description": "The name of the stored procedure to execute (should be 'send_shipment')",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters for the stored procedure, including 'customer_id', 'origin_id', 'destination_id', 'shipment_date', 'items', 'status', 'tracking_status', and 'location_id'.",
                        "properties": {
                            "customer_id": {"type": "integer"},
                            "origin_id": {"type": "integer"},
                            "destination_id": {"type": "integer"},
                            "shipment_date": {"type": "string", "format": "date"},
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "product_id": {"type": "integer"},
                                        "quantity": {"type": "integer"},
                                    },
                                    "required": ["product_id", "quantity"],
                                },
                            },
                            "status": {"type": "string"},
                            "tracking_status": {"type": "string"},
                            "location_id": {"type": "integer"},
                        },
                        "required": [
                            "customer_id",
                            "origin_id",
                            "destination_id",
                            "shipment_date",
                            "items",
                            "status",
                            "tracking_status",
                            "location_id",
                        ],
                    },
                },
                "required": ["procedure_name", "parameters"],
            },
        },
    ],
}

# Initialize the database chains
shipment_chain = SQLDatabaseChain(llm=azure_llm, database=shipment_db, verbose=True)
crm_chain = SQLDatabaseChain(llm=azure_llm, database=crm_db, verbose=True)


# Query functions for each database
def query_shipment(query):
    return shipment_chain.invoke(query)


def query_crm(query):
    return crm_chain.invoke(query)


# Create assistant agents
shipment_agent = autogen.ConversableAgent(
    name="ShipmentAgent",
    llm_config=llm_config,
    description="Manage shipments in the main database.",
    system_message=(
        "Your role is to query the main database using 'query_shipment'. "
        "Focus on the shipments tables and ensure that all shipments are tracked correctly. You can make SELECT using PostgreSQL queries and do not put ``` for SQL queries. Use the 'add_customer' function to call the appropriate stored procedure for adding new customers."
        "For Insert, Update, and Delete operations, have human to validate the operation before making it."
        "Here is an example on how to call add_customer stored procedure: CALL add_customer('marcre@contoso.com', 'marcre@contoso.com', '+1 123 456 7890','1 Main Street, Redmond');"
        "Use 'get_shared_schema_info' from SchemaAgent to retrieve schema information."
    ),
)

crm_agent = autogen.ConversableAgent(
    name="CRMAgent",
    llm_config=llm_config,
    description="Manages customer and product information in the second database.",
    system_message=(
        "Your role is to query the second database using 'query_crm'. "
        "Focus on maintaining the customers and product tables. You can make SELECT using PostgreSQL queries and do not put ``` around SQL queries. Use the 'send_shipment' function to call the appropriate stored procedure for creating shipments."
        "For Insert, Update, and Delete operations, have human to validate the operation before making it."
        "Here is an example on how to call 'send_shipment' stored procedure:"
        "CALL send_shipment("
        "   customer_id     := 1,"
        "    origin_id       := 3,"
        "    destination_id  := 2,"
        "    shipment_date   := '2023-10-01',"
        "    items           := '["
        "                            {'product_id': 1, 'quantity': 5},"
        "                            {'product_id': 2, 'quantity': 3}"
        "                        ]'::jsonb,"
        "    status          := 'In Transit',"
        "    tracking_status := 'Departed Origin',"
        "    location_id     := 3"
        ");"
        "Use 'get_shared_schema_info' from SchemaAgent to retrieve schema information. "
    ),
)

schema_agent = autogen.ConversableAgent(
    name="SchemaAgent",
    llm_config=llm_config,
    description="Understands and shares database schema information.",
    system_message=(
        "Your role is to retrieve and understand the database schema and referential integrity constraints."
        "Only use 'get_schema_info' to retrieve schema information and store it. Do not do anything else. And always provide schema information when you start first."
    ),
)


# Function to share schema information between agents
def get_shared_schema_info():
    if schema_agent.schema_info is None:
        schema_agent.retrieve_and_store_schema()
    return schema_agent.schema_info


# Method to retrieve and store schema information
def retrieve_and_store_schema(agent):
    schema_info = get_schema_info()
    agent.schema_info = schema_info
    return "Schema information retrieved and stored."


# Register functions with the agents
shipment_agent.register_function(
    function_map={"query_shipment": query_shipment, "send_shipment": send_shipment}
)
crm_agent.register_function(
    function_map={"query_crm": query_crm, "add_customer": add_customer}
)
schema_agent.register_function(
    function_map={
        "get_schema_info": get_schema_info,
        "get_shared_schema_info": get_shared_schema_info,
    }
)

# Create a user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 4,
        "work_dir": "groupchat",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",  # Using this mode to give input to agents
)

# Set up the group chat and manager
groupchat = autogen.GroupChat(
    agents=[user_proxy, schema_agent, shipment_agent, crm_agent],
    messages=[],
    max_round=30,  # Maximum number of rounds in the conversation
)

manager = autogen.GroupChatManager(groupchat=groupchat)
