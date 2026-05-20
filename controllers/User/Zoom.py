import time

class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    users = ["ABC1", "DEF1", "GHI1"]

    @classmethod
    def join_user(cls, browser, user):

        from playwright.sync_api import sync_playwright

        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(cls.meeting_url)

            page.wait_for_timeout(3000)

            context.close()
            return True

        except Exception as e:
            print("Error:", e)
            context.close()
            return False

    @classmethod
    def start(cls):

        # lazy import (IMPORTANT for Railway stability)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            for user in cls.users:
                cls.join_user(browser, user)
                time.sleep(1)

            browser.close()