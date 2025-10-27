from backend.agent.tools import list_tables_tool, list_schema_tool, run_query_tool
from backend.agent.llm import conversational_llm

from langgraph.prebuilt import ToolNode

#* for testing purposes
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

#* tool nodes for listing tables and schema
list_tables_node = ToolNode([list_tables_tool])
list_schema_node = ToolNode([list_schema_tool])

#* llm node
def llm_node(state: MessagesState):
    setup_prompt = '''
    You have access to the AdventureWorks database for answering user questions. 
    To run an SQL query, ensure you know the tables that exist by using the list_tables_tool.
    Ensure the SQL query is syntactically correct by using list_schema_tool on the relevant tables.
    The names of the tables present in the AdventureWorks database all contain dots (.), wrap quotation marks around the tables when using any of them in the SQL queries
    Produce either an SQL query or if you think the database is not needed, an user-ready answer.
    '''
    
    response = conversational_llm.\
                bind_tools([list_tables_tool, list_schema_tool, run_query_tool]).\
                invoke([SystemMessage(setup_prompt)] + state['messages'])
    
    return {'messages' : [response]}

#* run_query node
run_query_node = ToolNode([run_query_tool])

#* test out the nodes
if __name__ == '__main__':
    state = MessagesState(messages=[
        HumanMessage('How many employees are present in adventureworks?')
    ])
    
    response = llm_node(state)
    
    print(response['messages'][-1].content, response['messages'][-1].tool_calls) #type: ignore
    
    