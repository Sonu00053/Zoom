import time

class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    users = ["ABC2", "DEF2", "GHI2", "JKL2", "MNO2"]

    stay_seconds = 10

    @classmethod
    def join_user(cls, browser, user):

        from playwright.sync_api import sync_playwright

        context = browser.new_context()

        page = context.new_page()

        try:
            page.goto(cls.meeting_url)

            time.sleep(3)

            context.close()
            return True

        except Exception as e:
            print(e)
            context.close()
            return False

    @classmethod
    def start(cls):

        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox"]
            )

            for user in cls.users:
                cls.join_user(browser, user)

            browser.close()