#!/usr/bin/env python3
"""
Run this script to find your Instagram Business Account ID and save it automatically.

Usage:
    python3 get_ig_id.py
"""

import os
import requests

print("=" * 50)
print("  Instagram Setup")
print("=" * 50)
print()
print("Paste the short-lived token from Graph API Explorer.")
print("(Use the token straight from Graph API Explorer, before running refresh_token.py)")
print()

token = input("Paste your access token here: ").strip()
print()

ig_id = None

# Step 1: Try /me/accounts (works for direct page admins)
resp = requests.get(
    "https://graph.facebook.com/v19.0/me/accounts",
    params={"access_token": token}
)
pages = resp.json()

if pages.get("data"):
    for page in pages["data"]:
        ig = requests.get(
            f"https://graph.facebook.com/v19.0/{page['id']}",
            params={
                "fields": "instagram_business_account",
                "access_token": page["access_token"]
            }
        ).json()
        ig_id = ig.get("instagram_business_account", {}).get("id")
        if ig_id:
            print(f"Found: {page['name']} -> Instagram ID: {ig_id}")
            break

# Step 2: Fallback — ask for Facebook Page ID directly
# (needed when access is through Business Manager)
if not ig_id:
    print("Couldn't find your Instagram account automatically.")
    print("This is normal if your page is managed through Business Manager.")
    print()
    print("To find your Facebook Page ID:")
    print("  1. Go to your Facebook Page")
    print("  2. Click 'About' in the left menu")
    print("  3. Scroll to the bottom — you'll see a number labelled 'Page ID'")
    print()
    page_id = input("Enter your Facebook Page ID: ").strip()

    ig = requests.get(
        f"https://graph.facebook.com/v19.0/{page_id}",
        params={
            "fields": "instagram_business_account",
            "access_token": token
        }
    ).json()

    if "error" in ig:
        print(f"Error: {ig['error']['message']}")
        exit(1)

    ig_id = ig.get("instagram_business_account", {}).get("id")

    if not ig_id:
        print("No Instagram Business Account found linked to that page.")
        print("Make sure your Instagram is set to Professional and linked to the Facebook Page.")
        exit(1)

    print(f"Found Instagram ID: {ig_id}")

# Step 3: Save to .env
env_path = os.path.join(os.path.dirname(__file__), ".env")

if not os.path.exists(env_path):
    print(f"\nNo .env file found. Run setup.py first.")
    print(f"\nYour Instagram User ID is: {ig_id}")
    print("Copy it — you'll need it when setup.py asks.")
    exit(0)

with open(env_path, "r") as f:
    env_contents = f.read()

import re
env_contents = re.sub(r"IG_USER_ID=.*", f"IG_USER_ID={ig_id}", env_contents)
if "IG_USER_ID=" not in env_contents:
    env_contents += f"\nIG_USER_ID={ig_id}"

with open(env_path, "w") as f:
    f.write(env_contents)

print()
print("Done! Your Instagram User ID has been saved.")
print("Now run: python3 refresh_token.py")
