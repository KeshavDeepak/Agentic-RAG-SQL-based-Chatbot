from typing import Literal

from langgraph.graph import MessagesState, END

#* conditional edge that decides which node to go to depending on the llm node's response
def next(state: MessagesState) -> Literal['list_tables_node', 'list_schema_node', 'run_query_node', END]: # type: ignore
    response = state['messages'][-1]
    
    #* check if the llm's response is a tool call or not
    if response.tool_calls: # type: ignore
        #* deduce which tool is being called and route to it
        if response.tool_calls[0]['name'] == 'sql_db_list_tables': return 'list_tables_node' # type: ignore
        if response.tool_calls[0]['name'] == 'sql_db_schema': return 'list_schema_node' # type: ignore
        if response.tool_calls[0]['name'] == 'sql_db_query': return 'run_query_node' # type: ignore
    else:
        #* a user-ready answer has been generated, go to END and finish 
        return END
        
