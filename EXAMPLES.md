# Usage Examples

Comprehensive examples for using the Home Assistant REST API driver.

## Basic Device Control

### Lights

```python
from homeassistant_integration import HomeAssistantClient

ha = HomeAssistantClient("http://192.168.1.100:8123", "YOUR_TOKEN")

# Turn on with brightness
ha.turn_on("light.living_room", brightness=255)

# Turn on with color
ha.turn_on("light.bedroom", brightness=200, rgb_color=[255, 0, 0])  # Red

# Turn off
ha.turn_off("light.kitchen")

# Toggle
ha.toggle("light.hallway")
```

### Switches

```python
# Turn on switch
ha.turn_on("switch.coffee_maker")

# Turn off switch
ha.turn_off("switch.fan")

# Toggle switch
ha.toggle("switch.lamp")
```

### Climate Control

```python
# Set temperature
ha.call_service("climate", "set_temperature", "climate.thermostat",
                temperature=22, hvac_mode="heat")

# Set fan mode
ha.call_service("climate", "set_fan_mode", "climate.thermostat",
                fan_mode="auto")
```

## Querying States

### Get All Devices

```python
# Get all states
all_states = ha.get_states()

# Filter by domain
lights = ha.get_lights()
switches = ha.get_switches()
sensors = ha.get_sensors()

# Print device info
for light in lights:
    print(f"{light['entity_id']}: {light['state']}")
    print(f"  Brightness: {light['attributes'].get('brightness', 'N/A')}")
    print(f"  Friendly name: {light['attributes'].get('friendly_name')}")
```

### Get Specific Entity

```python
# Get sensor state
temp = ha.get_entity_state("sensor.living_room_temperature")
print(f"Temperature: {temp['state']}{temp['attributes']['unit_of_measurement']}")

# Get light state
light = ha.get_entity_state("light.bedroom")
print(f"Light is {light['state']}")
if light['state'] == 'on':
    print(f"Brightness: {light['attributes']['brightness']}")
```

## Automations

### Trigger Automation

```python
# Trigger existing automation
ha.trigger_automation("automation.good_morning")

# Or use call_service directly
ha.call_service("automation", "trigger", "automation.goodnight")
```

### Create Automation via API

```python
import requests

automation = {
    "alias": "Lights on at sunset",
    "trigger": [{"platform": "sun", "event": "sunset"}],
    "action": [{"service": "light.turn_on", "entity_id": "light.living_room"}]
}

response = requests.post(
    f"{ha.base_url}/api/config/automation/config/lights_sunset",
    headers=ha.headers,
    json=automation
)
```

## Media Players

### Sonos Control

```python
# Play media
ha.call_service("media_player", "play_media", "media_player.sonos",
                media_content_id="https://example.com/song.mp3",
                media_content_type="music")

# Set volume
ha.call_service("media_player", "volume_set", "media_player.sonos",
                volume_level=0.5)  # 50%

# Play/Pause
ha.call_service("media_player", "media_play", "media_player.sonos")
ha.call_service("media_player", "media_pause", "media_player.sonos")

# Next/Previous
ha.call_service("media_player", "media_next_track", "media_player.sonos")
ha.call_service("media_player", "media_previous_track", "media_player.sonos")
```

## Notifications

### Send Notification

```python
# Simple notification
ha.send_notification("Hello from Python!")

# With title
ha.send_notification("Door is open", title="Security Alert")

# To specific service
ha.send_notification("Test message", target="mobile_app_iphone")
```

## Advanced Examples

### Batch Operations

```python
# Turn on all lights
for light in ha.get_lights():
    if light['state'] == 'off':
        ha.turn_on(light['entity_id'])

# Turn off all switches
for switch in ha.get_switches():
    if switch['state'] == 'on':
        ha.turn_off(switch['entity_id'])
```

### Conditional Control

```python
# Turn on lights if dark
sun_state = ha.get_entity_state("sun.sun")
if sun_state['state'] == 'below_horizon':
    ha.turn_on("light.living_room")

# Adjust thermostat based on temperature
temp = float(ha.get_entity_state("sensor.temperature")['state'])
if temp < 20:
    ha.call_service("climate", "set_temperature", "climate.thermostat",
                    temperature=22)
```

### Doorbell Automation

```python
# Check doorbell state
doorbell = ha.get_entity_state("binary_sensor.doorbell")
if doorbell['state'] == 'on':
    # Play sound on Sonos
    ha.call_service("media_player", "play_media", "media_player.sonos",
                    media_content_id="/local/doorbell.mp3",
                    media_content_type="music")
    # Send notification
    ha.send_notification("Someone is at the door!", title="Doorbell")
```

### Scene Control

```python
# Activate scene
ha.call_service("scene", "turn_on", "scene.movie_time")

# Create dynamic scene
ha.call_service("scene", "turn_on", "scene.cozy_evening")
```

## Error Handling

```python
try:
    ha.turn_on("light.living_room")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Entity not found")
    elif e.response.status_code == 401:
        print("Unauthorized - check your token")
    else:
        print(f"Error: {e}")
except requests.exceptions.ConnectionError:
    print("Cannot connect to Home Assistant")
```

## Integration with Other Services

### With AI Assistant

```python
def process_command(command: str):
    """Process natural language commands"""
    command = command.lower()
    
    if "turn on" in command and "light" in command:
        # Extract room from command
        for light in ha.get_lights():
            if any(room in light['entity_id'] for room in ["living", "bedroom", "kitchen"]):
                ha.turn_on(light['entity_id'])
                return f"Turned on {light['attributes']['friendly_name']}"
    
    elif "temperature" in command:
        temp = ha.get_entity_state("sensor.temperature")
        return f"Temperature is {temp['state']}°C"
```

### With Scheduling

```python
import schedule
import time

def morning_routine():
    ha.turn_on("light.bedroom", brightness=50)
    ha.call_service("climate", "set_temperature", "climate.thermostat",
                    temperature=21)
    ha.send_notification("Good morning!")

schedule.every().day.at("07:00").do(morning_routine)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Command Line Examples

```bash
# List all devices
python3 ha_control.py list lights
python3 ha_control.py list switches
python3 ha_control.py list sensors

# Control devices
python3 ha_control.py turn_on light.living_room
python3 ha_control.py turn_off switch.fan
python3 ha_control.py toggle light.bedroom

# Check status
python3 ha_control.py status sensor.temperature
python3 ha_control.py status light.kitchen

# Trigger automations
python3 ha_control.py trigger automation.good_morning
```
