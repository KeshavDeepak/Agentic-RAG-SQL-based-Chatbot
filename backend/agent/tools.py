from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from backend.agent.llm import fixed_output_llm

#* ----------------------------------- Tools to interact with the database -----------------------------------
#* Establish a connection to the database
db = SQLDatabase.from_uri('sqlite:///backend/data/adventureworks.sqlite')

#* initialize a toolkit using the db and an llm
db_toolkit = SQLDatabaseToolkit(db=db, llm=fixed_output_llm)

#* separate out the tools from the toolkit
list_tables_tool = next(tool for tool in db_toolkit.get_tools() if tool.name == 'sql_db_list_tables')
list_schema_tool = next(tool for tool in db_toolkit.get_tools() if tool.name == 'sql_db_schema')
run_query_tool = next(tool for tool in db_toolkit.get_tools() if tool.name == 'sql_db_query')

#* test it out
if __name__ == '__main__':
    #* list out all the tables
    print(db_toolkit.get_tools()[2].invoke(''))
    
    #* use db to list out table info of ContactType
    print(print(db.run("PRAGMA table_info('Person.ContactType')")))