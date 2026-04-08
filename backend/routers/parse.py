from fastapi import APIRouter, HTTPException, UploadFile, File

from services.gemini import parse_document

router = APIRouter()

_MIME_FALLBACKS = {
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".heic": "image/heic",
    ".heif": "image/heif",
}


@router.post("/parse-document")
async def parse_doc(file: UploadFile = File(...)):
    content = await file.read()

    mime_type = file.content_type or "application/octet-stream"
    if mime_type == "application/octet-stream" and file.filename:
        suffix = "." + file.filename.rsplit(".", 1)[-1].lower()
        mime_type = _MIME_FALLBACKS.get(suffix, mime_type)

    try:
        result = await parse_document(content, mime_type)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
