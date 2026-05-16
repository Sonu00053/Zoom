from playwright.sync_api import sync_playwright
import time


class ZoomController:
    # Zoom meeting URL
    meeting_url = "https://app.zoom.us/wc/join/87417457133?pwd=55k88c"

    # Har run me 50 naye users
    users = [f"ABC{i}" for i in range(1, 2)]

    @classmethod
    def join_user(cls, browser, user):
        print(f"Joining {user}...")

        # Har user ke liye alag browser context
        context = browser.new_context(
            permissions=[],  # camera/mic permissions deny
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()

        try:
            # Camera/mic API disable
            page.add_init_script("""
                Object.defineProperty(navigator, 'mediaDevices', {
                    value: {
                        getUserMedia: async () => {
                            throw new Error('Media disabled');
                        }
                    }
                });
            """)

            # Zoom web client open
            page.goto(
                cls.meeting_url,
                wait_until="domcontentloaded",
                timeout=45000
            )

            # Name input wait
            page.wait_for_selector('input[type="text"]', timeout=15000)

            # Participant name fill
            page.locator('input[type="text"]').first.fill(user)

            # Join button click
            page.locator(
                'button:has-text("Join"), '
                'button:has-text("Join Meeting")'
            ).first.click()

            print(f"{user}: Join submitted")

            # Secondary dialogs handle
            page.wait_for_timeout(3000)

            selectors = [
                'button:has-text("Got it")',
                'button:has-text("OK")',
                'button:has-text("Cancel")',
            ]

            for selector in selectors:
                try:
                    btn = page.locator(selector)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click()
                        page.wait_for_timeout(500)
                except Exception:
                    pass

            print(f"{user}: Joined successfully")
            return context  # Context open rakho

        except Exception as e:
            print(f"{user}: Failed -> {e}")
            context.close()
            return None

    @classmethod
    def start(cls):
        with sync_playwright() as p:
            # Headless mode => koi tab visible nahi
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

                # Thoda fast joining
                time.sleep(0.2)

            print(f"\n{len(contexts)} participants joined successfully.")
            print("Press Ctrl+C to stop and disconnect all users.")

            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nClosing browser...")
                browser.close()


if __name__ == "__main__":
    ZoomController.start()