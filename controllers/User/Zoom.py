import time
from playwright.sync_api import sync_playwright


class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/81669486069?pwd=7x9FAa"

    users = ["ABC2", "DEF2", "GHI2", "JKL2", "MNO2"]

    stay_seconds = 10

    @classmethod
    def start(cls):

        print("🚀 Zoom Bot START CALLED")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
                )

                for user in cls.users:
                    print(f"➡️ Trying user: {user}")
                    cls.join_user(browser, user)

                browser.close()

        except Exception as e:
            print("❌ BOT ERROR:", e)

    @classmethod
    def join_user(cls, browser, user):

        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(cls.meeting_url, timeout=60000)
            page.wait_for_timeout(3000)

            try:
                page.locator("text=Join").first.click(timeout=5000)
            except:
                pass

            page.fill('input[type="text"]', user)

            page.locator("button:has-text('Join')").click(timeout=5000)

            print(f"✅ {user} joined")

            page.wait_for_timeout(cls.stay_seconds * 1000)

            context.close()
            return True

        except Exception as e:
            print(f"❌ {user} failed:", e)
            context.close()
            return False