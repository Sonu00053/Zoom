# controllers/User/Zoom.py

from playwright.sync_api import sync_playwright
import threading
import time
import traceback
import glob


class ZoomController:
    # Zoom Web Client URL
    meeting_url = "https://us05web.zoom.us/wc/join/84507049104?pwd=3PtVVMpyq11H6UFG81bawvwm0snLbr.1"

    # Test users
    users = [f"TestUser{i}" for i in range(1, 11)]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            permissions=[],
        )

        page = context.new_page()

        try:
            # Disable camera and microphone access
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Open Zoom web client
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(5000)

            # Click "Join from Your Browser" if present
            try:
                browser_link = page.locator('a:has-text("Join from Your Browser")')
                if browser_link.count() > 0:
                    browser_link.first.click()
                    page.wait_for_timeout(3000)
            except:
                pass

            # Fill participant name
            name_input = page.locator('input[type="text"]').first
            name_input.wait_for(timeout=20000)
            name_input.fill(user)

            # Click Join button
            join_button = page.locator(
                'button:has-text("Join"), button:has-text("Join Meeting")'
            ).first
            join_button.click()

            page.wait_for_timeout(8000)

            # Check if user is in waiting room
            content = page.content().lower()
            if "waiting room" in content or "waiting for the host" in content:
                print(f"{user}: in waiting room")
            else:
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
                # Dynamically locate installed Chromium
                chrome_candidates = glob.glob(
                    "/opt/render/project/src/.venv/lib/python3.11/"
                    "site-packages/playwright/driver/package/"
                    ".local-browsers/chromium-*/chrome-linux/chrome"
                )

                if not chrome_candidates:
                    raise Exception("Chromium executable not found")

                chrome_path = chrome_candidates[0]
                print("Using Chromium:", chrome_path)

                browser = p.chromium.launch(
                    channel="chromium",
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

                print(f"{len(contexts)} users joined successfully.")

                # Keep users connected for 10 minutes
                time.sleep(600)

                # Close contexts
                for context in contexts:
                    try:
                        context.close()
                    except:
                        pass

                browser.close()
                print("Browser closed.")

        except Exception as e:
            print("ZoomController Error:", e)
            traceback.print_exc()

    @classmethod
    def start(cls):
        # Run in background thread so Flask returns immediately
        thread = threading.Thread(target=cls.run_zoom, daemon=True)
        thread.start()

        return "Zoom automation started successfully!"
