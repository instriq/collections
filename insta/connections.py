#!/usr/bin/env python3

from apify_client import ApifyClient
import networkx as nx

def explore_users(username, owner_username_count, G, depth=1, max_depth=1):
    if depth > max_depth:
        return
    
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

                G.add_node(owner_username)
                G.add_edge(username, owner_username)

        if 'taggedUsers' in item:
            for user in item['taggedUsers']:
                owner_username = user['username']
                owner_username_count[owner_username] = owner_username_count.get(user['username'], 0) + 1

                G.add_node(owner_username)
                G.add_edge(username, owner_username)

        if 'latestComments' in item:
            for comment in item['latestComments']:
                if comment['ownerUsername'] != username:
                    owner_username = comment['ownerUsername']
                    owner_username_count[owner_username] = owner_username_count.get(owner_username, 0) + 1

                    G.add_node(owner_username)
                    G.add_edge(username, owner_username)

def count_direct_connection_groups(G, username):
    # Encontra todos os nós diretamente conectados ao usuário analisado
    neighbors = list(G.neighbors(username))
    
    # Cria um subgrafo apenas com as conexões diretas do usuário
    subgraph = G.subgraph(neighbors)
    
    # Calcula os componentes conectados no subgrafo
    direct_connection_groups = list(nx.connected_components(subgraph))
    group_count = len(direct_connection_groups)
    print(f"Total de grupos diretamente conectados ao usuário '{username}': {group_count}")
    return group_count

client = ApifyClient("") # Substitua pela sua chave de API

username = "username"
owner_username_count = {}

G = nx.Graph()

# Explora as conexões do usuário (apenas conexões diretas devido ao max_depth=1)
explore_users(username, owner_username_count, G, max_depth=1)

# Conta e imprime a quantidade de grupos diretamente conectados ao usuário
count_direct_connection_groups(G, username)