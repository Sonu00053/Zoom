# controllers/User/Zoom.py

from playwright.sync_api import sync_playwright
import traceback


class ZoomController:
    # Zoom meeting URL
    meeting_url = (
        "https://us05web.zoom.us/j/87417457133"
        "?pwd=OtxCvoT5mGn3rFYlVilSitECCaPlvl.1"
    )

    @staticmethod
    def run_user(user="TestUser"):
        """
        Launches a headless Chromium browser and attempts to join
        the Zoom meeting using the provided participant name.
        """
        browser = None
        context = None

        try:
            with sync_playwright() as p:
                # Launch lightweight Chromium for Render
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--no-zygote",
                        "--disable-extensions",
                        "--disable-background-networking",
                        "--disable-default-apps",
                        "--disable-sync",
                        "--mute-audio",
                    ],
                )

                # Create browser context
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    java_script_enabled=True,
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                )

                # Block heavy resources to reduce memory usage
                def block_resources(route):
                    if route.request.resource_type in ["image", "media", "font"]:
                        route.abort()
                    else:
                        route.continue_()

                context.route("**/*", block_resources)

                # Create page
                page = context.new_page()

                print(f"Opening Zoom meeting for {user}...")

                # Open Zoom URL
                page.goto(
                    ZoomController.meeting_url,
                    wait_until="domcontentloaded",
                    timeout=20000,
                )

                page.wait_for_timeout(2000)

                # Click "Join from your browser"
                join_browser_selectors = [
                    "text=Join from Your Browser",
                    "text=Join from your browser",
                    "a:has-text('Join from your browser')",
                ]

                for selector in join_browser_selectors:
                    try:
                        page.locator(selector).first.click(timeout=2000)
                        print(f"{user}: Clicked Join from your browser")
                        break
                    except:
                        pass

                page.wait_for_timeout(2000)

                # Fill participant name
                try:
                    page.locator("input").first.fill(user, timeout=2000)
                    print(f"{user}: Name entered")
                except:
                    print(f"{user}: Name input not found")

                # Click Join button
                try:
                    page.locator("button:has-text('Join')").first.click(timeout=2000)
                    print(f"{user}: Join button clicked")
                except:
                    print(f"{user}: Join button not found")

                # Wait for join process
                page.wait_for_timeout(3000)

                # Save screenshot for debugging
                page.screenshot(path=f"{user}.png")

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
        """
        Runs multiple fake users sequentially.
        On Render free plan, keep this between 1 and 3.
        """
        results = []

        # Number of fake users to attempt
        total_users = 3

        for i in range(1, total_users + 1):
            user_name = f"TestUser{i}"
            print(f"Starting {user_name}...")
            result = ZoomController.run_user(user_name)
            results.append(result)

        # Return HTML response
        return "<br>".join(results)