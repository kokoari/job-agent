import asyncio
import os
# ייבוא פונקציית הסריקה מהקובץ crawler_test
from crawler_test import run_crawler
from ai_agent import analyze_jobs
from notifier import send_job_notification


async def run_agent():
    print("🎬 מתחיל תהליך אוטומטי מלא: סריקה -> ניתוח -> התראה")

    # שלב 1: הרצת הסורק (החלק האוטומטי החדש)
    # זה יריץ את כל החברות שהגדרת ב-COMPANIES ויעדכן את last_scan_result.txt
    try:
        await run_crawler()
    except Exception as e:
        print(f"❌ שגיאה במהלך הסריקה: {e}")
        return

    # שלב 2: קריאת הנתונים שנסרקו
    file_path = "last_scan_result.txt"
    if not os.path.exists(file_path):
        print(f"❌ שגיאה: הקובץ {file_path} לא נוצר.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        # קוראים עד 150,000 תווים כפי שמצאנו שצריך
        raw_text = f.read()[:150000]

    if not raw_text.strip():
        print("⚠️ הקובץ ריק. הסריקה כנראה נכשלה.")
        return

    print(f"🧠 מנתח {len(raw_text)} תווים בעזרת Gemini...")

    # שלב 3: ניתוח המשרות בעזרת ה-AI
    try:
        relevant_jobs = analyze_jobs(raw_text)

        if relevant_jobs:
            print(f"✅ נמצאו {len(relevant_jobs)} משרות סטודנט רלוונטיות!")
            # שלב 4: שליחה לטלגרם
            await send_job_notification(relevant_jobs)
            print("📬 ההודעה נשלחה בהצלחה.")
        else:
            print("🤷 לא נמצאו משרות חדשות שמתאימות להנדסת חשמל בסבב הזה.")

    except Exception as e:
        print(f"❌ שגיאה בניתוח ה-AI או בשליחה: {e}")


if __name__ == "__main__":
    asyncio.run(run_agent())