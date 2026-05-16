# controllers/User/Zoom.py
# Render Free Plan ke liye optimized version
# IMPORTANT: total_users = 1 rakho, warna memory issue aayega.

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
                print(f"Opening Zoom meeting for {user}...")

                # Lightweight Chromium launch
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--no-zygote",
                        "--single-process",
                        "--disable-extensions",
                        "--disable-background-networking",
                        "--disable-default-apps",
                        "--disable-sync",
                        "--mute-audio",
                    ],
                )

                # Browser context
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    java_script_enabled=True,
                )

                # Block heavy resources
                def block_resources(route):
                    if route.request.resource_type in [
                        "image",
                        "media",
                        "font",
                        "stylesheet",
                    ]:
                        route.abort()
                    else:
                        route.continue_()

                context.route("**/*", block_resources)

                page = context.new_page()

                # Open Zoom page quickly
                page.goto(
                    ZoomController.meeting_url,
                    wait_until="domcontentloaded",
                    timeout=15000,
                )

                # Short wait
                page.wait_for_timeout(1500)

                # Click "Join from your browser"
                selectors = [
                    "text=Join from Your Browser",
                    "text=Join from your browser",
                    "a:has-text('Join from your browser')",
                ]

                for selector in selectors:
                    try:
                        page.locator(selector).first.click(timeout=1500)
                        print(f"{user}: Clicked browser join link")
                        break
                    except:
                        pass

                page.wait_for_timeout(1500)

                # Fill name
                try:
                    page.locator("input").first.fill(user, timeout=1500)
                    print(f"{user}: Name entered")
                except:
                    print(f"{user}: Name input not found")

                # Click Join
                try:
                    page.locator("button:has-text('Join')").first.click(timeout=1500)
                    print(f"{user}: Join button clicked")
                except:
                    print(f"{user}: Join button not found")

                # Save screenshot
                try:
                    page.screenshot(path=f"{user}.png")
                except:
                    pass

                print(f"{user}: Join attempted successfully")

                return f"{user} join attempted successfully"

        except Exception as e:
            traceback.print_exc()
            return f"{user} failed: {str(e)}"

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
        results = []

        # Render free plan ke liye sirf 1 user run karo
        total_users = 1

        for i in range(1, total_users + 1):
            user_name = f"TestUser{i}"
            print(f"Starting {user_name}...")
            result = ZoomController.run_user(user_name)
            results.append(result)

        return "<br>".join(results)