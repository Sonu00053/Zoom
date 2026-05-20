import time
from playwright.sync_api import sync_playwright


class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/81669486069?pwd=7x9FAa"

    users = ["ABC2", "DEF2", "GHI2", "JKL2", "MNO2"]

    stay_seconds = 10

    @classmethod
    def join_user(cls, browser, user):

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 Chrome/124",
        )

        page = context.new_page()

        try:
            print(f"➡️ Opening Zoom for {user}")

            page.goto(cls.meeting_url, wait_until="networkidle", timeout=90000)

            page.wait_for_timeout(5000)

            try:
                page.locator("text=Join").first.click(timeout=5000)
            except:
                print("Join button not found")

            page.wait_for_timeout(3000)

            # Name input (safe universal)
            try:
                page.fill('input[type="text"]', user)
            except:
                print("Name input not found")

            page.wait_for_timeout(2000)

            # Final join
            try:
                page.locator("button:has-text('Join')").click(timeout=5000)
            except:
                print("Final join button not found")

            print(f"✅ {user} joined")

            page.wait_for_timeout(cls.stay_seconds * 1000)

            context.close()
            return True

        except Exception as e:
            print(f"❌ {user} FAILED: {e}")
            context.close()
            return False

    @classmethod
    def start(cls):

        print("🚀 Zoom Bot Started")

        joined = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            for user in cls.users:
                result = cls.join_user(browser, user)

                if result:
                    joined.append(user)

                time.sleep(2)

            browser.close()

        print("🎯 DONE:", {"joined": joined})