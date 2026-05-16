# controllers/User/Zoom.py

from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom Meeting URL
    meeting_url = "https://app.zoom.us/wc/join/87417457133?pwd=55k88c"

    # Bot users
    users = ["ABC2"]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            permissions=[],
            java_script_enabled=True,
        )

        page = context.new_page()

        try:
            # Disable camera and microphone
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Open Zoom URL
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Wait for page load
            page.wait_for_timeout(5000)

            # Click "Join from Your Browser" if available
            browser_selectors = [
                'a:has-text("Join from Your Browser")',
                'a:has-text("join from your browser")',
                'button:has-text("Join from Your Browser")',
                'button:has-text("Launch Meeting")',
                'a[href*="wc/join"]',
            ]

            for selector in browser_selectors:
                try:
                    locator = page.locator(selector).first
                    if locator.is_visible():
                        locator.click()
                        print("Clicked browser join link")
                        page.wait_for_timeout(5000)
                        break
                except Exception:
                    pass

            # Wait until network is idle
            page.wait_for_load_state("networkidle", timeout=30000)

            # Debug logs
            print("Current URL:", page.url)
            print("Page Title:", page.title())

            # Name input selectors
            name_selectors = [
                'input#input-for-name',
                'input[name="inputname"]',
                'input[name="username"]',
                'input[name="name"]',
                'input[placeholder*="name" i]',
                'input[type="text"]',
            ]

            name_box = None
            for selector in name_selectors:
                try:
                    locator = page.locator(selector).first
                    if locator.is_visible(timeout=5000):
                        name_box = locator
                        print(f"Name field found with selector: {selector}")
                        break
                except Exception:
                    pass

            if not name_box:
                page.screenshot(path=f"{user}_debug.png")
                raise Exception("Name input field not found")

            # Fill participant name
            name_box.fill(user)
            page.wait_for_timeout(1000)

            # Join button selectors
            join_selectors = [
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]',
            ]

            joined = False
            for selector in join_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible():
                        btn.click()
                        joined = True
                        print(f"{user}: Join button clicked")
                        break
                except Exception:
                    pass

            if not joined:
                page.screenshot(path=f"{user}_join_debug.png")
                raise Exception("Join button not found")

            print(f"{user}: Joined successfully")

            # Keep bot in Zoom meeting for 30 minutes
            # 30 min = 30 × 60 × 1000 = 1,800,000 ms
            page.wait_for_timeout(1800000)

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
                        "--window-size=1280,720",
                    ],
                )

                for user in cls.users:
                    if cls.join_user(browser, user):
                        joined_users.append(user)

                    time.sleep(1)

                browser.close()

            return {
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
                "duration": "30 minutes"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }