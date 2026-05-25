from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream"]
    )
    page = browser.new_page()
    page.goto("http://localhost:8000")

    # Unlock audio
    page.click("#overlay")
    page.wait_for_timeout(500)

    # Close panel
    page.evaluate("togglePanel(false)")
    page.wait_for_timeout(500)

    # Click Run
    page.click("#runBtn")
    page.wait_for_timeout(500)

    # Screenshot gyro mode
    page.screenshot(path="screenshot_gyro.png")

    # Switch to XY Pad mode
    page.click("#btn-xypad")
    page.wait_for_timeout(500)
    page.screenshot(path="screenshot_xypad.png")

    # Interact with XY pad
    page.locator("#xyPad").wait_for(state="visible")
    pad_box = page.locator("#xyPad").bounding_box()
    if pad_box:
        page.mouse.move(
            pad_box["x"] + pad_box["width"] / 3, pad_box["y"] + pad_box["height"] / 3
        )
        page.mouse.down()
        page.wait_for_timeout(200)
        page.mouse.move(
            pad_box["x"] + pad_box["width"] * 0.8,
            pad_box["y"] + pad_box["height"] * 0.8,
        )
        page.wait_for_timeout(200)
        page.mouse.up()
        page.screenshot(path="screenshot_xypad_interact.png")

    # Switch to 16 Pad mode
    page.click("#btn-16pad")
    page.wait_for_timeout(500)
    page.screenshot(path="screenshot_16pad.png")

    # Interact with 16 pad
    page.locator(".pad-grid").wait_for(state="visible")
    page.click(".pad-btn:nth-child(5)")  # Click a pad
    page.wait_for_timeout(200)
    page.screenshot(path="screenshot_16pad_interact.png")

    browser.close()
