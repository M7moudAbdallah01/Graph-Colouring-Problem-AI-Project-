import math
import networkx as nx


def calculate_graph_positions(vertices, edges, width, height, node_radius=18):
    """Return centered NetworkX spring-layout coordinates within the canvas."""
    if vertices <= 0:
        return {}

    graph = nx.Graph()
    graph.add_nodes_from(range(vertices))
    graph.add_edges_from(edges)

    if vertices == 1:
        return {0: (width / 2, height / 2)}

    pad = max(node_radius + 24, 38)
    usable_w = max(30, width - 2 * pad)
    usable_h = max(30, height - 2 * pad)

    # spring_layout's k is the preferred distance between nodes in normalized space.
    k = 1.35 / math.sqrt(vertices)
    raw = nx.spring_layout(
        graph,
        k=k,
        iterations=300,
        seed=17,
        scale=1.0,
        weight=None
    )

    xs = [float(p[0]) for p in raw.values()]
    ys = [float(p[1]) for p in raw.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max(max_x - min_x, 1e-9)
    range_y = max(max_y - min_y, 1e-9)

    scale = min(usable_w / range_x, usable_h / range_y)
    center_x, center_y = width / 2, height / 2

    positions = {}
    for vertex, point in raw.items():
        positions[vertex] = [
            center_x + (float(point[0]) - (min_x + max_x) / 2) * scale,
            center_y + (float(point[1]) - (min_y + max_y) / 2) * scale
        ]

    # Light collision relaxation. Keep nodes inside the drawing area.
    min_distance = max(node_radius * 2.35, 28)
    left, right = pad, max(pad, width - pad)
    top, bottom = pad, max(pad, height - pad)

    for _ in range(180):
        moved = False
        for i, u in enumerate(range(vertices)):
            for v in range(i + 1, vertices):
                dx = positions[v][0] - positions[u][0]
                dy = positions[v][1] - positions[u][1]
                distance = math.hypot(dx, dy)
                if distance < min_distance:
                    if distance < 1e-8:
                        angle = (u + v + 1) * 2.399963
                        dx, dy, distance = math.cos(angle), math.sin(angle), 1.0
                    ux, uy = dx / distance, dy / distance
                    push = (min_distance - distance) * 0.26
                    positions[u][0] -= ux * push
                    positions[u][1] -= uy * push
                    positions[v][0] += ux * push
                    positions[v][1] += uy * push
                    moved = True

        for vertex in positions:
            positions[vertex][0] = min(max(positions[vertex][0], left), right)
            positions[vertex][1] = min(max(positions[vertex][1], top), bottom)

        if not moved:
            break

    return {v: (p[0], p[1]) for v, p in positions.items()}
