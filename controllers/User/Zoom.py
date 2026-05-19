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

    # 30 minutes
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
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(10000)

            # Join from browser link/button
            for selector in [
                'a:has-text("Join from Your Browser")',
                'button:has-text("Join from Your Browser")',
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

            # Name input
            name_filled = False
            for selector in [
                'input#input-for-name',
                'input[name="inputname"]',
                'input[name="username"]',
                'input[name="name"]',
                'input[placeholder*="name" i]',
                'input[type="text"]',
            ]:
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
                raise Exception("Name input field not found")

            page.wait_for_timeout(2000)

            # Join button
            joined = False
            for selector in [
                'button.preview-join-button',
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]',
            ]:
                try:
                    btn = page.locator(selector).first
                    if btn.count() > 0:
                        btn.click(force=True)
                        print(f"{user}: Join button clicked")
                        joined = True
                        break
                except Exception:
                    pass

            if not joined:
                raise Exception("Join button not found")

            # Wait to enter meeting
            page.wait_for_timeout(15000)

            print(f"{user}: Joined successfully")

            # Stay in meeting
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

            print({
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
                "duration": "30 minutes",
            })

        except Exception as e:
            print({
                "status": "error",
                "message": str(e),
            })