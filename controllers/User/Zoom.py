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
                    headless=True,
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

                # Faster timeout to avoid Gunicorn worker timeout
                page.goto(
                    ZoomController.meeting_url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )

                page.wait_for_timeout(3000)

                # Try to click Join from browser link
                selectors = [
                    "text=Join from Your Browser",
                    "text=Join from your browser",
                    "a:has-text('Join from your browser')",
                ]

                for selector in selectors:
                    try:
                        page.locator(selector).first.click(timeout=3000)
                        print("Clicked Join from your browser")
                        break
                    except:
                        pass

                page.wait_for_timeout(3000)

                # Fill participant name
                try:
                    page.locator("input").first.fill(user, timeout=3000)
                    print("Name entered")
                except Exception as e:
                    print("Name input not found:", e)

                # Click Join button
                try:
                    page.locator("button:has-text('Join')").first.click(timeout=3000)
                    print("Join button clicked")
                except Exception as e:
                    print("Join button not found:", e)

                page.wait_for_timeout(5000)

                # Save screenshot for debugging
                page.screenshot(path=f"{user}.png", full_page=True)

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