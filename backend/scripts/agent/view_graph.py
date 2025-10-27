from backend.agent.build_graph import agent

graph_back = agent.get_graph()

print("🧩 NODES:")
for name in graph_back.nodes:
    print(" -", name)

print("\n🕸️  EDGES:")
for edge in graph_back.edges:
    print(" -", edge)