import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# טעינת המשתנים מה-env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# הגדרת הבוט - כאן אנחנו פותרים את הבעיה של "bot לא מוגדר"
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_job_notification(jobs):
    if not jobs:
        return

    # בונים הודעה אחת מרוכזת
    message = "🎯 **אריאל, מצאתי משרות סטודנט חדשות!**\n\n"

    for job in jobs:
        # שימוש ב-.get() מונע את שגיאת ה-'title' שראינו קודם
        title = job.get('title', 'משרה ללא כותרת')
        company = job.get('company', 'חברה לא ידועה')
        location = job.get('location', 'מיקום לא צוין')
        link = job.get('link', '#')

        message += f"🔹 **{title}** | {company}\n"
        message += f"📍 {location}\n"
        message += f"🔗 [הגשת מועמדות]({link})\n\n"
        message += "---\n"

    try:
        # שליחת ההודעה לטלגרם
        await bot.send_message(
            chat_id=MY_CHAT_ID,
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        print("📬 ההודעה נשלחה בהצלחה לטלגרם!")
    except Exception as e:
        print(f"❌ שגיאה בשליחת הודעה לטלגרם: {e}")