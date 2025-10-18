#!/usr/bin/env python3
"""
Find and list all devices by type in Home Assistant
"""

import requests
import os
import sys
from collections import defaultdict

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def get_all_entities():
    """Get all entities grouped by domain"""
    response = requests.get(f"{HA_URL}/api/states", headers=headers)
    response.raise_for_status()
    entities = response.json()
    
    by_domain = defaultdict(list)
    for entity in entities:
        domain = entity['entity_id'].split('.')[0]
        by_domain[domain].append(entity)
    
    return by_domain

def find_by_keyword(keyword):
    """Find entities matching a keyword"""
    response = requests.get(f"{HA_URL}/api/states", headers=headers)
    response.raise_for_status()
    entities = response.json()
    
    matches = []
    for entity in entities:
        entity_id = entity['entity_id'].lower()
        friendly_name = entity['attributes'].get('friendly_name', '').lower()
        
        if keyword.lower() in entity_id or keyword.lower() in friendly_name:
            matches.append(entity)
    
    return matches

if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        print(f"Searching for '{keyword}'...\n")
        matches = find_by_keyword(keyword)
        
        if matches:
            for entity in matches:
                print(f"Entity: {entity['entity_id']}")
                print(f"  Name: {entity['attributes'].get('friendly_name')}")
                print(f"  State: {entity['state']}")
                print()
        else:
            print(f"No devices found matching '{keyword}'")
    else:
        print("All device types:\n")
        by_domain = get_all_entities()
        
        for domain in sorted(by_domain.keys()):
            count = len(by_domain[domain])
            print(f"{domain:20s} {count:3d} devices")
        
        print(f"\nUsage: {sys.argv[0]} <keyword>")
        print("Example: python3 find_devices.py doorbell")
