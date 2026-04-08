import base64
import json
import os
import re
from io import BytesIO

import fitz  # pymupdf
from docx import Document as DocxDocument
from groq import Groq

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Llama 4 Scout — vision-capable, fast on Groq.
# Swap to "meta-llama/llama-4-maverick-17b-128e-instruct" if you get access.
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

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

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _pdf_to_image_bytes(file_bytes: bytes) -> bytes:
    """Convert the first page of a PDF to PNG bytes at 200 dpi."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    return pix.tobytes("png")


def _extract_docx_text(file_bytes: bytes) -> str:
    """Extract plain text from a DOCX file."""
    doc = DocxDocument(BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def _parse_response(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    result = json.loads(text.strip())
    if result.get("detected_type") not in VALID_TYPES:
        result["detected_type"] = "Others"
    return result


async def parse_document(file_bytes: bytes, mime_type: str) -> dict:
    # DOCX: extract text, send as text-only prompt (no vision needed)
    if mime_type == DOCX_MIME:
        text = _extract_docx_text(file_bytes)
        response = _client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": f"{PARSE_PROMPT}\n\nDocument text:\n{text}"}
            ],
        )
        return _parse_response(response.choices[0].message.content)

    # PDF: convert first page to image, then fall through to vision
    if mime_type == "application/pdf":
        file_bytes = _pdf_to_image_bytes(file_bytes)
        mime_type = "image/png"

    # Images: send directly to vision model
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{encoded}"

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PARSE_PROMPT},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
    )
    return _parse_response(response.choices[0].message.content)
