from pathlib import Path
from uuid import uuid4

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db
from app.db.models import Meeting
from app.workers.processing import process_meeting


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AI Meeting Minutes Recorder",
    description="Backend API for recording, processing, and generating meeting minutes.",
    version="0.1.0",
)


# Folder where uploaded audio files are stored
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Allowed audio formats
ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/x-m4a",
    "audio/webm",
    "audio/ogg",
    "application/ogg",
}


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Meeting Minutes Recorder API is running",
        "status": "ok"
    }


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# Upload meeting audio
# ---------------------------------------------------------

@app.post("/meetings/upload")
async def upload_meeting_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check audio format
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type: {file.content_type}"
        )

    # Get file extension
    extension = Path(file.filename).suffix.lower()

    if not extension:
        extension = ".audio"

    # Generate unique meeting ID
    meeting_id = str(uuid4())

    # Generate unique filename
    saved_filename = f"{meeting_id}{extension}"
    saved_path = UPLOAD_DIR / saved_filename

    # Save uploaded audio
    with open(saved_path, "wb") as output_file:
        while chunk := await file.read(1024 * 1024):
            output_file.write(chunk)

    # Create meeting record in database
    meeting = Meeting(
        id=meeting_id,
        original_filename=file.filename,
        audio_path=str(saved_path),
        status="uploaded"
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    # Start background processing
    background_tasks.add_task(
        process_meeting,
        meeting_id
    )

    # Return immediately to the user
    return {
        "meeting_id": meeting.id,
        "original_filename": meeting.original_filename,
        "status": "processing",
        "message": "Meeting audio uploaded and processing started."
    }


# ---------------------------------------------------------
# Get meeting processing status
# ---------------------------------------------------------

@app.get("/meetings/{meeting_id}")
def get_meeting_status(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    # Meeting doesn't exist
    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    return {
        "meeting_id": meeting.id,
        "original_filename": meeting.original_filename,
        "status": meeting.status,
        "created_at": meeting.created_at,
        "error_message": meeting.error_message
    }