from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom meeting URL
    meeting_url = "https://app.zoom.us/wc/join/87417457133?pwd=55k88c"

    # Kitne fake users join karne hain
    users = [f"ABC{i}" for i in range(1, 2)]  # ABC1

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            permissions=[],
            viewport={"width": 1280, "height": 720},
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

            # Redirect to "Join from your browser" if available
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

            # Name input ke multiple selectors
            name_selectors = [
                'input[type="text"]',
                'input#input-for-name',
                'input[name="name"]',
                'input[placeholder*="name" i]'
            ]

            name_box = None
            for selector in name_selectors:
                try:
                    page.wait_for_selector(selector, timeout=10000)
                    name_box = page.locator(selector).first
                    if name_box.is_visible():
                        break
                except Exception:
                    continue

            if not name_box:
                raise Exception("Name input field not found")

            # Name fill
            name_box.fill(user)

            # Join button selectors
            join_selectors = [
                'button:has-text("Join")',
                'button:has-text("Join Meeting")',
                'button[type="submit"]'
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
                    continue

            if not joined:
                raise Exception("Join button not found")

            print(f"{user}: Join submitted")

            # Wait a few seconds
            page.wait_for_timeout(5000)

            # Dialogs handle
            popup_buttons = [
                'button:has-text("Got it")',
                'button:has-text("OK")',
                'button:has-text("Cancel")',
                'button:has-text("Continue")',
                'button:has-text("Dismiss")'
            ]

            for selector in popup_buttons:
                try:
                    btn = page.locator(selector)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click()
                        page.wait_for_timeout(500)
                except Exception:
                    pass

            print(f"{user}: Joined successfully")
            return context

        except Exception as e:
            print(f"{user}: Failed -> {e}")
            context.close()
            return None

    @classmethod
    def start(cls):
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

            contexts = []

            try:
                for user in cls.users:
                    context = cls.join_user(browser, user)
                    if context:
                        contexts.append(context)

                    time.sleep(1)

                print(f"\n{len(contexts)} participants joined successfully.")

                # Render/Gunicorn timeout se bachne ke liye
                # Infinite loop mat lagao; sirf thoda wait karke return karo
                if contexts:
                    time.sleep(10)

                # Sab contexts close karo
                for context in contexts:
                    try:
                        context.close()
                    except Exception:
                        pass

                browser.close()

                return {
                    "status": "success",
                    "joined": len(contexts),
                    "users": [user for user in cls.users[:len(contexts)]]
                }

            except Exception as e:
                browser.close()
                return {
                    "status": "error",
                    "message": str(e)
                }


if __name__ == "__main__":
    print(ZoomController.start())