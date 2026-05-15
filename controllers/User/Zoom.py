from playwright.sync_api import sync_playwright
import threading
import time
import traceback


class ZoomController:

    # Zoom meeting URL
    meeting_url = "https://us05web.zoom.us/wc/join/84507049104?pwd=3PtVVMpyq11H6UFG81bawvwm0snLbr.1"

    # Simple test users list (sequential only)
    users = [f"TestUser{i}" for i in range(1, 6)]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            permissions=[]
        )

        page = context.new_page()

        try:
            # Disable media devices
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Open Zoom
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(5000)

            # Handle "Join from Browser"
            try:
                join_browser = page.locator('a:has-text("Join from Your Browser")')
                if join_browser.count() > 0:
                    join_browser.first.click()
                    page.wait_for_timeout(3000)
            except:
                pass

            # Enter name
            name_input = page.locator('input[type="text"]').first
            name_input.wait_for(timeout=20000)
            name_input.fill(user)

            # Click Join
            join_btn = page.locator(
                'button:has-text("Join"), button:has-text("Join Meeting")'
            ).first
            join_btn.click()

            page.wait_for_timeout(8000)

            # Status check
            content = page.content().lower()

            if "waiting room" in content:
                print(f"{user}: waiting room")
            else:
                print(f"{user}: join attempted")

            return context

        except Exception as e:
            print(f"{user}: failed -> {e}")
            traceback.print_exc()
            context.close()
            return None

    @classmethod
    def run_zoom(cls):
        try:
            with sync_playwright() as p:

                # IMPORTANT: DO NOT check manual browser path
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                    ],
                )

                contexts = []

                for user in cls.users:
                    context = cls.join_user(browser, user)
                    if context:
                        contexts.append(context)

                    time.sleep(1)

                print(f"{len(contexts)} sessions created.")

                # keep alive
                time.sleep(300)

                for c in contexts:
                    try:
                        c.close()
                    except:
                        pass

                browser.close()
                print("Browser closed.")

        except Exception as e:
            print("ZoomController Error:", e)
            traceback.print_exc()

    @classmethod
    def start(cls):
        thread = threading.Thread(target=cls.run_zoom, daemon=True)
        thread.start()
        return "Zoom automation started successfully!"