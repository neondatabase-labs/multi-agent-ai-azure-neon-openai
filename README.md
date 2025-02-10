# Multi-Agent AI Example with LangChain, AutoGen, Azure OpenAI, and Neon Serverless Postgres

This repository demonstrates how to build a **multi-agent AI solution** using:
- **LangChain** for natural language to SQL translation.
- **[AutoGen](https://github.com/microsoft/autogen)** for coordinating AI agents in collaborative workflows.
- **Azure OpenAI GPT-4o** for intelligent language understanding and generation of SQL queries in Neon PostgreSQL.
- **Neon Serverless Postgres** for scalable database branching and dynamic data management.

The application showcases a shipping company where AI agents manage shipments, customers, and product information. The main goal is to demonstrate how AI agents can not only **query data** but also **act on it**, extending the "Chat With Your Data" concept to "Chat and Act on Your Data."

---

## Features

- 🌐 **Gradio UI**: User-friendly interface for natural language interactions.
- 🤖 **AutoGen Multi-Agent**: AI agents collaborate for specific tasks:
  - **SchemaAgent**: Manages database schema retrieval and sharing.
  - **ShipmentAgent**: Handles shipment-related queries and updates. Uses the *send_shipment* stored procedure.
  - **CRMAgent**: Manages customer and product-related data. Uses the *add_customer* stored procedure.

---

## Getting Started

### 1. Prerequisites

- Python 3.9+ (Recommended: 3.10 or 3.11)
- A **Neon** account ([Sign up for Neon](https://neon.tech))
- **[Azure OpenAI API Endpoint](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Ckeyless%2Ctypescript-keyless%2Cpython-new&pivots=programming-language-python#retrieve-key-and-endpoint), Model Deployment Name and API Key** (For GPT-4)

---

### **2. Setup Instructions**

#### **Clone the Repository**
```bash
git clone https://github.com/your-username/multi-agent-ai-azure-neon-openai.git
cd multi-agent-ai-azure-neon-openai
```

#### Create and Configure a Neon Serverless Postgres Database

You can manually create a **Neon project** in your [Neon Console](https://console.neon.tech/) or via **[Neon API](https://neon.tech/docs/reference/api-reference)**.

**Initialize Schema & Data:**
Run the SQL queries using [Neon Console SQL Editor](https://console.neon.tech/) to create databases, tables, insert sample data, and create stored procedures:

First run SQL queries in `sql/schema_crm.sql` and then `sql/schema_shipment.sql` files.

- 1️⃣ **CRM Database:** Stores **customer and product** information.
- 2️⃣ **Shipment Database:** Stores **shipment tracking and logistics** data.

---

#### Configure .env File

Create a **.env** file in the root directory with the following contents:
```ini
# OpenAI API
AZURE_OPENAI_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Neon Database URIs
NEON_CRM_DB_URI=
NEON_SHIPMENT_DB_URI=

```

🚨 **Important:** Ensure you update these values with your **actual credentials.**

---

### **3. Virtual Environment & Dependencies**

#### **Create a Virtual Environment**
```bash
python3 -m venv .venv
```

#### **Activate the Virtual Environment**
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```

#### **Install Required Libraries**
```bash
pip install -r requirements.txt
```

---

## **Usage Examples**

### **🔍 Chat With Your Data**
✅ **Example Questions:**
- "Which products are currently in transit?"
- "Is Alice Johnson a customer?"

### **💡 Database Development Assistance**
✅ **Example Task:**
- "I need to create a stored procedure to delete customers. What would be the best way to do this?"

### **🚀 Acting on Data**
✅ **Example Actions:**
- "Can you add Marc with email `marc@contoso.com`, phone `+1 123 456 7890`, and address `1 Main Street, Redmond`?"
- "Can you create a new shipment of **1 Laptop and 1 Smartphone** for Marc and update its status to **Departed Origin** from New York to Los Angeles?"

---

## **🔧 Running the Gradio UI**

```bash
python -m app.app
```

This will launch a **Gradio UI** where you can interact with the multi-agent AI chat.

---

