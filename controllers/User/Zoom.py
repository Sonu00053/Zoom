import time
from playwright.sync_api import sync_playwright


class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    users = ["ABC2", "DEF2", "GHI2"]

    stay_seconds = 10  # ⚠️ Railway safe (30 min हटाया)

    @classmethod
    def join_user(cls, browser, user):

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 Chrome/124",
        )

        page = context.new_page()

        try:
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(3000)

            # Try join button safely
            try:
                page.click("text=Join from Your Browser", timeout=3000)
            except:
                pass

            page.wait_for_timeout(2000)

            # Fill name (safe selectors only)
            for selector in [
                'input[name="name"]',
                'input[type="text"]',
                'input[placeholder*="name" i]'
            ]:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, user)
                        break
                except:
                    pass

            page.wait_for_timeout(1000)

            # Join button
            try:
                page.click("button:has-text('Join')", timeout=5000)
            except:
                pass

            page.wait_for_timeout(5000)

            print(f"{user} joined")

            time.sleep(cls.stay_seconds)

            context.close()
            return True

        except Exception as e:
            print(f"{user} failed: {e}")
            context.close()
            return False

    @classmethod
    def start(cls):

        joined = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ],
            )

            for user in cls.users:
                try:
                    if cls.join_user(browser, user):
                        joined.append(user)
                    time.sleep(1)
                except Exception as e:
                    print("Error:", e)

            browser.close()

        print({
            "status": "done",
            "joined": joined
        })