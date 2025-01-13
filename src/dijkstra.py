from mininet.topo import MultiGraph

def shortest_path_routing(graph):
    # Initialize distances and the shortest-path tree graph
    shortest_tree = MultiGraph()
    distances = {}
    previous = {}
    visited = set()

    # Select a source node (arbitrarily, the first node in the graph)
    source = next(iter(graph.nodes()))  # Use `graph.nodes()` directly for iteration

    # Initialize all distances to infinity, except the source
    for node in graph.nodes():
        distances[node] = float('inf')
        previous[node] = None
    distances[source] = 0

    # Main loop: process nodes
    while len(visited) < len(graph.nodes()):
        # Select the unvisited node with the smallest distance
        current_node = min(
            (node for node in distances if node not in visited),
            key=lambda node: distances[node]
        )
        visited.add(current_node)

        # Iterate over all edges to find neighbors of the current node
        for edge in graph.edges(data=True):
            node1, node2, edge_params = edge
            if current_node in (node1, node2):
                neighbor = node2 if current_node == node1 else node1
                if neighbor not in visited:
                    # Retrieve edge cost from edge parameters
                    cost = edge_params.get('cost', 1)  # Default cost to 1 if not set
                    new_distance = distances[current_node] + cost
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_node

    # Build the shortest-path tree graph based on `previous`
    for node, parent in previous.items():
        if parent is not None:
            # Find the edge between `parent` and `node`
            for edge in graph.edges(data=True):
                if {parent, node} == {edge[0], edge[1]}:
                    edge_params = edge[2]
                    shortest_tree.add_edge(parent, node, **edge_params)

    return shortest_tree

