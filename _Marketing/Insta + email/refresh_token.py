#!/usr/bin/env python3
"""
Exchanges a short-lived Meta token for a 60-day long-lived token
and saves it automatically to your .env file.

Run this whenever your token expires (every ~60 days).

Usage:
    python3 refresh_token.py
"""

import os
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("  Meta Token Refresher")
print("=" * 50)
print()
print("You need two things from your Meta Developer app:")
print("  developers.facebook.com > Safari Coaching Newsletter > App Settings > Basic")
print()

app_id     = input("Paste your App ID: ").strip()
app_secret = input("Paste your App Secret: ").strip()

print()
print("Now go to: developers.facebook.com > Tools > Graph API Explorer")
print("Generate a short-lived token with these permissions:")
print("  - instagram_basic")
print("  - pages_read_engagement")
print("  - pages_show_list")
print()

short_token = input("Paste your short-lived token: ").strip()
print()

# Exchange for long-lived token
print("Exchanging for 60-day token...")
resp = requests.get(
    "https://graph.facebook.com/v19.0/oauth/access_token",
    params={
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }
)

data = resp.json()

if "error" in data:
    print(f"Error: {data['error']['message']}")
    exit(1)

long_token = data.get("access_token")
expires_in = data.get("expires_in", 5184000)  # default 60 days
expires_date = datetime.now() + timedelta(seconds=expires_in)

print(f"Success! Token valid until: {expires_date.strftime('%B %d, %Y')}")

# Update .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")

if not os.path.exists(env_path):
    print("\n⚠️  No .env file found.")
    print("Please run setup.py first to create your credentials file:")
    print("  python3 setup.py")
    print("\nYour new token is:")
    print(f"  {long_token}")
    print("Copy it — you'll need to paste it when setup.py asks for your Meta access token.")
    exit(0)

with open(env_path, "r") as f:
    env_contents = f.read()

# Replace the token
env_contents = re.sub(
    r"META_ACCESS_TOKEN=.*",
    f"META_ACCESS_TOKEN={long_token}",
    env_contents
)

# Add or update expiry comment
if "# Token expires:" in env_contents:
    env_contents = re.sub(
        r"# Token expires:.*",
        f"# Token expires: {expires_date.strftime('%B %d, %Y')} — run refresh_token.py to renew",
        env_contents
    )
else:
    env_contents = env_contents.replace(
        f"META_ACCESS_TOKEN={long_token}",
        f"META_ACCESS_TOKEN={long_token}\n# Token expires: {expires_date.strftime('%B %d, %Y')} — run refresh_token.py to renew"
    )

with open(env_path, "w") as f:
    f.write(env_contents)

print()
print(f"Token saved to .env file.")
print(f"Set a reminder to run python3 refresh_token.py again on {expires_date.strftime('%B %d, %Y')}.")
