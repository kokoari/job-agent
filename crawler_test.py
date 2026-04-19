import asyncio
from playwright.async_api import async_playwright

COMPANIES = {
    "Apple": "https://jobs.apple.com/en-il/search?location=israel-ISR&key=student",
    "Intel": "https://intel.wd1.myworkdayjobs.com/External/page/1ed62136c9271001e7edf16d5d680000",
    "Elbit": "https://elbitsystemscareer.com/jobs/?category=%D7%A1%D7%98%D7%95%D7%93%D7%A0%D7%98%D7%99%D7%9D",
    "Refael": "https://career.rafael.co.il/search/f/T2/1/",
    "Amazon": "https://www.amazon.jobs/content/en/teams/amazon-web-services/annapurna-labs?country%5B%5D=IL&employment-type%5B%5D=Intern",
    "Qualcomm": "https://careers.qualcomm.com/careers?start=0&location=israel&sort_by=distance&filter_include_remote=0&filter_seniority=Intern",
    "Marvell": "https://marvell.wd1.myworkdayjobs.com/MarvellCareers?Country=084562884af243748dad7c84c304d89a",
    "google": "https://www.google.com/about/careers/applications/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=INFORMATION_TECHNOLOGY&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&category=USER_EXPERIENCE&employment_type=FULL_TIME&employment_type=PART_TIME&employment_type=TEMPORARY&jex=ENTRY_LEVEL&location=Israel",
    "Microsoft": "https://apply.careers.microsoft.com/careers?hl=en&start=0&location=Israel&pid=1970393556734780&sort_by=distance&filter_include_remote=1&filter_seniority=Intern",
    "KLA": "https://kla.wd1.myworkdayjobs.com/Search?Country=084562884af243748dad7c84c304d89a&jobFamilyGroup=bcb876733f86019037b304ff551bb91e",
    "Applied Materials": "https://careers.appliedmaterials.com/careers?domain=appliedmaterials.com&triggerGoButton=false&start=0&pid=790314788018&sort_by=relevance&filter_country=Israel&filter_seniority=Intern",

}


async def get_generic_job_data(page, url):

    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)

        job_elements = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links
                .map(link => ({
                    text: link.innerText.trim(),
                    href: link.href
                }))
                .filter(l => l.text.length > 5 && l.href.startsWith('http'));
        }''')

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
            print(f"🚀 סורק את {name} ...")
            data = await get_generic_job_data(page, url)
            all_data += f"\n--- COMPANY: {name} ---\n{data}\n"
            print(f"✅ {name} נסרקה.")

        with open("last_scan_result.txt", "w", encoding="utf-8") as f:
            f.write(all_data)

        await browser.close()
        print("\n✨ הסריקה הסתיימה בהצלחה.")


if __name__ == "__main__":
    asyncio.run(run_crawler())