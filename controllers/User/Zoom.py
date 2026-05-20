from playwright.sync_api import sync_playwright
import time


class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    users = [
        "ABC2",
        "DEF2",
        "GHI2",
        "JKL2",
        "MNO2",
    ]

    stay_seconds = 60  # testing (30 min = 1800)

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}")

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36",
        )

        page = context.new_page()

        try:
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(8000)

            # join from browser
            try:
                page.click("text=Join from Your Browser", timeout=5000)
            except:
                pass

            page.wait_for_timeout(5000)

            # name fill
            for sel in [
                'input[name="name"]',
                'input[type="text"]',
                'input[placeholder*="name" i]'
            ]:
                try:
                    if page.locator(sel).count() > 0:
                        page.fill(sel, user)
                        break
                except:
                    pass

            page.wait_for_timeout(2000)

            # join button
            for sel in [
                "button:has-text('Join')",
                "button[type='submit']"
            ]:
                try:
                    if page.locator(sel).count() > 0:
                        page.click(sel)
                        break
                except:
                    pass

            page.wait_for_timeout(10000)

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
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ],
            )

            for user in cls.users:
                cls.join_user(browser, user)
                time.sleep(2)

            browser.close()