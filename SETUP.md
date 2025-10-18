# Home Assistant Integration Setup Guide

Complete guide for setting up the Home Assistant REST API Python driver.

## Prerequisites

✅ Home Assistant instance running
✅ Network access to Home Assistant
✅ Python 3.7 or higher
✅ pip package manager

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/nillium/home-assistant-rest-driver.git
cd home-assistant-rest-driver
```

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Generate Access Token

1. Open your Home Assistant web interface
2. Click on your **profile** (bottom left)
3. Scroll to **Long-Lived Access Tokens**
4. Click **Create Token**
5. Give it a name (e.g., "Python API Client")
6. **Copy the token** - you won't see it again!

### 4. Configure Environment

**Option A: Environment Variables (Recommended)**

```bash
export HA_URL="http://your-ha-ip:8123"
export HA_TOKEN="your_long_lived_access_token"
```

Or create a `.env` file:
```
HA_URL=http://your-ha-ip:8123
HA_TOKEN=your_long_lived_access_token
```

**Option B: Direct Configuration**

Edit the scripts and replace:
```python
HA_URL = "http://your-ha-ip:8123"
ACCESS_TOKEN = "your_token_here"
```

### 5. Test Connection

```bash
python3 homeassistant_integration.py
```

You should see a list of your devices!

## Usage Examples

### Python Script

```python
from homeassistant_integration import HomeAssistantClient

ha = HomeAssistantClient(
    "http://192.168.1.100:8123",
    "your_token"
)

# List all lights
for light in ha.get_lights():
    print(f"{light['entity_id']}: {light['state']}")

# Control a light
ha.turn_on("light.living_room", brightness=255)
ha.turn_off("light.bedroom")

# Get sensor data
temp = ha.get_entity_state("sensor.temperature")
print(f"Temperature: {temp['state']}°C")
```

### Command Line

```bash
# List devices
python3 ha_control.py list lights
python3 ha_control.py list switches
python3 ha_control.py list sensors

# Control devices
python3 ha_control.py turn_on light.kitchen
python3 ha_control.py turn_off switch.fan
python3 ha_control.py toggle light.bedroom

# Check status
python3 ha_control.py status sensor.temperature
python3 ha_control.py status light.living_room

# Trigger automation
python3 ha_control.py trigger automation.good_morning
```

## Tailscale Setup (Optional)

For secure remote access:

1. Install Tailscale on your Home Assistant machine
2. Install Tailscale on client machines
3. Use Tailscale IP in configuration:
   ```python
   HA_URL = "http://100.x.x.x:8123"  # Tailscale IP
   ```
4. Access from anywhere securely!

## Security Best Practices

⚠️ **Important Security Tips:**

1. **Never commit tokens to Git**
   - Add `.env` to `.gitignore`
   - Use environment variables

2. **Use HTTPS when possible**
   ```python
   HA_URL = "https://your-domain.com:8123"
   ```

3. **Restrict token permissions**
   - Create separate tokens for different purposes
   - Revoke tokens when not needed

4. **Use Tailscale for remote access**
   - More secure than port forwarding
   - No need to expose Home Assistant to internet

## Troubleshooting

### Connection Refused
```
requests.exceptions.ConnectionError
```
**Solution:**
- Check Home Assistant is running
- Verify IP address and port
- Check firewall settings

### 401 Unauthorized
```
requests.exceptions.HTTPError: 401
```
**Solution:**
- Verify access token is correct
- Generate a new token if expired
- Check token hasn't been revoked

### 404 Not Found
```
requests.exceptions.HTTPError: 404
```
**Solution:**
- Check entity ID exists
- Use `ha.get_states()` to list all entities
- Verify entity ID spelling

### Import Error
```
ModuleNotFoundError: No module named 'requests'
```
**Solution:**
```bash
pip install requests
```

## Next Steps

- 📚 Read `EXAMPLES.md` for more usage examples
- 🔔 Set up doorbell automation
- 🤖 Integrate with AI assistant
- 📈 Build monitoring dashboards

## Support

For issues or questions:
- Open an issue on GitHub
- Check Home Assistant documentation
- Visit Home Assistant community forum
