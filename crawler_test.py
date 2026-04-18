import asyncio
from playwright.async_api import async_playwright

# כאן אתה מוסיף כמה חברות שבא לך
COMPANIES = {
    "Apple": "https://jobs.apple.com/en-il/search?location=israel-ISR&key=student",
    "Intel": "https://intel.wd1.myworkdayjobs.com/External/page/1ed62136c9271001e7edf16d5d680000",
    # דוגמה לעוד חברה שתוכל להוסיף בעתיד:
    # "NVIDIA": "https://nvidia.wd1.myworkdayjobs.com/NVIDIAExternalCareerSite?q=student&locationCountry=Israel"
}


async def run_crawler():
    async with async_playwright() as p:
        # headless=True כדי שזה ירוץ "שקוף" ברקע
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # ניסיון להפעיל Stealth כדי שלא יחסמו אותנו
        try:
            from playwright_stealth import stealth
            await stealth(page)
        except Exception:
            pass

        all_data = ""

        for name, url in COMPANIES.items():
            print(f"🚀 סורק את {name}...")
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)

                # גלילה אוטומטית - קריטי כדי לטעון משרות שמופיעות רק כשגוללים
                print(f"🖱️ גולל ב-{name} כדי לוודא שכל המשרות נטענו...")
                for _ in range(3):
                    await page.mouse.wheel(0, 2000)
                    await asyncio.sleep(2)

                # לוקחים רק את הטקסט הנקי - SNR גבוה ל-AI
                page_text = await page.locator("body").inner_text()

                all_data += f"\n--- COMPANY: {name} ---\n"
                all_data += page_text + "\n"
                print(f"✅ {name} נסרקה בהצלחה.")

            except Exception as e:
                print(f"❌ שגיאה בסריקת {name}: {e}")

        # שמירה לקובץ אחד מרוכז
        with open("last_scan_result.txt", "w", encoding="utf-8") as f:
            f.write(all_data)

        print(f"\n✨ סיימתי! כל המידע נשמר ב-last_scan_result.txt ({len(all_data)} תווים).")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run_crawler())