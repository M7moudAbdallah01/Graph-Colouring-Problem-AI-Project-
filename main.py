from GUI.app import GraphColoringApp


if __name__ == "__main__":

    app = GraphColoringApp()

    app.mainloop()



graph_data = {
    "vertices": 5,

    "edges": [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4)
    ],

    "adjacency": {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3]
    }
}