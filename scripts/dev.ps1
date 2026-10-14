# Dev server for outreach-reply-classifier
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
