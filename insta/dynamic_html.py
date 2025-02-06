#!/usr/bin/env python3

import webbrowser
from apify_client import ApifyClient
import networkx as nx
import matplotlib.pyplot as plt
import mpld3

def explore_users(username, owner_username_count, G, explored_users, depth=1, max_depth=2):
    if depth > max_depth or username in explored_users:
        return
    
    explored_users.add(username)

    print(f"Exploring {username} with 10 posts")

    run_input = {
        "username": [username],
        "resultsLimit": 5,
    }

    run = client.actor("nH2AHrwxeTRJoN5hX").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if 'mentions' in item:
            for mention in item['mentions']:
                owner_username = mention
                owner_username_count[owner_username] = owner_username_count.get(mention, 0) + 1

        if 'taggedUsers' in item:
            for user in item['taggedUsers']:
                owner_username = user['username']
                owner_username_count[owner_username] = owner_username_count.get(user['username'], 0) + 1

        if 'latestComments' in item:
            for comment in item['latestComments']:
                if comment['ownerUsername'] != username:
                    owner_username = comment['ownerUsername']
                    owner_username_count[owner_username] = owner_username_count.get(owner_username, 0) + 1
                    
                    if owner_username not in G.nodes:
                        G.add_node(owner_username, count=owner_username_count.get(owner_username, 0), size=owner_username_count.get(owner_username, 0))
                    
                    G.add_edge(username, owner_username)

                    explore_users(owner_username, owner_username_count, G, explored_users, depth=depth+1, max_depth=max_depth)
                    
                    generate_html(G, explored_users)

def generate_html(G, explored_users):
    isolated_nodes = [node for node in G.nodes() if node not in explored_users]
    G_copy = G.copy()
    G_copy.remove_nodes_from(isolated_nodes)

    pos = nx.spring_layout(G_copy)

    for node in G_copy.nodes():
        if 'count' not in G_copy.nodes[node]:
            G_copy.nodes[node]['count'] = 0

    node_sizes = [data['count'] * 550 for node, data in G_copy.nodes(data=True)]

    fig, ax = plt.subplots()
    nx.draw(G_copy, pos, with_labels=True, node_size=node_sizes, font_size=12, font_weight='bold', ax=ax)

    for edge in G_copy.edges():
        nx.draw_networkx_edges(G_copy, pos, edgelist=[edge], edge_color=edge_color(G_copy, edge[0], edge[1]), ax=ax)

    node_labels = {node: data['count'] for node, data in G_copy.nodes(data=True)}
    nx.draw_networkx_labels(G_copy, pos, labels=node_labels)

    mpld3.save_html(fig, "graph.html")
    plt.close(fig)  # Fecha a figura para evitar vazamento de memória

    # Abrir o HTML no navegador padrão
    webbrowser.open_new_tab("graph.html")

def edge_color(G, node_A, node_B):
    if G.has_edge(node_A, node_B) or G.has_edge(node_B, node_A):
        return 'blue'
    elif any(nx.has_path(G, node_A, node) and nx.has_path(G, node, node_B) for node in G.nodes() if node != node_A and node != node_B):
        return 'purple'
    else:
        return 'black'

client = ApifyClient("") # 

username = "username"
owner_username_count = {}

G = nx.Graph()
explored_users = set()
explore_users(username, owner_username_count, G, explored_users, max_depth=2)
generate_html(G, explored_users)