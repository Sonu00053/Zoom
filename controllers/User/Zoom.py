from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom meeting URL
    meeting_url = "https://app.zoom.us/wc/join/87417457133?pwd=55k88c"

    # Sirf 1 user test ke liye
    users = ["ABC2"]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            permissions=[],
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True,
        )

        page = context.new_page()

        try:
            # Camera/Mic disable
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Zoom page open
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # "Join from Your Browser" link handle
            try:
                browser_link = page.locator(
                    'a:has-text("Join from Your Browser"), '
                    'a:has-text("join from your browser")'
                )
                if browser_link.count() > 0:
                    browser_link.first.click()
                    page.wait_for_timeout(5000)
            except Exception:
                pass

            # Name input selectors
            name_selectors = [
                'input#input-for-name',
                'input[name="name"]',
                'input[type="text"]',
                'input[placeholder*="name" i]',
            ]

            name_box = None
            for selector in name_selectors:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    locator = page.locator(selector).first
                    if locator.is_visible():
                        name_box = locator
                        break
                except Exception:
                    pass

            if not name_box:
                raise Exception("Name input field not found")

            # Fill participant name
            name_box.fill(user)

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
                        break
                except Exception:
                    pass

            if not joined:
                raise Exception("Join button not found")

            print(f"{user}: Joined successfully")

            # Meeting ko 10 seconds tak open rakho
            page.wait_for_timeout(10000)

            context.close()
            return True

        except Exception as e:
            print(f"{user}: Failed -> {e}")
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
                        "--single-process",
                        "--no-zygote",
                    ],
                )

                for user in cls.users:
                    if cls.join_user(browser, user):
                        joined_users.append(user)

                    # Chhota delay
                    time.sleep(1)

                browser.close()

            return {
                "status": "success",
                "joined_count": len(joined_users),
                "joined_users": joined_users,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }


if __name__ == "__main__":
    print(ZoomController.start())