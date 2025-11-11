from backend.agent.nodes import list_tables_node, list_schema_node, llm_node, run_query_node
from backend.agent.edges import next

from langgraph.graph import MessagesState, StateGraph, START

from langchain_core.messages import HumanMessage, SystemMessage

from backend.prompts import user_parsing_prompt

#* graph configuration
config={
    'recursion_limit': 50
}

#* initialize a graph
graph = StateGraph(MessagesState)

#* add the nodes
graph.add_node('llm_node', llm_node)
graph.add_node('list_tables_node', list_tables_node)
graph.add_node('list_schema_node', list_schema_node)
graph.add_node('run_query_node', run_query_node)

#* add the edges
graph.add_edge(START, 'llm_node')
graph.add_conditional_edges('llm_node', next)
graph.add_edge('list_tables_node', 'llm_node')
graph.add_edge('list_schema_node', 'llm_node')
graph.add_edge('run_query_node', 'llm_node')

#* compile
agent = graph.compile()

#* test out the agent
if __name__ == '__main__':
    state = MessagesState(messages=[
        SystemMessage(content=user_parsing_prompt),
        # HumanMessage(content="Show each customer’s name, email, territory, salesperson, their department, and the total sales amount including product names and categories.")
        HumanMessage(content="List vendors whose supplied products were sold, showing product category, total revenue, customer names, and the country where those customers are located.")
    ])
    
    #* streaming mode
    # for event in agent.stream(state):
    #     for node, update in event.items():
    #         update['messages'][-1].pretty_print()

    #         print('\n\n')

    #* invoke and see full results at once
    agent_log = agent.invoke(state, config=config)
    
    for message in agent_log['messages']:
        message.pretty_print()

