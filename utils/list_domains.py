#!/usr/bin/env python3
"""
List all available domains (device types) in Home Assistant
"""

import requests
import os
from collections import Counter

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(f"{HA_URL}/api/states", headers=headers)
response.raise_for_status()

entities = response.json()
domains = Counter(entity['entity_id'].split('.')[0] for entity in entities)

print(f"Found {len(entities)} total entities across {len(domains)} domains:\n")
print(f"{'Domain':<25} {'Count':>6}  Description")
print("-" * 70)

domain_descriptions = {
    'light': 'Lights and bulbs',
    'switch': 'Switches and outlets',
    'sensor': 'Sensors (temperature, humidity, etc)',
    'binary_sensor': 'Binary sensors (motion, door, etc)',
    'media_player': 'Media players (Sonos, TV, etc)',
    'climate': 'Climate control (thermostats)',
    'camera': 'Cameras',
    'automation': 'Automations',
    'script': 'Scripts',
    'scene': 'Scenes',
    'person': 'People/presence tracking',
    'device_tracker': 'Device tracking',
    'sun': 'Sun position',
    'weather': 'Weather information',
    'zone': 'Geographic zones',
    'input_boolean': 'Input helpers (boolean)',
    'input_number': 'Input helpers (number)',
    'input_select': 'Input helpers (select)',
    'input_text': 'Input helpers (text)',
    'cover': 'Covers (blinds, garage doors)',
    'lock': 'Locks',
    'fan': 'Fans',
    'vacuum': 'Vacuum cleaners',
}

for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
    desc = domain_descriptions.get(domain, '')
    print(f"{domain:<25} {count:>6}  {desc}")
