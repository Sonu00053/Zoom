from playwright.sync_api import sync_playwright
import traceback


class ZoomController:
    meeting_url = (
        "https://us05web.zoom.us/j/87417457133"
        "?pwd=OtxCvoT5mGn3rFYlVilSitECCaPlvl.1"
    )

    @staticmethod
    def run_user(user="TestUser"):
        browser = None
        context = None

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,  # REQUIRED on Render
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--no-zygote",
                        "--single-process",
                        "--disable-blink-features=AutomationControlled",
                    ],
                )

                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                )

                page = context.new_page()

                print(f"Opening Zoom meeting for {user}...")
                page.goto(ZoomController.meeting_url, timeout=90000)
                page.wait_for_timeout(8000)

                # Click "Join from your browser"
                join_browser_selectors = [
                    "text=Join from Your Browser",
                    "text=Join from your browser",
                    "a:has-text('Join from your browser')",
                ]

                for selector in join_browser_selectors:
                    try:
                        page.locator(selector).first.click(timeout=5000)
                        print("Clicked Join from your browser")
                        break
                    except:
                        pass

                page.wait_for_timeout(5000)

                # Fill participant name
                try:
                    page.locator("input").first.fill(user)
                    print("Name entered")
                except Exception as e:
                    print("Name input not found:", e)

                # Click Join button
                join_button_selectors = [
                    "button:has-text('Join')",
                    "button:has-text('Join Meeting')",
                ]

                for selector in join_button_selectors:
                    try:
                        page.locator(selector).first.click(timeout=5000)
                        print("Join button clicked")
                        break
                    except:
                        pass

                page.wait_for_timeout(10000)

                # Save screenshot for debugging
                page.screenshot(path=f"{user}.png", full_page=True)

                print(f"{user} join attempted successfully")
                return f"{user} join attempted successfully"

        except Exception as e:
            traceback.print_exc()
            return f"Zoom Error: {str(e)}"

        finally:
            try:
                if context:
                    context.close()
            except:
                pass

            try:
                if browser:
                    browser.close()
            except:
                pass

    @staticmethod
    def start():
        return ZoomController.run_user("TestUser")