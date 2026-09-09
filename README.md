# ClipForge AI — Chromebook Web Version

This is the browser version of ClipForge. Your Chromebook only needs Chrome/browser access.

## Easiest setup
Deploy this folder to a server that supports Docker. The server installs Python and FFmpeg automatically from the Dockerfile.

## Important
This starter creates a vertical clip from the beginning of the uploaded video. It is the browser/server foundation for the full AI version.

For the full production AI pipeline, add:
- Faster-Whisper transcription
- AI highlight ranking
- multiple clips per VOD
- animated captions
- face/speaker tracking
- cloud storage
- background workers and job queue
- authentication and upload limits

Only process videos you have permission to use, and follow the platform's rules and copyright law.
