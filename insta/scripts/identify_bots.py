#!/usr/bin/env python3

import json
import networkx as nx
from apify_client import ApifyClient

client = ApifyClient("")

def check_eligible_analysis(profile):
    run_input = { "usernames": [profile] }
    run       = client.actor("dSCLg0C3YEZ83HzYX").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if not item['verified']:
            if item['postsCount'] > 0 and not item['private']:
                return profile
            
            # if item['followersCount'] == 1 or item['followsCount'] == 1:
            #     return profile
           
    return 0


def explore_users(username, owner_username_count, G, depth=1, max_depth=1):
    if depth > max_depth:
        return
    
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
    neighbors = list(G.neighbors(username))
    subgraph = G.subgraph(neighbors)
    
    direct_connection_groups = list(nx.connected_components(subgraph))
    group_count = len(direct_connection_groups)
    
    print(f"Total de grupos diretamente conectados ao usuário '{username}': {group_count}")
    return group_count


with open('./users.json', 'r') as arquivo:
    dados = json.load(arquivo)

for item in dados:
    elegible = check_eligible_analysis(item['ID'])

    if elegible:
        print (f"Starting analysis for {item['ID']}")
        
        owner_username_count = {}

        G = nx.Graph()

        explore_users(item['ID'], owner_username_count, G, max_depth=1)
        count_direct_connection_groups(G, item['ID'])