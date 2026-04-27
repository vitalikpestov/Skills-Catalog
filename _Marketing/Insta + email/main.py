#!/usr/bin/env python3
"""
Instagram → Newsletter automation
----------------------------------
Generates one email per Instagram post, lets you review/edit each one,
then copies to clipboard for pasting into GHL.

Usage:
    python3 main.py
    python3 main.py --urls https://instagram.com/reel/ABC123 https://instagram.com/p/XYZ
    python3 main.py --whisper-model small
"""

import argparse
import os
import sys
import subprocess
import webbrowser
import pathlib
import tempfile
from dotenv import load_dotenv

from instagram import InstagramClient
from transcriber import transcribe_video
from email_generator import generate_newsletter_email
from ghl import GHLClient


def load_config() -> dict:
    load_dotenv()
    required = {
        "META_ACCESS_TOKEN": os.getenv("META_ACCESS_TOKEN"),
        "IG_USER_ID": os.getenv("IG_USER_ID"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Run python3 setup.py to configure your credentials.")
        sys.exit(1)
    return {
        **required,
        "from_name": os.getenv("NEWSLETTER_FROM_NAME", "Newsletter"),
        "from_email": os.getenv("NEWSLETTER_FROM_EMAIL", ""),
        "subject_prefix": os.getenv("NEWSLETTER_SUBJECT_PREFIX", ""),
        "cta_text": os.getenv("NEWSLETTER_CTA_TEXT", ""),
        "cta_url": os.getenv("NEWSLETTER_CTA_URL", ""),
    }


def get_urls_interactively() -> list[str]:
    print("\nPaste Instagram post URLs (one per line).")
    print("Press Enter twice when done:\n")
    urls = []
    while True:
        line = input().strip()
        if not line:
            if urls:
                break
            print("Please enter at least one URL.")
        else:
            urls.append(line)
    return urls


def copy_to_clipboard(text: str):
    try:
        if sys.platform == "darwin":
            subprocess.run("pbcopy", input=text.encode(), check=True)
            return True
        elif sys.platform == "win32":
            subprocess.run("clip", input=text.encode(), check=True)
            return True
    except Exception:
        pass
    return False


def open_in_editor(filepath: str):
    """Open a file in TextEdit (plain text mode)."""
    if sys.platform == "darwin":
        # Open in TextEdit as plain text (shows raw HTML, easy to edit)
        subprocess.run(["open", "-e", filepath])
    elif sys.platform == "win32":
        subprocess.run(["notepad", filepath])
    else:
        subprocess.run(["xdg-open", filepath])


def review_email(email: dict, index: int, total: int) -> bool:
    """
    Show email preview in browser, let user approve/edit/skip.
    Returns True if approved and pushed to clipboard.
    """
    print(f"\n{'='*50}")
    print(f"Email {index}/{total}")
    print(f"  Subject: {email['subject']}")
    print(f"  Preview: {email['preview_text']}")
    print(f"{'='*50}")

    # Save to temp file and open in browser
    tmp_path = pathlib.Path(f"draft_{index}.html").resolve()
    with open(tmp_path, "w") as f:
        f.write(f"<!-- SUBJECT: {email['subject']} -->\n")
        f.write(f"<!-- PREVIEW: {email['preview_text']} -->\n\n")
        f.write(email["html_body"])

    webbrowser.open(f"file://{tmp_path}")
    print("\nEmail opened in browser for preview.")

    while True:
        print("\nWhat would you like to do?")
        print("  [a] Approve — copy to clipboard and open GHL")
        print("  [e] Edit — find & replace words")
        print("  [u] Change button URL")
        print("  [s] Skip — move to next email")
        print("  [q] Quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "a":
            # Confirm CTA URL before approving
            cta_url = os.getenv("NEWSLETTER_CTA_URL", "").strip()
            if cta_url:
                print(f"\n  CTA URL in this email: {cta_url}")
                new_url = input("  Press Enter to keep it, or paste a new URL: ").strip()
                if new_url:
                    # Update the HTML file with the new URL
                    with open(tmp_path, "r") as f:
                        content = f.read()
                    content = content.replace(cta_url, new_url)
                    with open(tmp_path, "w") as f:
                        f.write(content)
                    print(f"  URL updated to: {new_url}")
                    webbrowser.open(f"file://{tmp_path}")
                    input("  Browser refreshed — press Enter to continue...")

            # Re-read in case it was edited
            with open(tmp_path, "r") as f:
                content = f.read()
            # Strip the comment lines to get just HTML
            html = "\n".join(
                line for line in content.split("\n")
                if not line.startswith("<!-- SUBJECT:") and not line.startswith("<!-- PREVIEW:")
            ).strip()

            copied = copy_to_clipboard(html)
            ghl_url = "https://app.gohighlevel.com/marketing/emails/campaigns"
            webbrowser.open(ghl_url)

            if copied:
                print("\n  HTML copied to clipboard!")
            print("  GHL Campaigns page opened.")
            print("  Click '+ New' > 'Blank' > '</>' HTML button > Cmd+V to paste")
            input("\n  Press Enter when done to continue to next email...")
            return True

        elif choice == "e":
            import re as _re
            with open(tmp_path, "r") as f:
                content = f.read()

            # Strip tags to show readable text preview
            preview = _re.sub(r'<[^>]+>', '', content)
            preview = _re.sub(r'\n{3,}', '\n\n', preview).strip()
            # Remove comment lines
            preview_lines = [l for l in preview.split('\n') if not l.strip().startswith('<!--')]
            preview = '\n'.join(preview_lines).strip()
            print("\n" + "─"*50)
            print(preview[:2000])
            print("─"*50)

            print("\n  Type the exact words you want to change (or press Enter to go back).")
            while True:
                find = input("\n  Find: ").strip()
                if not find:
                    break
                if find not in content:
                    print(f"  ❌ Not found. Check the text above and try again.")
                    continue
                replace = input("  Replace with: ").strip()
                content = content.replace(find, replace)
                with open(tmp_path, "w") as f:
                    f.write(content)
                print(f"  ✅ Done. Make another change, or press Enter to finish.")

            webbrowser.open(f"file://{tmp_path}")
            print("  Browser refreshed with your edits.")

        elif choice == "u":
            import re
            with open(tmp_path, "r") as f:
                content = f.read()
            urls = list(set(re.findall(r'href=["\']([^"\']+)["\']', content)))
            urls = [u for u in urls if u.startswith("http")]
            if not urls:
                print("\n  No links found in this email.")
                print("  Would you like to add a CTA button?")
                btn_text = input("  Button text (or press Enter to skip): ").strip()
                if btn_text:
                    btn_url = input("  Button URL: ").strip()
                    if btn_url:
                        cta_html = (
                            f'\n<div style="text-align:center;margin:32px 0;">'
                            f'<a href="{btn_url}" style="background-color:#000;color:#fff;'
                            f'padding:14px 32px;text-decoration:none;border-radius:4px;'
                            f'font-weight:bold;display:inline-block;">{btn_text}</a></div>\n'
                        )
                        # Insert before </body> if present, otherwise append
                        if "</body>" in content:
                            content = content.replace("</body>", cta_html + "</body>")
                        else:
                            content += cta_html
                        with open(tmp_path, "w") as f:
                            f.write(content)
                        webbrowser.open(f"file://{tmp_path}")
                        print(f"  Button added. Browser refreshed.")
            else:
                print("\n  URLs in this email:")
                for i, url in enumerate(urls, 1):
                    print(f"  [{i}] {url}")
                pick = input("\n  Which number to replace? ").strip()
                try:
                    current_url = urls[int(pick) - 1]
                    new_url = input("  New URL: ").strip()
                    if new_url:
                        content = content.replace(current_url, new_url)
                        with open(tmp_path, "w") as f:
                            f.write(content)
                        webbrowser.open(f"file://{tmp_path}")
                        print("  URL updated. Browser refreshed.")
                except (ValueError, IndexError):
                    print("  Invalid selection.")

        elif choice == "s":
            print("  Skipped.")
            return False

        elif choice == "q":
            print("\nQuitting.")
            sys.exit(0)

        else:
            print("  Please type a, e, s, or q.")


def run(urls: list[str], config: dict, whisper_model: str):
    # --- Step 1: Fetch Instagram posts ---
    print(f"\n[1/3] Fetching {len(urls)} Instagram post(s)...")
    ig = InstagramClient(
        access_token=config["META_ACCESS_TOKEN"],
        ig_user_id=config["IG_USER_ID"],
    )
    posts = ig.get_posts_by_urls(urls)

    if not posts:
        print("No posts found. Check that the URLs belong to the configured account.")
        sys.exit(1)

    print(f"  Found {len(posts)} post(s)")

    # --- Step 2: Transcribe any Reels ---
    print("\n[2/3] Processing content...")
    video_tmp_files = []

    for post in posts:
        if post.get("type") == "VIDEO" and post.get("video_url"):
            print(f"  Reel detected — transcribing...")
            tmp_path = ig.download_video(post["video_url"])
            video_tmp_files.append(tmp_path)
            post["transcript"] = transcribe_video(tmp_path, model_size=whisper_model)
            print(f"  Done ({len(post['transcript'])} chars)")
        else:
            print(f"  Post: using caption")

    # --- Step 3: Generate one email per post ---
    print(f"\n[3/3] Generating {len(posts)} email(s) with Claude...\n")

    emails = []
    for i, post in enumerate(posts, 1):
        print(f"  Writing email {i}/{len(posts)}...")
        email = generate_newsletter_email(
            posts_content=[post],
            client_name=config["from_name"],
            from_name=config["from_name"],
            subject_prefix=config["subject_prefix"],
            anthropic_api_key=config["ANTHROPIC_API_KEY"],
            cta_text=config["cta_text"],
            cta_url=config["cta_url"],
        )
        emails.append(email)
        print(f"  Subject: {email['subject']}")

    # --- Review and approve each email ---
    print(f"\nAll {len(emails)} email(s) generated. Starting review...\n")

    approved = 0
    for i, email in enumerate(emails, 1):
        result = review_email(email, i, len(emails))
        if result:
            approved += 1

    # Cleanup temp video files
    for tmp in video_tmp_files:
        try:
            os.unlink(tmp)
        except OSError:
            pass

    print(f"\nDone. {approved}/{len(emails)} email(s) approved and sent to GHL.")


def main():
    parser = argparse.ArgumentParser(description="Instagram → Newsletter automation")
    parser.add_argument("--urls", nargs="+", help="Instagram post URLs")
    parser.add_argument(
        "--whisper-model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
    )
    args = parser.parse_args()

    config = load_config()
    urls = args.urls if args.urls else get_urls_interactively()
    urls = [u.strip() for u in urls if u.strip()]

    if not urls:
        print("No URLs provided.")
        sys.exit(1)

    run(urls, config, whisper_model=args.whisper_model)


if __name__ == "__main__":
    main()
