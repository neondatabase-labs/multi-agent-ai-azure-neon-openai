import json
from app.database import shipment_db, crm_db
from sqlalchemy import text


# Function to retrieve database schema information
def get_schema_info():
    with shipment_db._engine.connect() as connection:
        query = text("""
        SELECT
            cols.table_schema,
            cols.table_name,
            cols.column_name,
            cols.data_type,
            cols.is_nullable,
            cons.constraint_type,
            cons.constraint_name,
            fk.references_table AS referenced_table,
            fk.references_column AS referenced_column
        FROM information_schema.columns cols
        LEFT JOIN information_schema.key_column_usage kcu
            ON cols.table_schema = kcu.table_schema
            AND cols.table_name = kcu.table_name
            AND cols.column_name = kcu.column_name
        LEFT JOIN information_schema.table_constraints cons
            ON kcu.table_schema = cons.table_schema
            AND kcu.table_name = cons.table_name
            AND kcu.constraint_name = cons.constraint_name
        LEFT JOIN (
            SELECT
                rc.constraint_name,
                kcu.table_name AS references_table,
                kcu.column_name AS references_column
            FROM information_schema.referential_constraints rc
            JOIN information_schema.key_column_usage kcu
                ON rc.unique_constraint_name = kcu.constraint_name
        ) fk
            ON cons.constraint_name = fk.constraint_name
        WHERE cols.table_schema = 'public'
        ORDER BY cols.table_schema, cols.table_name, cols.ordinal_position;
        """)
        result = connection.execute(query)
        columns = result.keys()
        rows = result.fetchall()
        # Convert the result to a list of dictionaries
        schema_info = [dict(zip(columns, row)) for row in rows]
    return json.dumps(schema_info, indent=2)


# Method to add a new customer to the CRM database
def add_customer(procedure_name, parameters):
    from sqlalchemy import text

    with crm_db._engine.connect() as connection:
        trans = connection.begin()  # Begin a transaction
        try:
            # Prepare the parameter placeholders
            param_placeholders = ", ".join([f":{k}" for k in parameters.keys()])
            # Construct the SQL command to execute the stored procedure
            sql_command = text(f"CALL {procedure_name}({param_placeholders})")
            # Pass parameters as a dictionary
            connection.execute(sql_command, parameters)
            # Commit the transaction
            trans.commit()
            # Return a success message
            return "Customer added successfully."
        except Exception as e:
            trans.rollback()
            return f"An error occurred while executing the stored procedure: {e}"


# Method to create a new shipment in the shipment database
def send_shipment(procedure_name, parameters):
    from sqlalchemy import text
    import json

    with shipment_db._engine.connect() as connection:
        trans = connection.begin()  # Begin a transaction
        try:
            # If 'items' is a list, convert it to JSON string
            if isinstance(parameters.get("items"), list):
                parameters["items"] = json.dumps(parameters["items"])
            # Prepare the parameter placeholders
            param_placeholders = ", ".join([f":{k}" for k in parameters.keys()])
            # Construct the SQL command
            sql_command = text(f"CALL {procedure_name}({param_placeholders})")
            # Execute the stored procedure
            connection.execute(sql_command, parameters)
            # Commit the transaction
            trans.commit()
            return "Shipment sent successfully."
        except Exception as e:
            trans.rollback()
            return f"An error occurred while executing the stored procedure: {e}"
