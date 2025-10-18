#!/usr/bin/env python3
"""
Test Home Assistant connection and authentication
"""

import requests
import os
import sys

HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')
ACCESS_TOKEN = os.getenv('HA_TOKEN')

def test_connection():
    """Test basic connectivity and authentication"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    print(f"Testing connection to {HA_URL}...")
    
    # Test API endpoint
    try:
        response = requests.get(f"{HA_URL}/api/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Connection successful")
            data = response.json()
            print(f"  Message: {data.get('message')}")
        else:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {HA_URL}")
        print("  Check that Home Assistant is running and accessible")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout")
        return False
    
    # Test authentication
    try:
        response = requests.get(f"{HA_URL}/api/states", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Authentication successful")
            states = response.json()
            print(f"  Found {len(states)} entities")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed")
            print("  Check your access token")
            return False
        else:
            print(f"❌ API error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        print("Error: HA_TOKEN environment variable not set")
        print("\nSet it with:")
        print("  export HA_TOKEN='your_token_here'")
        sys.exit(1)
    
    success = test_connection()
    sys.exit(0 if success else 1)
