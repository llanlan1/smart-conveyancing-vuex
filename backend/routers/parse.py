from fastapi import APIRouter, HTTPException, UploadFile, File

from services.groq_service import parse_document

router = APIRouter()

# Whitelist: extension → canonical MIME type
_ALLOWED = {
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif":  "image/gif",
    ".bmp":  "image/bmp",
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".tiff": "image/tiff",
    ".tif":  "image/tiff",
    ".pdf":  "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.post("/parse-document")
async def parse_doc(file: UploadFile = File(...)):
    filename = file.filename or ""
    ext = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""

    if ext not in _ALLOWED:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(_ALLOWED)}"
        )

    # Always derive MIME from extension — never trust the browser-supplied value
    mime_type = _ALLOWED[ext]
    content = await file.read()

    try:
        result = await parse_document(content, mime_type)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
