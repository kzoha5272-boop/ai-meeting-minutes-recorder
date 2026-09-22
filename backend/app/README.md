# AI Meeting Minutes Recorder

An AI-powered application for recording, processing, and generating structured meeting minutes from audio recordings.

## Project Status

### Completed

- FastAPI backend initialized
- Audio upload endpoint implemented
- Audio file validation implemented
- SQLite database configured
- Meeting database model created
- Background processing mechanism implemented
- Meeting processing status tracking implemented
- Initial ASR experiments started in Google Colab

### Current Work

- ASR model evaluation
- Noisy and multi-speaker audio testing
- Speaker diarization
- Speaker-attributed transcription
- Meeting understanding
- Automated Minutes of Meeting generation

## Planned Pipeline

```text
Audio Recording
       |
       v
Audio Upload
       |
       v
Background Processing
       |
       v
Speech-to-Text (ASR)
       |
       v
Speaker Diarization
       |
       v
Speaker-Attributed Transcript
       |
       v
Meeting Understanding
       |
       v
Minutes of Meeting
       |
       v
Structured Results