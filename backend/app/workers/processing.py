import time

from app.db.database import SessionLocal
from app.db.models import Meeting


def process_meeting(meeting_id: str):
    db = SessionLocal()

    try:
        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id
        ).first()

        if not meeting:
            print(f"Meeting {meeting_id} not found.")
            return

        print(f"Starting processing for meeting: {meeting_id}")

        meeting.status = "processing"
        db.commit()

        # Temporary test processing.
        # Later this will contain:
        # 1. Audio preprocessing
        # 2. ASR
        # 3. Speaker diarization
        # 4. Transcript generation
        # 5. LLM meeting-minutes generation

        print(f"Processing meeting: {meeting_id}")

        time.sleep(10)

        meeting.status = "completed"
        db.commit()

        print(f"Meeting completed: {meeting_id}")

    except Exception as e:
        print(f"Error processing meeting {meeting_id}: {e}")

        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id
        ).first()

        if meeting:
            meeting.status = "failed"
            meeting.error_message = str(e)
            db.commit()

    finally:
        db.close()