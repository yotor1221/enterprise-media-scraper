from playwright.async_api import async_playwright
import asyncio

async def scrape_social_profile(browser_context, url):
    page = await browser_context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Simple extraction for the demo
        data = {
            "url": url,
            "title": await page.title(),
            "status": "Success"
        }
        return data
    finally:
        await page.close()