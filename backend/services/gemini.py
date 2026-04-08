import asyncio
import base64
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_executor = ThreadPoolExecutor()

PARSE_PROMPT = """You are a document parser for a Singapore conveyancing law firm.
Analyze the uploaded document/image and extract structured data.

Singapore context:
- NRIC numbers: S/T/F/G followed by 7 digits and a letter (eg S1234567Z, T0123456A)
- FIN numbers start with F or G
- Singapore postcodes are exactly 6 digits
- OTP = Option to Purchase (real estate sale agreement between vendor and purchaser)
- AML = Anti-Money Laundering form
- LO = Letter of Offer (from bank for mortgage)
- Convert all extracted dates to YYYY-MM-DD format

First identify the document type from this exact list, then extract all visible fields.
Return ONLY valid JSON — no markdown, no code blocks, no extra text:

{
  "detected_type": "<one of: IC—Front | IC—Back | IC—Both Sides | Passport | OTP | WhatsApp Screenshot | AML | LO | ACRA | Others>",
  "fields": {
    "nameOnId": "<full legal name exactly as printed on the ID, or null>",
    "idNo": "<NRIC/IC/FIN/Passport number exactly as shown, or null>",
    "asianChars": "<Chinese or other Asian script name if present on ID, or null>",
    "dateOfBirth": "<YYYY-MM-DD format, or null>",
    "citizenship": "<nationality eg Singapore, Malaysia, China, India, or null>",
    "phone": "<phone number, include +65 if Singapore number, or null>",
    "email": "<email address in lowercase, or null>",
    "postcode": "<6-digit Singapore postal code, or null>",
    "floor": "<floor number only as integer string eg 12, or null>",
    "unit": "<unit number only eg 345, or null>",
    "block": "<block number or HDB block number, or null>",
    "street": "<street name without block/unit/floor, or null>",
    "buildingName": "<building name or estate/condo name, or null>",
    "propertyPrice": "<numeric only sale price in SGD eg 650000, or null>",
    "optionDate": "<YYYY-MM-DD option date, or null>",
    "optionExpiry": "<YYYY-MM-DD option expiry date, or null>",
    "completionDate": "<YYYY-MM-DD completion/completion date, or null>",
    "weeksUponExercising": "<integer number of weeks as string eg 10, or null>"
  }
}"""

VALID_TYPES = {
    "IC—Front", "IC—Back", "IC—Both Sides", "Passport",
    "OTP", "WhatsApp Screenshot", "AML", "LO", "ACRA", "Others"
}


def _sync_parse(file_bytes: bytes, mime_type: str) -> dict:
    model = genai.GenerativeModel("gemini-2.0-flash")
    encoded = base64.b64encode(file_bytes).decode("utf-8")

    response = model.generate_content([
        PARSE_PROMPT,
        {
            "inline_data": {
                "mime_type": mime_type,
                "data": encoded,
            }
        },
    ])

    text = response.text.strip()
    # Strip markdown code fences if Gemini adds them despite instructions
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    result = json.loads(text)

    # Normalise detected_type to known values
    if result.get("detected_type") not in VALID_TYPES:
        result["detected_type"] = "Others"

    return result


async def parse_document(file_bytes: bytes, mime_type: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _sync_parse, file_bytes, mime_type)
