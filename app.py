from datetime import datetime, timezone
from typing import List
from fastapi.responses import HTMLResponse

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
          <p><code>/scores/ui</code> — view scores in a pretty format</p>
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

@app.get("/scores/ui", response_class=HTMLResponse)
def scores_ui():
    ordered = sorted(
        scores,
        key=lambda s: (s.level, s.coins, s.timestamp or datetime.min),
        reverse=True
    )

    rows = ""
    for i, s in enumerate(ordered, start=1):
        ts = s.timestamp.isoformat() if s.timestamp else "-"
        rows += f"""
          <tr>
            <td class="rank">#{i}</td>
            <td>{s.player}</td>
            <td>{s.level}</td>
            <td>{s.coins}</td>
            <td class="ts">{ts}</td>
          </tr>
        """

    return f"""
    <html>
      <head>
        <title>Kamal Platformer Leaderboard</title>
        <style>
          body {{
            margin: 0;
            background: radial-gradient(1200px circle at 10% 10%, #0b1220 0%, #020617 45%, #000 100%);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, Segoe UI, sans-serif;
            display: flex;
            justify-content: center;
            padding: 40px 16px;
          }}
          .wrap {{
            width: 100%;
            max-width: 900px;
          }}
          h1 {{
            font-size: 2.2rem;
            margin: 0 0 6px;
            letter-spacing: .5px;
          }}
          .sub {{
            color: #9ca3af;
            margin-bottom: 18px;
          }}
          .card {{
            background: rgba(3, 7, 18, 0.75);
            border: 1px solid #1f2937;
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            overflow: hidden;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
          }}
          thead th {{
            text-align: left;
            font-size: .9rem;
            color: #a3a3a3;
            background: rgba(17, 24, 39, 0.8);
            padding: 12px 14px;
          }}
          tbody td {{
            padding: 12px 14px;
            border-top: 1px solid #111827;
            font-size: 1rem;
          }}
          tbody tr:hover {{
            background: rgba(17, 24, 39, 0.55);
          }}
          .rank {{
            font-weight: 700;
            color: #38bdf8;
          }}
          .ts {{
            color: #a3a3a3;
            font-size: .9rem;
          }}
          .pill {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 999px;
            background: #111827;
            border: 1px solid #1f2937;
            font-size: .85rem;
            color: #cbd5e1;
          }}
          .footer {{
            margin-top: 10px;
            color: #6b7280;
            font-size: .85rem;
          }}
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1>🕹 Kamal’s Platformer Leaderboard</h1>
          <div class="sub">Live scores from your local game → AKS backend</div>

          <div class="card">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player</th>
                  <th>Level</th>
                  <th>Coins</th>
                  <th>Time (UTC)</th>
                </tr>
              </thead>
              <tbody>
                {rows if rows else '<tr><td colspan="5" style="padding:18px;color:#9ca3af;">No scores yet. Go beat a level 😄</td></tr>'}
              </tbody>
            </table>
          </div>

          <div class="footer">
            JSON still available at <span class="pill">/scores</span>
          </div>
        </div>
      </body>
    </html>
    """
