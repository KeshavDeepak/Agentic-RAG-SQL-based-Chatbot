from backend.agent.nodes import list_tables_node, list_schema_node, llm_node, run_query_node
from backend.agent.edges import next

from langgraph.graph import MessagesState, StateGraph, START

from langchain_core.messages import HumanMessage, SystemMessage

from backend.prompts import user_parsing_prompt

#* graph configuration
config={
    'recursion_limit': 25
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
        # HumanMessage(content="Which product categories had the highest total sales in Europe in Q3 2013, and what were the top 3 customers in each category?")
        # HumanMessage(content="List all salespersons who exceeded their sales quota in 2013, including their employee name, department, manager, and total sales value.")
        
        # HumanMessage(content="Show each customer’s name, email, territory, salesperson, their department, and the total sales amount including product names and categories.")
        # HumanMessage(content="List vendors whose supplied products were sold, showing product category, total revenue, customer names, and the country where those customers are located.")
        # HumanMessage(content="For each salesperson, list their assigned territory, number of customers handled, total sales value, and top product category sold.")
        # HumanMessage(content="Show the flow from vendor to customer: vendor name, product name, total purchased quantity, total sold quantity, and shipping method used.")
        HumanMessage(content="List each product with its category, average rating, total sales value, the territory where it sold most, and the salesperson responsible.")
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
