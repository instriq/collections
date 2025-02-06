#!/usr/bin/env python3

import json
from apify_client import ApifyClient

client = ApifyClient("")

def check_eligible_analysis(profile):
    run_input = { "usernames": [profile] }
    run       = client.actor("dSCLg0C3YEZ83HzYX").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print (item)

        # if item['postsCount'] == 0 and item['private']:
        #     return profile
   
    return 0


check_eligible_analysis("username")