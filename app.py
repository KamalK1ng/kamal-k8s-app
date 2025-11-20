from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Kamal K8s Game Backend")


class Score(BaseModel):
    player: str
    level: int
    coins: int
    timestamp: datetime | None = None


# super simple in-memory storage (for demo)
scores: List[Score] = []


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>Kamal K8s Game Backend</title>
        <style>
          body {
            background-color: #020617;
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
          }
          .card {
            padding: 2rem 3rem;
            border-radius: 1rem;
            border: 1px solid #1f2937;
            box-shadow: 0 20px 40px rgba(0,0,0,0.45);
            text-align: center;
            max-width: 480px;
          }
          h1 { margin-bottom: 0.75rem; }
          p { margin-bottom: 0.5rem; }
          code { background: #111827; padding: 0.25rem 0.5rem; border-radius: 0.25rem; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>🕹 Kamal's Platformer Backend</h1>
          <p>This FastAPI app is running in AKS.</p>
          <p>Used by your local Python platformer to send scores.</p>
          <p>Interesting endpoints:</p>
          <p><code>/healthz</code> — health check</p>
          <p><code>/score</code> — POST scores from the game</p>
          <p><code>/scores</code> — view scores</p>
        </div>
      </body>
    </html>
    """


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}! This is running in Kubernetes."}


@app.post("/score")
def submit_score(score: Score):
    # stamp with server-side time if client didn't send one
    if score.timestamp is None:
        score.timestamp = datetime.now(timezone.utc)
    scores.append(score)
    return {"status": "saved", "count": len(scores)}


@app.get("/scores")
def list_scores():
    # newest first
    ordered = sorted(scores, key=lambda s: s.timestamp or datetime.min, reverse=True)
    return ordered
