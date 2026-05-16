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
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

            page.wait_for_timeout(12000)

            # STEP 1: try browser join button
            join_browser = page.locator("text=Join from Your Browser")
            if join_browser.count() > 0:
                join_browser.first.click()
                page.wait_for_timeout(8000)

            # DEBUG snapshot (VERY IMPORTANT)
            page.screenshot(path=f"step1_{user}.png", full_page=True)

            # STEP 2: check if we are actually on wrong page
            html = page.content().lower()

            if "download" in html or "install" in html:
                raise Exception("Zoom redirected to app download page")

            if "sign in" in html and "join" not in html:
                raise Exception("Zoom asking sign-in (blocked flow)")

            # STEP 3: more flexible input search
            inputs = page.locator("input")

            if inputs.count() == 0:
                page.screenshot(path=f"no_input_{user}.png", full_page=True)
                raise Exception("No input fields found on page")

            # try first visible input
            name_input = None
            for i in range(min(inputs.count(), 5)):
                try:
                    el = inputs.nth(i)
                    if el.is_visible():
                        name_input = el
                        break
                except:
                    continue

            if not name_input:
                raise Exception("No visible input found")

            name_input.fill(user)

            # STEP 4: click join
            buttons = page.locator("button")

            clicked = False
            for i in range(buttons.count()):
                try:
                    btn = buttons.nth(i)
                    text = btn.inner_text().lower()
                    if "join" in text:
                        btn.click()
                        clicked = True
                        break
                except:
                    continue

            if not clicked:
                raise Exception("Join button not found")

            page.wait_for_timeout(8000)

            print(f"{user}: join attempted")

            return context

        except Exception as e:
            print(f"{user}: failed -> {e}")
            page.screenshot(path=f"error_{user}.png", full_page=True)
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