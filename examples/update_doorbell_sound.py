#!/usr/bin/env python3
"""
Update Doorbell Sound URL
Usage: python3 update_doorbell_sound.py [URL]
"""

import sys
import requests
import os

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

# Preset doorbell sounds
PRESET_SOUNDS = {
    "1": "https://www.soundjay.com/misc/sounds/doorbell-1.mp3",
    "2": "https://www.soundjay.com/misc/sounds/doorbell-chime-1.mp3",
    "3": "https://www.soundjay.com/misc/sounds/bell-ringing-01.mp3",
    "4": "https://www.soundjay.com/misc/sounds/wind-chimes-1.mp3",
}

def update_automation(media_url):
    automation_config = {
        "alias": "Doorbell Ring - Play Sound on Sonos",
        "trigger": [{"platform": "state", "entity_id": "binary_sensor.doorbell_visitor", "to": "on"}],
        "action": [
            {"service": "media_player.volume_set", "target": {"entity_id": "media_player.sonos"}, "data": {"volume_level": 0.5}},
            {"service": "media_player.play_media", "target": {"entity_id": "media_player.sonos"}, "data": {"media_content_id": media_url, "media_content_type": "music"}},
        ],
        "mode": "single"
    }
    
    response = requests.post(
        f"{HA_URL}/api/config/automation/config/doorbell_sonos",
        headers=headers,
        json=automation_config
    )
    return response.status_code in [200, 201]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Choose a preset sound or enter URL:")
        for k, v in PRESET_SOUNDS.items():
            print(f"  {k}. {v}")
        print("  5. Enter custom URL")
        choice = input("Choice: ").strip()
        
        if choice in PRESET_SOUNDS:
            url = PRESET_SOUNDS[choice]
        elif choice == "5":
            url = input("Enter URL: ").strip()
        else:
            print("Invalid choice")
            sys.exit(1)
    
    print(f"Updating doorbell sound to: {url}")
    if update_automation(url):
        print("✓ Updated successfully!")
        requests.post(f"{HA_URL}/api/services/automation/reload", headers=headers)
        print("✓ Automations reloaded")
    else:
        print("❌ Failed to update")
