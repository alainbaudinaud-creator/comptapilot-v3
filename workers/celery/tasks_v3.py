from datetime import datetime


def run_ocr_job(payload):
    return {
        "success": True,
        "job": "OCR",
        "payload": payload,
        "status": "READY",
        "timestamp": datetime.utcnow().isoformat(),
    }


def run_openai_job(payload):
    return {
        "success": True,
        "job": "OPENAI_ANALYSIS",
        "payload": payload,
        "status": "READY",
        "timestamp": datetime.utcnow().isoformat(),
    }


def run_pdf_job(payload):
    return {
        "success": True,
        "job": "PDF_EXPORT",
        "payload": payload,
        "status": "READY",
        "timestamp": datetime.utcnow().isoformat(),
    }

