#!/usr/bin/env python3
"""
Run this once to set up your newsletter automation.

Usage:
    python3 setup.py
"""

import os
import re
import requests
from datetime import datetime, timedelta

print("=" * 50)
print("  Newsletter Automation Setup")
print("=" * 50)
print()

def ask(prompt):
    value = input(prompt + ": ").strip()
    while not value:
        value = input(f"  (required) {prompt}: ").strip()
    return value

print("Paste each value and hit Enter.\n")

# ── Step 1: Exchange short-lived token for 60-day token ──
print("STEP 1 — Meta Access Token")
print("Go to: developers.facebook.com > Tools > Graph API Explorer")
print("Generate a short-lived token with these permissions:")
print("  - instagram_basic")
print("  - pages_read_engagement")
print("  - pages_show_list")
print()
short_token = ask("Paste your short-lived token here")
print()
print("Now go to your Meta App > Basic Settings and find your App ID and App Secret.")
print()
app_id     = ask("App ID")
app_secret = ask("App Secret")

print("\nExchanging for 60-day token...")
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
    print(f"Error exchanging token: {data['error']['message']}")
    print("Saving short-lived token instead — remember to run refresh_token.py soon.")
    meta_token = short_token
    expires_note = "# Token expires: soon — run refresh_token.py to get a 60-day token"
else:
    meta_token = data.get("access_token")
    expires_in = data.get("expires_in", 5184000)
    expires_date = datetime.now() + timedelta(seconds=expires_in)
    expires_note = f"# Token expires: {expires_date.strftime('%B %d, %Y')} — run refresh_token.py to renew"
    print(f"Success! Token valid until: {expires_date.strftime('%B %d, %Y')}")

# ── Step 2: Find Instagram User ID ──
print("\nLooking up your Instagram account...")
ig_id = None

# Try via /me/accounts first
try:
    pages = requests.get(
        "https://graph.facebook.com/v19.0/me/accounts",
        params={"access_token": short_token}
    ).json().get("data", [])

    for page in pages:
        result = requests.get(
            f"https://graph.facebook.com/v19.0/{page['id']}",
            params={"fields": "instagram_business_account", "access_token": page["access_token"]}
        ).json()
        ig_id = result.get("instagram_business_account", {}).get("id")
        if ig_id:
            print(f"Found Instagram account automatically.")
            break
except Exception:
    pass

# Fallback: ask for Facebook Page ID (needed for Business Manager accounts)
if not ig_id:
    print("Could not find it automatically (common with Business Manager accounts).")
    print()
    print("To find your Facebook Page ID:")
    print("  1. Go to your Facebook Page")
    print("  2. Click 'About' in the left menu")
    print("  3. Scroll to the bottom — you'll see a number labelled 'Page ID'")
    print()
    page_id = ask("Enter your Facebook Page ID")
    result = requests.get(
        f"https://graph.facebook.com/v19.0/{page_id}",
        params={"fields": "instagram_business_account", "access_token": short_token}
    ).json()
    ig_id = result.get("instagram_business_account", {}).get("id")
    if not ig_id:
        print("Still couldn't find it. Enter your Instagram User ID manually.")
        print("(You can find this by running: python3 get_ig_id.py)")
        ig_id = ask("Instagram User ID")

# ── Step 3: Other credentials ──
print()
print("STEP 2 — Claude AI")
anthropic_key = ask("Anthropic API key (from console.anthropic.com)")

print()
print("STEP 3 — Newsletter Settings")
from_name  = ask("Sender name (e.g. Khadijah Safari)")
from_email = ask("Sender email")
cta_text   = ask("CTA button text (e.g. Book a Call)")
cta_url    = ask("CTA button URL")

# ── Step 4: Write .env ──
env_path = os.path.join(os.path.dirname(__file__), ".env")

env_contents = f"""# Meta Graph API
META_ACCESS_TOKEN={meta_token}
{expires_note}
IG_USER_ID={ig_id}

# Anthropic (Claude)
ANTHROPIC_API_KEY={anthropic_key}

# Newsletter settings
NEWSLETTER_FROM_NAME={from_name}
NEWSLETTER_FROM_EMAIL={from_email}
NEWSLETTER_CTA_TEXT={cta_text}
NEWSLETTER_CTA_URL={cta_url}
"""

with open(env_path, "w") as f:
    f.write(env_contents)

print()
print("=" * 50)
print("  Setup complete!")
print("=" * 50)
print()
print("You're ready to run: python3 main.py")
print()
print(f"Reminder: Set a phone reminder to renew your Meta token before {expires_date.strftime('%B %d, %Y') if 'expires_date' in dir() else 'it expires'}.")
print("Just run: python3 refresh_token.py")
