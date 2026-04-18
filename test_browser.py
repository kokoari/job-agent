import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig


async def main():
    # הגדרות מינימליות
    browser_cfg = BrowserConfig(headless=False, browser_type="firefox")

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        print("🌍 Trying to open Google...")
        # אנחנו פשוט מבקשים ממנו ללכת לגוגל ולחזור
        result = await crawler.arun(url="https://www.google.com")

        if result.success:
            print("✅ It works! The browser reached Google.")
        else:
            print(f"❌ Still failing: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())