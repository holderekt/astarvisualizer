from queue import PriorityQueue

def generatePath(node, parent_trace):
    current_parent = node
    path = []
    while current_parent is not None:
        path.append(current_parent)
        current_parent = parent_trace[current_parent]
    return path
   
def AstarSearch(start, finish, graph):
    closed_set = []
    open_set = [start]
    frontier = PriorityQueue()
    parent_trace = {start:None}
    nodes_cost = {start:0}
    frontier.put((0,start))

    while not frontier.empty():
        _, current_node = frontier.get()
        open_set.remove(current_node)
        closed_set.append(current_node)

        if current_node == finish:
            return generatePath(current_node, parent_trace), closed_set

        for neighbor in graph.getNeighbor(current_node):
            if neighbor in closed_set:
                continue

            neighbor_cost = nodes_cost[current_node] + graph.getWeight(neighbor, current_node)
            if (neighbor not in open_set) or neighbor_cost < nodes_cost[neighbor]:
                nodes_cost[neighbor] = neighbor_cost
                parent_trace[neighbor] = current_node
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    frontier.put((neighbor_cost + graph.heuristic(neighbor, finish), neighbor))