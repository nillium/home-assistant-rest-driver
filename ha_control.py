#!/usr/bin/env python3
"""
Quick Home Assistant Control Script
Usage examples:
  python3 ha_control.py list lights
  python3 ha_control.py turn_on light.bedroom
  python3 ha_control.py turn_off light.kitchen
  python3 ha_control.py status sensor.temperature
  python3 ha_control.py trigger automation.good_morning
"""

import sys
import os
from homeassistant_integration import HomeAssistantClient

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN', 'YOUR_TOKEN_HERE')

ha = HomeAssistantClient(HA_URL, ACCESS_TOKEN)

def list_devices(device_type):
    """List devices by type"""
    if device_type == 'lights':
        devices = ha.get_lights()
    elif device_type == 'switches':
        devices = ha.get_switches()
    elif device_type == 'sensors':
        devices = ha.get_sensors()
    else:
        print(f"Unknown device type: {device_type}")
        return
    
    for device in devices:
        state = device['state']
        name = device['attributes'].get('friendly_name', device['entity_id'])
        unit = device['attributes'].get('unit_of_measurement', '')
        print(f"  {device['entity_id']}: {state} {unit} - {name}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    try:
        if command == 'list' and len(sys.argv) >= 3:
            list_devices(sys.argv[2])
        
        elif command == 'turn_on' and len(sys.argv) >= 3:
            entity_id = sys.argv[2]
            ha.turn_on(entity_id)
            print(f"✓ Turned on {entity_id}")
        
        elif command == 'turn_off' and len(sys.argv) >= 3:
            entity_id = sys.argv[2]
            ha.turn_off(entity_id)
            print(f"✓ Turned off {entity_id}")
        
        elif command == 'toggle' and len(sys.argv) >= 3:
            entity_id = sys.argv[2]
            ha.toggle(entity_id)
            print(f"✓ Toggled {entity_id}")
        
        elif command == 'status' and len(sys.argv) >= 3:
            entity_id = sys.argv[2]
            state = ha.get_entity_state(entity_id)
            name = state['attributes'].get('friendly_name', entity_id)
            value = state['state']
            unit = state['attributes'].get('unit_of_measurement', '')
            print(f"{name}: {value} {unit}")
        
        elif command == 'trigger' and len(sys.argv) >= 3:
            entity_id = sys.argv[2]
            ha.trigger_automation(entity_id)
            print(f"✓ Triggered {entity_id}")
        
        else:
            print(__doc__)
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
