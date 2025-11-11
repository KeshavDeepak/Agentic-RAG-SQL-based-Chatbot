Use sqlite dialect when writing queries  
Return final response in markdown  
Almost all of the table names contain dots (.) in their names so use quotes when referring to them in any sql queries  

Using JOIN statements is causing relevant data to be filtered, *do not use JOINs*, use LEFT JOINs and/or UNIONs instead

Use the list_tables tool to list all tables in the database  
Use the list_schema tool to get the schema of relevant tables, ensure the tables actually exist by calling list_tables first. You can input multiple tables into one call of this tool, so minimize the number of times you call this tool for performance reasons.
Do not use LEFT JOINs without ensuring that the primary-foreign key relationships being assumed are valid, always check this first in a prior query before running the actual main query
Use the run_query tool to run a query on the database; ensure the syntaxing is correct by calling list_tables,  list_schema pre-hand and if using LEFT JOINs, ensure the relationship exists