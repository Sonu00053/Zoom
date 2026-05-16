from playwright.sync_api import sync_playwright
import time

class ZoomController:

    meeting_url = "https://us05web.zoom.us/j/87417457133?pwd=OtxCvoT5mGn3rFYlVilSitECCaPlvl.1"

    @staticmethod
    def run_user(user="TestUser"):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False,  # important for Zoom stability
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context()
            page = context.new_page()

            try:
                page.goto(ZoomController.meeting_url, timeout=60000)

                page.wait_for_timeout(8000)

                # join from browser (if available)
                try:
                    page.get_by_text("Join from your browser", exact=False).click(timeout=5000)
                except:
                    pass

                page.wait_for_timeout(5000)

                # fill name
                name_input = page.locator("input:visible").first
                name_input.fill(user)

                # click join
                join_btn = page.locator("button:has-text('Join')").first
                join_btn.click()

                page.wait_for_timeout(10000)

                print("Joined successfully")

            except Exception as e:
                print("Error:", e)
                page.screenshot(path="error.png", full_page=True)

            finally:
                context.close()
                browser.close()

    @staticmethod
    def start():
        ZoomController.run_user("TestUser")
        return "Zoom join attempted"