from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Analizador de Puertos", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (Frontend)
# In production/monolithic mode, frontend export goes to app/static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/_next", StaticFiles(directory=os.path.join(static_dir, "_next")), name="next_assets")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_frontend():
    # Helper to serve the index.html from Next.js export
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "Backend Running", "message": "Frontend not found in static/ directory yet. Run 'npm run build' in frontend first."}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "system": "Analizador de Puertos v1.0"}

# --- Scanner Endpoints ---
from pydantic import BaseModel

class ScanRequest(BaseModel):
    target: str
    ports: str = "1-1000"
    arguments: str = "-sV"

@app.post("/api/scan")
async def run_scan(request: ScanRequest):
    from .scanners import scanner_instance
    return scanner_instance.scan_host(request.target, request.ports, request.arguments)

# --- Flood Endpoints ---
class FloodRequest(BaseModel):
    target: str
    port: int
    method: str = "TCP"
    threads: int = 10

@app.post("/api/flood/start")
def start_flood_endpoint(req: FloodRequest):
    from .flood import flood_instance
    if flood_instance._running:
        return {"error": "Flood already running"}
    flood_instance.start_flood(req.target, req.port, req.method, req.threads)
    return {"status": "Flood started", "target": req.target}

@app.post("/api/flood/stop")
def stop_flood_endpoint():
    from .flood import flood_instance
    flood_instance.stop_flood()
    return {"status": "Flood stopped"}

@app.get("/api/flood/stats")
def get_flood_stats():
    from .flood import flood_instance
    return flood_instance.get_stats()

# Placeholder for WebSocket (Real-time updates)
@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
