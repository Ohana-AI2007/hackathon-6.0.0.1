from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import orchestrator as orch

app = FastAPI(title="EduMind AI")


class Req(BaseModel):
    input: str


@app.post("/api/orchestrate")
def orchestrate(r: Req):
    agent = orch.route(r.input)
    return {"agent": agent, "url": orch.AGENTS[agent]}


@app.get("/api/agents/config")
def agents_config():
    return orch.AGENTS


@app.get("/api/agents/status")
async def agents_status():
    return await orch.status()


@app.get("/api/progress")
def progress():
    return {"overall": 70, "topics": {"Machine Learning": 85, "Python": 72, "DBMS": 58, "Operating Systems": 65}}


@app.get("/api/wellness/status")
def wellness():
    return {"water": 4, "breaks": 2, "eye_rest": 3}

@app.get("/open/{name}", response_class=HTMLResponse)
def open_agent(name: str):
    url = orch.AGENTS.get(name)
    if not url:
        raise HTTPException(404, "Agent is not configured")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>EduMind - {name.title()}</title>
<style>
html,body{{margin:0;height:100%}}
body{{display:flex;flex-direction:column;font-family:Arial,sans-serif}}
.bar{{display:flex;align-items:center;gap:14px;padding:10px 16px;background:#0a1030;color:#fff}}
.bar a{{padding:10px 20px;border-radius:12px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);
color:#fff;font-weight:700;text-decoration:none}}
iframe{{flex:1;border:0;width:100%}}
</style></head><body>
<div class="bar"><a href="/" onclick="window.close()">&larr; Back to EduMind</a><b>{name.title()} Agent</b></div>
<iframe src="{url}"></iframe></body></html>"""

# Hamesha sabse last mein
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)