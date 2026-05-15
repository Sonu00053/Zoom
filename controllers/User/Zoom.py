# controllers/User/Zoom.py

from playwright.sync_api import sync_playwright
import threading
import time
import traceback


class ZoomController:
    # Zoom meeting URL
    meeting_url = "https://app.zoom.us/wc/join/84507049104?pwd=4059Rm"

    # Start with 10 users for Render
    users = [f"TestUser{i}" for i in range(1, 11)]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            permissions=[],
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()

        try:
            # Disable camera/mic
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Open Zoom Web Client
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=45000
            )

            # Fill participant name
            page.wait_for_selector('input[type="text"]', timeout=15000)
            page.locator('input[type="text"]').first.fill(user)

            # Click Join button
            page.locator(
                'button:has-text("Join"), '
                'button:has-text("Join Meeting")'
            ).first.click()

            page.wait_for_timeout(3000)

            print(f"{user}: joined successfully")
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
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--mute-audio",
                        "--disable-notifications",
                        "--disable-popup-blocking",
                        "--disable-infobars",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                    ],
                )

                contexts = []

                for user in cls.users:
                    context = cls.join_user(browser, user)
                    if context:
                        contexts.append(context)

                    time.sleep(0.2)

                print(f"{len(contexts)} users joined successfully.")

                # Keep users connected for 10 minutes
                time.sleep(600)

                browser.close()
                print("Browser closed.")

        except Exception as e:
            print("ZoomController Error:", e)
            traceback.print_exc()

    @classmethod
    def start(cls):
        # Run in background thread so Flask responds immediately
        thread = threading.Thread(target=cls.run_zoom, daemon=True)
        thread.start()

        return "Zoom automation started successfully!"