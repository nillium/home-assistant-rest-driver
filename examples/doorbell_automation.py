#!/usr/bin/env python3
"""
Create Doorbell to Sonos Automation
Plays a sound on Sonos when doorbell button is pressed
"""

import requests
import os

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

automation_config = {
    "alias": "Doorbell Ring - Play Sound on Sonos",
    "description": "Play a doorbell sound on Sonos when someone rings",
    "trigger": [
        {
            "platform": "state",
            "entity_id": "binary_sensor.doorbell_visitor",
            "to": "on"
        }
    ],
    "condition": [],
    "action": [
        {
            "service": "media_player.volume_set",
            "target": {"entity_id": "media_player.sonos"},
            "data": {"volume_level": 0.5}
        },
        {
            "service": "media_player.play_media",
            "target": {"entity_id": "media_player.sonos"},
            "data": {
                "media_content_id": "https://www.soundjay.com/door/sounds/doorbell-1.mp3",
                "media_content_type": "music"
            }
        },
        {
            "service": "notify.persistent_notification",
            "data": {
                "title": "🔔 Doorbell",
                "message": "Someone is at the door!"
            }
        }
    ],
    "mode": "single"
}

print("Creating doorbell automation...")
response = requests.post(
    f"{HA_URL}/api/config/automation/config/doorbell_sonos",
    headers=headers,
    json=automation_config
)

if response.status_code in [200, 201]:
    print("✓ Automation created successfully!")
    print(f"\nEdit in Home Assistant to customize:")
    print(f"  - Change media_player entity")
    print(f"  - Change doorbell sound URL")
    print(f"  - Adjust volume level")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
