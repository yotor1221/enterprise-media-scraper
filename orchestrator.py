import asyncio
import pandas as pd
from tqdm.asyncio import tqdm
from proxy_handler import ProxyManager
from scraper_logic import scrape_social_profile
from playwright.async_api import async_playwright
from logger_config import setup_logger

# Professional Config
CONCURRENCY_LIMIT = 5 
logger = setup_logger()

async def worker(name, queue, context, results, pbar):
    while True:
        url = await queue.get()
        logger.info(f"Worker {name} started: {url}")
        
        try:
            # The actual scraping call
            result = await scrape_social_profile(context, url)
            if result:
                results.append(result)
            logger.info(f"Worker {name} success: {url}")
        except Exception as e:
            logger.error(f"Worker {name} FAILED on {url} | Error: {str(e)}")
        finally:
            queue.task_done()
            pbar.update(1) # Updates the visual progress bar

async def main():
    # 1. Setup Data Source
    # For Upwork Demo: 20 URLs to show movement
    # Use a site that doesn't block basic scrapers for your demo
    urls = [f"http://books.toscrape.com/catalogue/page-{i}.html" for i in range(1, 6)]
    
    queue = asyncio.Queue()
    for url in urls:
        queue.put_nowait(url)

    proxy_manager = ProxyManager()
    results = []

    # 2. Start Playwright
    async with async_playwright() as p:
        # Headless=False so you can record a video/screenshot for Upwork
        browser = await p.chromium.launch(
            headless=False, 
            proxy=proxy_manager.get_proxy_settings()
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        # 3. Create Workers & Progress Bar
        print(f"\n🚀 Launching {CONCURRENCY_LIMIT} Workers for 65k Scale Test...")
        
        with tqdm(total=len(urls), desc="Overall Progress", unit="url") as pbar:
            tasks = []
            for i in range(CONCURRENCY_LIMIT):
                task = asyncio.create_task(worker(f"W-{i}", queue, context, results, pbar))
                tasks.append(task)

            await queue.join()
            
            for task in tasks:
                task.cancel()
            
        await browser.close()
        
        # 4. Save and Display Results
        if results:
            df = pd.DataFrame(results)
            df.to_csv("scraped_data.csv", index=False)
            
            print("\n" + "="*50)
            print("✅ SCRAPING COMPLETE - SESSION SUMMARY")
            print("="*50)
            print(f"Total Profiles Scraped: {len(df)}")
            print("\n--- DATA PREVIEW (Top 5) ---")
            print(df.head(5).to_string())
            print("="*50)
        else:
            print("❌ No data was collected. Check scraper_errors.log")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping orchestrator...")