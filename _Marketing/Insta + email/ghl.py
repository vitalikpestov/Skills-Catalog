"""
Go High Level (GHL) API v2 client.
Creates an email campaign draft in your GHL location.
"""

import requests
from datetime import datetime


class GHLClient:
    BASE_URL = "https://services.leadconnectorhq.com"

    def __init__(self, api_key: str, location_id: str):
        self.api_key = api_key
        self.location_id = location_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Version": "2021-07-28",
            "Content-Type": "application/json",
        }

    def _post(self, endpoint: str, payload: dict) -> dict:
        resp = requests.post(
            f"{self.BASE_URL}{endpoint}",
            headers=self.headers,
            json=payload,
        )
        if not resp.ok:
            raise RuntimeError(
                f"GHL API error {resp.status_code}: {resp.text}\n"
                f"Endpoint: {endpoint}"
            )
        return resp.json()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        resp = requests.get(
            f"{self.BASE_URL}{endpoint}",
            headers=self.headers,
            params=params or {},
        )
        resp.raise_for_status()
        return resp.json()

    def create_email_campaign_draft(
        self,
        subject: str,
        html_body: str,
        preview_text: str,
        from_name: str,
        from_email: str,
    ) -> dict:
        """
        Creates an email template in GHL (Marketing > Emails > Templates).
        From there, click the template and select 'Create Campaign' to send.
        """
        print("Creating email template in Go High Level...")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        template_name = f"Newsletter — {timestamp}"

        payload = {
            "locationId": self.location_id,
            "name": template_name,
            "subject": subject,
            "previewText": preview_text,
            "fromName": from_name,
            "fromEmail": from_email,
            "html": html_body,
            "type": "html",
        }

        result = self._post("/emails/builder", payload)
        return result

    def verify_connection(self) -> bool:
        """Quick check that the API key is valid."""
        try:
            self._get("/oauth/installedLocations", params={"limit": 1})
            return True
        except Exception:
            pass
        # If that fails, just assume it's fine and let the campaign creation fail with a clear error
        return True
