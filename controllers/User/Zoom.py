# controllers/User/Zoom.py

from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom meeting link
    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"

    # Add participant names here
    users = [
        "ABC2"
    ]

    # Stay in meeting for 30 minutes
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
            # Hide webdriver flag
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Open Zoom meeting
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(10000)

            # Click "Join from Your Browser"
            for selector in [
                'a:has-text("Join from Your Browser")',
                'button:has-text("Join from Your Browser")',
                'button:has-text("Launch Meeting")',
                'a:has-text("join from your browser")',
            ]:
                try:
                    locator = page.locator(selector).first
                    if locator.count() > 0:
                        locator.click(force=True)
                        print("Clicked Join from Browser")
                        page.wait_for_timeout(8000)
                        break
                except Exception:
                    pass

            # Wait for page to render
            page.wait_for_timeout(8000)

            print("Current URL:", page.url)
            print("Page Title:", page.title())

            # Fill participant name
            name_filled = False
            input_selectors = [
                'input#input-for-name',
                'input[name="inputname"]',
                'input[name="username"]',
                'input[name="name"]',
                'input[placeholder*="name" i]',
                'input[type="text"]',
                'input:not([type])',
            ]

            for selector in input_selectors:
                try:
                    field = page.locator(selector).first
                    if field.count() > 0 and field.is_visible():
                        field.fill(user)
                        print(f"{user}: Name filled")
                        name_filled = True
                        break
                except Exception:
                    pass

            if not name_filled:
                page.screenshot(path=f"{user}_name_not_found.png")
                raise Exception("Name input field not found")

            page.wait_for_timeout(2000)

            # Accept preview page / join audio popup if any
            for selector in [
                'button[aria-label="Close"]',
                'button:has-text("Got It")',
                'button:has-text("OK")',
                'button:has-text("Cancel")',
                'button:has-text("Close")',
            ]:
                try:
                    popup = page.locator(selector).first
                    if popup.count() > 0 and popup.is_visible():
                        popup.click(force=True)
                        print("Popup closed")
                        page.wait_for_timeout(1000)
                        break
                except Exception:
                    pass

            # Click Join button
            joined = False
            join_selectors = [
                'button.preview-join-button',
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]',
            ]

            for selector in join_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.count() > 0:
                        try:
                            btn.click(force=True, timeout=10000)
                        except Exception:
                            btn.evaluate("el => el.click()")

                        print(f"{user}: Join button clicked")
                        joined = True
                        break
                except Exception as e:
                    print(f"Join selector failed: {selector} -> {e}")

            if not joined:
                page.screenshot(path=f"{user}_join_not_found.png")
                raise Exception("Join button not found")

            # Wait to enter meeting
            page.wait_for_timeout(15000)

            # Check if user actually entered meeting
            current_url = page.url.lower()
            page_text = page.locator("body").inner_text().lower()

            if (
                "waiting for the host" in page_text
                or "you are in the waiting room" in page_text
                or "/wc/" in current_url
            ):
                print(f"{user}: Successfully joined / waiting room")
            else:
                print(f"{user}: Join status uncertain")

            # Stay connected for 30 minutes
            page.wait_for_timeout(cls.stay_ms)

            context.close()
            return True

        except Exception as e:
            print(f"{user}: Failed -> {e}")

            try:
                page.screenshot(path=f"{user}_error.png")
            except Exception:
                pass

            try:
                context.close()
            except Exception:
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