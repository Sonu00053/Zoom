from playwright.sync_api import sync_playwright
import threading
import time
import traceback


class ZoomController:

    meeting_url = "https://us05web.zoom.us/wc/join/84507049104?pwd=3PtVVMpyq11H6UFG81bawvwm0snLbr.1"

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
            # block camera/mic
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # open zoom
            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(8000)

            # OPTIONAL: click "Join from browser"
            try:
                join_browser = page.locator("text=Join from Your Browser")
                if join_browser.count() > 0:
                    join_browser.first.click()
                    page.wait_for_timeout(5000)
            except:
                pass

            # DEBUG (uncomment if needed)
            # page.screenshot(path=f"debug_{user}.png", full_page=True)

            # -------------------------
            # FIND NAME INPUT (ROBUST)
            # -------------------------
            selectors = [
                'input[name="name"]',
                'input[placeholder*="name" i]',
                'input[type="text"]'
            ]

            name_input = None

            for sel in selectors:
                loc = page.locator(sel)
                try:
                    if loc.count() > 0:
                        loc.first.wait_for(timeout=8000)
                        name_input = loc.first
                        break
                except:
                    continue

            if not name_input:
                page.screenshot(path=f"error_{user}.png", full_page=True)
                raise Exception("Name input not found (Zoom UI blocked / changed)")

            name_input.fill(user)

            # -------------------------
            # CLICK JOIN BUTTON
            # -------------------------
            join_button = page.locator(
                'button:has-text("Join"), button:has-text("Join Meeting")'
            )

            if join_button.count() > 0:
                join_button.first.click()
            else:
                raise Exception("Join button not found")

            page.wait_for_timeout(8000)

            # check status
            content = page.content().lower()

            if "waiting room" in content or "waiting for the host" in content:
                print(f"{user}: in waiting room")
            else:
                print(f"{user}: join attempted")

            return context

        except Exception as e:
            print(f"{user}: failed -> {e}")
            traceback.print_exc()
            page.screenshot(path=f"fail_{user}.png", full_page=True)
            context.close()
            return None

    @classmethod
    def run_zoom(cls):

        try:
            with sync_playwright() as p:

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
                    ctx = cls.join_user(browser, user)
                    if ctx:
                        contexts.append(ctx)

                    time.sleep(1)

                print(f"{len(contexts)} users processed.")

                time.sleep(600)

                for c in contexts:
                    try:
                        c.close()
                    except:
                        pass

                browser.close()
                print("Browser closed")

        except Exception as e:
            print("ZoomController Error:", e)
            traceback.print_exc()

    @classmethod
    def start(cls):
        thread = threading.Thread(target=cls.run_zoom, daemon=True)
        thread.start()
        return "Zoom automation started"