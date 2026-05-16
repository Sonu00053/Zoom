from playwright.sync_api import sync_playwright
import time


class ZoomController:

    meeting_url = "https://us05web.zoom.us/wc/join/84507049104?pwd=3PtVVMpyq11H6UFG81bawvwm0snLbr.1"
    user_name = "TestUser"

    @classmethod
    def run(cls):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False,   # IMPORTANT: set False for debugging
                args=[
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-gpu",
                ],
            )

            context = browser.new_context(
                viewport={"width": 1280, "height": 720}
            )

            page = context.new_page()

            try:
                print("Opening Zoom meeting...")

                page.goto(cls.meeting_url, wait_until="domcontentloaded", timeout=60000)

                page.wait_for_timeout(5000)

                # Try browser join button
                try:
                    btn = page.locator("text=Join from Your Browser")
                    if btn.count() > 0:
                        btn.first.click()
                        print("Clicked 'Join from Browser'")
                        page.wait_for_timeout(5000)
                except:
                    pass

                # Detect redirect to app download
                html = page.content().lower()

                if "download" in html or "install" in html:
                    print("❌ This meeting does NOT allow browser join.")
                    page.screenshot(path="zoom_blocked.png", full_page=True)
                    return

                if "sign in" in html:
                    print("⚠️ Meeting requires sign-in")

                # Find name input
                inputs = page.locator("input")

                if inputs.count() == 0:
                    print("❌ No input found (likely blocked or different flow)")
                    page.screenshot(path="no_input.png", full_page=True)
                    return

                name_input = inputs.first
                name_input.fill(cls.user_name)

                # Click join button
                join_btn = page.locator("button:has-text('Join')")

                if join_btn.count() > 0:
                    join_btn.first.click()
                    print("✅ Join clicked")
                else:
                    print("❌ Join button not found")

                page.wait_for_timeout(10000)

                print("Test completed.")

            except Exception as e:
                print("Error:", e)
                page.screenshot(path="error.png", full_page=True)

            finally:
                time.sleep(5)
                context.close()
                browser.close()


if __name__ == "__main__":
    ZoomTester.run()