import os
import json
from dotenv import load_dotenv
from google import genai

# 1. טעינת המפתח
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_jobs(raw_text):
    model_id = 'gemini-2.5-flash'

    prompt = f"""
    You are an expert career consultant for Electrical Engineering (EE) and Hardware students in Israel.
    Your mission is to find ANY student position that a Hardware/EE student would be qualified for.

    ### WHAT TO INCLUDE (The "Gold" List):
    - Silicon/Chip/ASIC/FPGA (Design, Verification, Validation, Physical Design).
    - Board Design, Analog, Digital, RF, Signal Integrity (SI), Power.
    - Systems Engineering, Control Systems, Electro-Optics, Camera Systems.
    - Embedded Systems, Firmware, Hardware-oriented Python/C++.
    - Lab Tech, Hardware Student, Product Engineering.

    ### WHAT TO STICK TO (The "Trash" List):
    - Web Development (Frontend, Backend, React, Node, etc.).
    - Pure Software roles like App development, Java, Backend Cloud.
    - ONLY exclude if it is clearly 100% Software with no relation to Hardware/Physics/Electronics.

    ### OUTPUT RULES:
    - If a job title is "System Engineering" or "Verification" - ALWAYS include it.
    - Return a JSON list of objects. Link MUST be a valid URL.
    - If no relevant jobs, return [].

    RAW TEXT:
    ---
    {raw_text}
    ---
    """

    print(f"🤖 מנתח בעזרת {model_id}...")

    try:
        # כאן הורדתי את הסוגריים הכפולים לרגילים - זה התיקון!
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config={
                'response_mime_type': 'application/json'
            }
        )
        return json.loads(response.text)

    except Exception as e:
        if "429" in str(e):
            print("⏳ עומס על השרת (Quota), נסה שוב בעוד דקה.")
        else:
            print(f"❌ שגיאה: {e}")
        return []


if __name__ == "__main__":
    # בדיקת Mock Data
    mock_data = """
    Jobs at Intel Israel:
    1. Electrical Engineering Student for VLSI - Haifa. Apply at intel.com/job123
    2. Hardware Intern (Chips design) - Jerusalem. Apply at intel.com/intern456
    """
    relevant_jobs = analyze_jobs(mock_data)
    print("\n🎯 תוצאות:")
    print(json.dumps(relevant_jobs, indent=2, ensure_ascii=False))