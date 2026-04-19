import asyncio
from playwright.async_api import async_playwright

# פשוט תוסיף כאן חברה ו-URL. זה יעבוד על הכל.
COMPANIES = {
    "Apple": "https://jobs.apple.com/en-il/search?location=israel-ISR&key=student",
    "Intel": "https://intel.wd1.myworkdayjobs.com/External/page/1ed62136c9271001e7edf16d5d680000",
}


async def get_generic_job_data(page, url):
    """מנוע גנרי ששולף את כל הקישורים והטקסטים הרלוונטיים מהדף"""
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)  # זמן טעינה לאלמנטים דינמיים

        # סקריפט JS שרץ בתוך הדפדפן ושולף את כל הלינקים שיש בהם טקסט
        job_elements = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links
                .map(link => ({
                    text: link.innerText.trim(),
                    href: link.href
                }))
                .filter(l => l.text.length > 5 && l.href.startsWith('http'));
        }''')

        # הופך את הרשימה לטקסט אחד ארוך שה-AI יבין בקלות
        formatted_text = ""
        for item in job_elements:
            formatted_text += f"Title: {item['text']} | URL: {item['href']}\n"

        return formatted_text
    except Exception as e:
        return f"Error scanning URL: {e}"


async def run_crawler():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36..."
        )
        page = await context.new_page()

        all_data = ""

        for name, url in COMPANIES.items():
            print(f"🚀 סורק את {name} (גנרי)...")
            data = await get_generic_job_data(page, url)
            all_data += f"\n--- COMPANY: {name} ---\n{data}\n"
            print(f"✅ {name} נסרקה.")

        with open("last_scan_result.txt", "w", encoding="utf-8") as f:
            f.write(all_data)

        await browser.close()
        print("\n✨ הסריקה הגנרית הסתיימה בהצלחה.")


if __name__ == "__main__":
    asyncio.run(run_crawler())