import time


def is_safe(graph, vertex, color, coloring):
    for neighbor in graph[vertex]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False

    return True

def backtracking_coloring(graph, k, ordering="original", stats=None):
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("Number of colors must be a positive integer.")

    vertices = order_vertices(graph, ordering)
    coloring = {}

    if stats is not None:
        stats["nodes_visited"] = 0

    def backtrack(index):
        if stats is not None:
            stats["nodes_visited"] += 1

        if index == len(vertices):
            return True

        vertex = vertices[index]

        for color in range(k):
            if is_safe(graph, vertex, color, coloring):
                coloring[vertex] = color

                if backtrack(index + 1):
                    return True

                del coloring[vertex]

        return False

    if backtrack(0):
        return coloring.copy()

    return None




def find_chromatic_number(graph, ordering="original", stats=None):
    vertices = list(graph.keys())

    if not vertices:
        if stats is not None:
            stats["nodes_visited"] = 0
        return 0, {}

    total_nodes = 0

    for k in range(1, len(vertices) + 1):
        attempt_stats = {}

        coloring = backtracking_coloring(
            graph,
            k,
            ordering=ordering,
            stats=attempt_stats
        )

        total_nodes += attempt_stats["nodes_visited"]

        if coloring is not None:
            if stats is not None:
                stats["nodes_visited"] = total_nodes

            return k, coloring

    if stats is not None:
        stats["nodes_visited"] = total_nodes

    return None, None


def order_vertices(graph, ordering="original"):
    vertices = list(graph.keys())

    if ordering == "original":
        return vertices

    if ordering == "degree":
        return sorted(
            vertices,
            key=lambda vertex: len(graph[vertex]),
            reverse=True
        )

    raise ValueError(f"Unknown ordering strategy: {ordering}")


if __name__ == "__main__":
    graph = {
        "A": {"B"},
        "B": {"A", "C", "D", "E"},
        "C": {"B", "D"},
        "D": {"B", "C", "E"},
        "E": {"B", "D"}
    }

    for ordering in ["original", "degree"]:
        stats = {}

        start_time = time.perf_counter()

        chromatic_number, coloring = find_chromatic_number(
            graph,
            ordering=ordering,
            stats=stats
        )

        end_time = time.perf_counter()

        execution_time = end_time - start_time

        print(f"\nOrdering: {ordering}")
        print("Chromatic Number:", chromatic_number)
        print("Coloring:", coloring)
        print("Nodes Visited:", stats["nodes_visited"])
        print(f"Execution Time: {execution_time:.6f} seconds")