from playwright.sync_api import sync_playwright
import time


class ZoomController:

    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"
    users = ["ABC2"]

    @classmethod
    def join_user(cls, browser, user):

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36",
        )

        page = context.new_page()

        try:
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(10000)

            # click join from browser
            try:
                page.click("text=Join from Your Browser", timeout=15000)
            except:
                pass

            page.wait_for_timeout(8000)

            # find input
            inputs = page.locator("input")

            filled = False
            for i in range(inputs.count()):
                if inputs.nth(i).is_visible():
                    inputs.nth(i).fill(user)
                    filled = True
                    break

            if not filled:
                raise Exception("Name input not found")

            # click join
            buttons = page.locator("button")

            clicked = False
            for i in range(buttons.count()):
                btn = buttons.nth(i)
                if btn.is_visible():
                    if "join" in btn.inner_text().lower():
                        btn.click()
                        clicked = True
                        break

            if not clicked:
                raise Exception("Join button not found")

            page.wait_for_timeout(15000)

            print(f"{user} joined successfully")

            page.wait_for_timeout(1800000)  # 30 min stay

            context.close()
            return True

        except Exception as e:
            print(f"{user} error: {e}")
            try:
                page.screenshot(path=f"{user}_error.png")
            except:
                pass
            context.close()
            return False

    @classmethod
    def start(cls):

        result = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            for user in cls.users:
                if cls.join_user(browser, user):
                    result.append(user)

            browser.close()

        return {
            "status": "success",
            "joined_users": result
        }