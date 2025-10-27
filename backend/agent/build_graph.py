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
    for step in agent.stream(
        MessagesState(messages=[
            HumanMessage('How many employees are present in AdventureWorks?')
        ]),
        stream_mode='values'
    ):
        step['messages'][-1].pretty_print()
