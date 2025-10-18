# Home Assistant REST API Driver

🏠 A comprehensive Python REST API driver for Home Assistant with device control, automation management, and integration scripts.

## Features

- ✅ **Complete REST API Wrapper** - Full Python client for Home Assistant REST API
- 🎮 **Device Control** - Control lights, switches, sensors, and more
- 🤖 **Automation Management** - Create, trigger, and manage automations
- 🔔 **Doorbell Integration** - Automatic doorbell sound on Sonos when visitor detected
- 📱 **Tailscale Ready** - Secure remote access via Tailscale VPN
- 🎵 **Media Player Control** - Control Sonos and other media players
- 📝 **CLI Tools** - Command-line scripts for quick device control

## Installation

```bash
pip install requests
```

## Quick Start

### 1. Get Your Access Token

1. Open Home Assistant
2. Go to your Profile → Long-Lived Access Tokens
3. Create a new token
4. Copy the token

### 2. Basic Usage

```python
from homeassistant_integration import HomeAssistantClient

# Initialize client
ha = HomeAssistantClient(
    base_url="http://your-ha-ip:8123",
    access_token="YOUR_TOKEN_HERE"
)

# Control lights
ha.turn_on("light.living_room", brightness=255)
ha.turn_off("light.bedroom")

# Get sensor data
temp = ha.get_entity_state("sensor.temperature")
print(f"Temperature: {temp['state']}°C")

# Trigger automation
ha.trigger_automation("automation.good_morning")
```

### 3. Command-Line Usage

```bash
# List all lights
python3 ha_control.py list lights

# Turn on a light
python3 ha_control.py turn_on light.kitchen

# Check sensor status
python3 ha_control.py status sensor.temperature

# Trigger automation
python3 ha_control.py trigger automation.good_morning
```

## Files Included

### Core Library
- **`homeassistant_integration.py`** - Main REST API client library
- **`ha_control.py`** - Command-line control tool

### Automation Scripts
- **`create_doorbell_automation.py`** - Create doorbell-to-Sonos automation
- **`update_doorbell_sound.py`** - Change doorbell sound easily
- **`test_doorbell_automation.py`** - Test doorbell automation

### Utility Scripts
- **`find_doorbell.py`** - Find doorbell devices
- **`find_cosmo.py`** - Find Sonos devices
- **`test_ha.py`** - Test all device types

### Documentation
- **`SETUP.md`** - Detailed setup guide
- **`EXAMPLES.md`** - Usage examples
- **`DOORBELL_CUSTOMIZATION.md`** - Doorbell sound customization guide

## API Reference

### HomeAssistantClient Class

#### Device Control
```python
ha.turn_on(entity_id, **kwargs)  # Turn on device
ha.turn_off(entity_id)            # Turn off device
ha.toggle(entity_id)              # Toggle device
```

#### Query States
```python
ha.get_states()                   # Get all entities
ha.get_entity_state(entity_id)    # Get specific entity
ha.get_lights()                   # Get all lights
ha.get_switches()                 # Get all switches
ha.get_sensors()                  # Get all sensors
```

#### Automations
```python
ha.trigger_automation(entity_id)  # Trigger automation
ha.call_service(domain, service, entity_id, **kwargs)  # Call any service
```

#### Notifications
```python
ha.send_notification(message, title=None, target="notify")
```

## Example: Doorbell Automation

Create an automation that plays a doorbell sound on your Sonos when someone rings:

```python
python3 create_doorbell_automation.py
```

Customize the sound:
```python
python3 update_doorbell_sound.py https://example.com/doorbell.mp3
```

## Configuration

**Security Best Practices:**
- Never commit your access token to Git
- Use environment variables: `os.getenv('HA_TOKEN')`
- Store tokens in a secure config file
- Use Tailscale for secure remote access

```python
import os

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

ha = HomeAssistantClient(HA_URL, ACCESS_TOKEN)
```

## Tailscale Integration

For secure remote access:
1. Install Tailscale on your Home Assistant server
2. Connect via Tailscale IP (e.g., `http://100.x.x.x:8123`)
3. Access from anywhere securely

## Use Cases

- 🤖 **AI Assistant Integration** - Control home via voice/chat
- 📱 **Remote Control** - Control home from anywhere via Tailscale
- 🔔 **Smart Doorbell** - Play custom sounds when doorbell rings
- 📊 **Monitoring** - Track sensor data and device states
- ⚡ **Automation** - Create complex automations programmatically

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT License - Feel free to use in your projects!

## Author

Created with ❤️ for the Home Assistant community

## Links

- [Home Assistant Documentation](https://www.home-assistant.io/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Tailscale](https://tailscale.com/)