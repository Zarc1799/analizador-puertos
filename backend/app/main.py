import os
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .scanners import scanner_instance
from .flood import flood_instance

app = Flask(__name__, static_folder="static")
CORS(app) # Enable CORS for development

# Servir Frontend Estático
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    
    # Si existe el archivo, sírvelo
    if path != "" and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    
    # Si no, devuelve index.html (SPA routing)
    if os.path.exists(os.path.join(static_dir, "index.html")):
        return send_from_directory(static_dir, "index.html")
        
    return "<h1>Backend Running</h1><p>Frontend not built yet. Run 'npm run build' in frontend/</p>"

@app.route("/api/health")
def health_check():
    return jsonify({"status": "ok", "system": "Analizador de Puertos v1.0 (Flask)"})

# --- Scanner Endpoints ---
@app.route("/api/scan", methods=["POST"])
def run_scan():
    data = request.json
    target = data.get("target")
    ports = data.get("ports", "1-1000")
    arguments = data.get("arguments", "-sV")
    
    result = scanner_instance.scan_host(target, ports, arguments)
    return jsonify(result)

# --- Flood Endpoints ---
@app.route("/api/flood/start", methods=["POST"])
def start_flood_endpoint():
    data = request.json
    target = data.get("target")
    port = int(data.get("port", 80))
    threads = int(data.get("threads", 10))
    method = data.get("method", "TCP")
    
    if flood_instance._running:
        return jsonify({"error": "Flood already running"})
        
    flood_instance.start_flood(target, port, method, threads)
    return jsonify({"status": "Flood started", "target": target})

@app.route("/api/flood/stop", methods=["POST"])
def stop_flood_endpoint():
    flood_instance.stop_flood()
    return jsonify({"status": "Flood stopped"})

@app.route("/api/flood/stats", methods=["GET"])
def get_flood_stats():
    return jsonify(flood_instance.get_stats())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
