from apify_client import ApifyClient

client = ApifyClient("")
username = "username"

run_input = {
    "username": [username],
    "resultsLimit": 43,
}

run = client.actor("nH2AHrwxeTRJoN5hX").call(run_input=run_input)

owner_username_count = {}

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    if 'timestamp' in item:
        print(item['timestamp'])

    if 'locationName' in item:
        print(item['locationName'])

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

for owner_username, count in owner_username_count.items():
    print(f"{owner_username}: {count}")