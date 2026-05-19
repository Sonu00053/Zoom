# controllers/User/Zoom.py
from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom web client join link
    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    # Names to join with
    users = ["ABC2"]

    # Stay in meeting (30 minutes)
    stay_ms = 30 * 60 * 1000

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            java_script_enabled=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        try:
            # Reduce automation detection
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Open Zoom link
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(10000)

            # Click "Join from Your Browser" if shown
            for selector in [
                'text="Join from Your Browser"',
                'text="join from your browser"',
                'text="Launch Meeting"',
            ]:
                try:
                    page.locator(selector).first.click(timeout=5000)
                    print("Clicked browser join link")
                    page.wait_for_timeout(8000)
                    break
                except:
                    pass

            # Wait a bit instead of networkidle (Zoom keeps connections open)
            page.wait_for_timeout(8000)

            # Fill visible text input with participant name
            name_filled = False
            inputs = page.locator('input[type="text"], input:not([type])')

            for i in range(inputs.count()):
                try:
                    field = inputs.nth(i)
                    if field.is_visible():
                        field.fill(user)
                        print(f"{user}: Name filled")
                        name_filled = True
                        break
                except:
                    pass

            if not name_filled:
                page.screenshot(path=f"{user}_name_not_found.png")
                raise Exception("Name input field not found")

            page.wait_for_timeout(2000)

            # Click Join button
            joined = False
            for selector in [
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]',
            ]:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible():
                        btn.click()
                        print(f"{user}: Join clicked")
                        joined = True
                        break
                except:
                    pass

            if not joined:
                page.screenshot(path=f"{user}_join_not_found.png")
                raise Exception("Join button not found")

            # Wait for admission / meeting screen
            page.wait_for_timeout(15000)

            print(f"{user}: Joined successfully")

            # Stay in meeting for 30 minutes
            page.wait_for_timeout(cls.stay_ms)

            context.close()
            return True

        except Exception as e:
            print(f"{user}: Failed -> {e}")

            try:
                page.screenshot(path=f"{user}_error.png")
            except:
                pass

            try:
                context.close()
            except:
                pass

            return False

    @classmethod
    def start(cls):
        joined_users = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--mute-audio",
                        "--disable-notifications",
                        "--disable-popup-blocking",
                        "--disable-infobars",
                        "--disable-blink-features=AutomationControlled",
                        "--window-size=1366,768",
                    ],
                )

                for user in cls.users:
                    if cls.join_user(browser, user):
                        joined_users.append(user)
                    time.sleep(2)

                browser.close()

            return {
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
                "duration": "30 minutes",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }