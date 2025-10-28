from backend.agent.nodes import list_tables_node, list_schema_node, llm_node, run_query_node
from backend.agent.edges import next

from langgraph.graph import MessagesState, StateGraph, START, END

from langchain_core.messages import HumanMessage

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
        # HumanMessage('How many employees are present in AdventureWorks?')
        # HumanMessage('Which year was the biggest turnover')
        # HumanMessage('For each salesperson, show their total sales amount, total number of distinct customers, and their average order value for the last three years, but only include salespeople who sold products from at least three different product categories. Sort the result by total sales descending.')
        HumanMessage('Least popular product with a non-zero sales count')
        # HumanMessage('What is the meaning of life')
    ])
    
    agent_log = agent.invoke(state)
    
    for message in agent_log['messages']:
        message.pretty_print()

