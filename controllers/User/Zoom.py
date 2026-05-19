from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # meeting_url can be WC/JOIN link
    meeting_url = "https://app.zoom.us/wc/join/9779246549?pwd=UezT5M"
    # add multiple names here
    users = ["ABC2"]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            permissions=[],
            java_script_enabled=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
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

                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Open meeting URL
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            page.wait_for_timeout(8000)

            # Click browser join link if present
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
                    if locator.count() > 0 and locator.is_visible():
                        locator.click()
                        print("Clicked browser join link")
                        page.wait_for_timeout(8000)
                        break
                except Exception:
                    pass

            page.wait_for_load_state("networkidle", timeout=30000)

            print("Current URL:", page.url)
            print("Page Title:", page.title())

            # Wait up to 60 seconds for name field
            name_box = None

            for _ in range(12):
                selectors = [
                    'input#input-for-name',
                    'input[name="inputname"]',
                    'input[name="username"]',
                    'input[name="name"]',
                    'input[placeholder*="name" i]',
                    'input[type="text"]',
                ]

                for selector in selectors:
                    try:
                        locator = page.locator(selector).first
                        if locator.count() > 0 and locator.is_visible():
                            name_box = locator
                            print(f"Name field found with selector: {selector}")
                            break
                    except Exception:
                        pass

                if name_box:
                    break

                print("Name field not found yet, waiting 5 seconds...")
                page.wait_for_timeout(5000)

            if not name_box:
                raise Exception("Name input field not found")

            # Fill name
            name_box.fill(user)
            page.wait_for_timeout(2000)

            # Click Join button
            join_selectors = [
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]',
            ]

            joined = False

            for selector in join_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.count() > 0 and btn.is_visible():
                        btn.click()
                        joined = True
                        print(f"{user}: Join button clicked")
                        break
                except Exception:
                    pass

            if not joined:
                raise Exception("Join button not found")

            # Wait to enter meeting
            page.wait_for_timeout(15000)

            print(f"{user}: Joined successfully")

            # Stay in meeting for 30 minutes
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

            print({
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
                "duration": "30 minutes",
            })

            return {
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
                "duration": "30 minutes",
            }

        except Exception as e:
            print({
                "status": "error",
                "message": str(e),
            })

            return {
                "status": "error",
                "message": str(e),
            }