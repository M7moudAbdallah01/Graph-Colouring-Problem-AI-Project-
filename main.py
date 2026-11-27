from GUI.app import GraphColoringApp
from Algorithms.Backtracking import find_chromatic_number

# Example graph data for testing
# graph_data = {
#     "vertices": 3,
#     "edges": [(0, 1), (1, 2), (0, 2)],
#     "adjacency": {
#         0: {1, 2},
#         1: {0, 2},
#         2: {0, 1}
#     }
# }

def run_backtracking(graph_data, **params):

    graph = graph_data["adjacency"]

    stats = {}

    chromatic_number, coloring = find_chromatic_number(
        graph,
        ordering="original",
        stats=stats
    )

    success = coloring is not None

    return {
        "success": success,
        "colors": coloring if success else {},
        "chromatic_number": chromatic_number,
        "execution_time": 0.0,
        "statistics": {
            "nodes_visited": stats["nodes_visited"]
        }
    }


if __name__ == "__main__":

    app = GraphColoringApp()

    app.register_algorithm(
        "Backtracking Search",
        run_backtracking
    )

    app.mainloop()
