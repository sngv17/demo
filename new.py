from flask import Flask, render_template
import pandas as pd
import networkx as nx
import plotly.graph_objs as go

app = Flask(__name__)

# Sample data for table 1 and table 2
table1 = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

table2 = pd.DataFrame({
    'id': [1, 2, 4],
    'age': [25, 30, 22]
})

# Perform a join operation
joined_table = pd.merge(table1, table2, on='id', how='inner')

# Create a graph to represent the join operation
def create_join_graph(table1, table2, join_column):
    G = nx.DiGraph()

    # Add nodes for table1 and table2
    G.add_node("Table 1", type="table")
    G.add_node("Table 2", type="table")

    # Add edges for the join column
    G.add_edge("Table 1", "Table 2", label=f"Join on {join_column}")

    return G

# Generate Plotly visualization for the graph
def generate_graph_visualization(graph):
    pos = nx.spring_layout(graph)
    edge_trace = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'))

    node_trace = go.Scatter(
        x=[], y=[], text=[], mode='markers+text',
        hoverinfo='text', marker=dict(
            color=[], size=10, line=dict(width=2)))

    for node in graph.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)

    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return fig.to_html(full_html=False)

@app.route('/')
def index():
    graph = create_join_graph(table1, table2, 'id')
    graph_html = generate_graph_visualization(graph)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
