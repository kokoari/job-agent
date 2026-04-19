import asyncio
import os
import json
# ייבוא פונקציית הסריקה מהקובץ crawler_test
from crawler_test import run_crawler
from ai_agent import analyze_jobs
from notifier import send_job_notification

# שם הקובץ שבו נשמור את המשרות שכבר נשלחו
DB_FILE = "sent_jobs.json"


def load_sent_jobs():
    """טוען את רשימת הקישורים שכבר נשלחו מהקובץ"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"⚠️ שגיאה בקריאת קובץ הזיכרון: {e}")
            return set()
    return set()


def save_sent_jobs(sent_set):
    """שומר את רשימת הקישורים המעודכנת לקובץ"""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(list(sent_set), f, indent=4)
        print(f"💾 הזיכרון עודכן: {len(sent_set)} משרות שמורות במערכת.")
    except Exception as e:
        print(f"❌ שגיאה בשמירת קובץ הזיכרון: {e}")


async def run_agent():
    print("🎬 מתחיל תהליך אוטומטי מלא: סריקה -> ניתוח -> סינון כפילויות -> התראה")

    # שלב 1: הרצת הסורק
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
        raw_text = f.read()[:150000]

    if not raw_text.strip():
        print("⚠️ הקובץ ריק. הסריקה כנראה נכשלה.")
        return

    print(f"🧠 מנתח {len(raw_text)} תווים בעזרת Gemini...")

    # שלב 3: ניתוח המשרות בעזרת ה-AI
    try:
        all_relevant_jobs = analyze_jobs(raw_text)

        if not all_relevant_jobs:
            print("🤷 לא נמצאו משרות שמתאימות להנדסת חשמל בסבב הזה.")
            return

        # --- שלב החדש: סינון משרות שכבר נשלחו ---
        sent_jobs_pool = load_sent_jobs()
        new_jobs_to_send = []

        for job in all_relevant_jobs:
            # אנחנו בודקים אם הלינק כבר קיים ב"זיכרון" שלנו
            if job.get('link') not in sent_jobs_pool:
                new_jobs_to_send.append(job)
                sent_jobs_pool.add(job.get('link'))

        if new_jobs_to_send:
            print(f"🔥 נמצאו {len(new_jobs_to_send)} משרות חדשות באמת!")
            # שלב 4: שליחה לטלגרם (רק של החדשות)
            await send_job_notification(new_jobs_to_send)

            # שלב 5: שמירת המצב המעודכן כדי שלא יישלחו מחר שוב
            save_sent_jobs(sent_jobs_pool)
            print("📬 ההודעה נשלחה בהצלחה והזיכרון עודכן.")
        else:
            print("😴 כל המשרות שנמצאו כבר נשלחו בעבר. לא שולח הודעה כפולה.")

    except Exception as e:
        print(f"❌ שגיאה בניתוח ה-AI או בשליחה: {e}")


if __name__ == "__main__":
    asyncio.run(run_agent())