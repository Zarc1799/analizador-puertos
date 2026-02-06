"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000"; // Hardcoded for local usage simplicity

export default function Home() {
  const [activeTab, setActiveTab] = useState<"scan" | "flood">("scan");

  // Scanner State
  const [target, setTarget] = useState("127.0.0.1");
  const [ports, setPorts] = useState("8000"); // Default port
  const [scanResult, setScanResult] = useState<any>(null);
  const [scanning, setScanning] = useState(false);

  // Flood State
  const [floodTarget, setFloodTarget] = useState("127.0.0.1");
  const [floodPort, setFloodPort] = useState(80);
  const [floodThreads, setFloodThreads] = useState(10);
  const [flooding, setFlooding] = useState(false);
  const [floodStats, setFloodStats] = useState<any>(null);

  // --- Actions ---

  const handleScan = async () => {
    setScanning(true);
    setScanResult(null);
    try {
      const res = await fetch(`${API_BASE}/api/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target, ports, arguments: "-sV" }),
      });
      const data = await res.json();
      setScanResult(data);
    } catch (e) {
      console.error(e);
      setScanResult({ error: "Connection Failed" });
    }
    setScanning(false);
  };

  const toggleFlood = async () => {
    if (flooding) {
      await fetch(`${API_BASE}/api/flood/stop`, { method: "POST" });
      setFlooding(false);
    } else {
      await fetch(`${API_BASE}/api/flood/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: floodTarget, port: floodPort, threads: floodThreads }),
      });
      setFlooding(true);
    }
  };

  // Poll stats while flooding
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (flooding) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/api/flood/stats`);
          const data = await res.json();
          setFloodStats(data);
        } catch (e) { console.error(e) }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [flooding]);

  return (
    <main className="min-h-screen bg-black text-green-500 p-8 font-mono">
      <header className="mb-8 border-b border-green-700 pb-4">
        <h1 className="text-4xl font-bold glitch-effect">ZARC1799 NET-ANALYZER</h1>
        <p className="text-green-300 text-sm mt-2">SYSTEM STATUS: <span className="text-green-400">ONLINE</span></p>
      </header>

      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab("scan")}
          className={`px-6 py-2 border ${activeTab === "scan" ? "bg-green-900 border-green-400 text-white" : "border-green-800 hover:bg-green-900/50"}`}
        >
          [ PORT SCANNER ]
        </button>
        <button
          onClick={() => setActiveTab("flood")}
          className={`px-6 py-2 border ${activeTab === "flood" ? "bg-red-900 border-red-500 text-white" : "border-red-900/50 text-red-400 hover:bg-red-900/30"}`}
        >
          [ NETWORK FLOOD ]
        </button>
      </div>

      <div className="border border-green-800 bg-gray-900/50 p-6 min-h-[500px]">

        {activeTab === "scan" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs mb-1">TARGET HOST</label>
                <input
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  className="w-full bg-black border border-green-600 p-2 text-green-400 focus:outline-none focus:border-green-300"
                />
              </div>
              <div>
                <label className="block text-xs mb-1">PORTS (Range or List)</label>
                <input
                  value={ports}
                  onChange={(e) => setPorts(e.target.value)}
                  className="w-full bg-black border border-green-600 p-2 text-green-400 focus:outline-none focus:border-green-300"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={handleScan}
                  disabled={scanning}
                  className="w-full bg-green-700 hover:bg-green-600 text-black font-bold p-2 disabled:opacity-50"
                >
                  {scanning ? "SCANNING..." : "INIT_SCAN_SEQUENCE"}
                </button>
              </div>
            </div>

            <div className="mt-8 bg-black border border-green-900 p-4 h-96 overflow-auto">
              <pre className="text-xs">
                {scanResult ? JSON.stringify(scanResult, null, 2) : "> AWAITING INPUT commands..."}
              </pre>
            </div>
          </div>
        )}

        {activeTab === "flood" && (
          <div className="space-y-6 border-red-900">
            <div className="p-4 bg-red-900/10 border border-red-900 mb-4">
              <h3 className="text-red-500 font-bold mb-2">WARNING: AUTHORIZED USE ONLY</h3>
              <p className="text-red-400 text-xs">Generar tráfico masivo puede saturar redes. Úsalo solo en entornos controlados.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="col-span-2">
                <label className="block text-xs mb-1 text-red-400">TARGET HOST</label>
                <input
                  value={floodTarget}
                  onChange={(e) => setFloodTarget(e.target.value)}
                  className="w-full bg-black border border-red-600 p-2 text-red-500 focus:outline-none focus:border-red-400"
                />
              </div>
              <div>
                <label className="block text-xs mb-1 text-red-400">PORT</label>
                <input
                  type="number"
                  value={floodPort}
                  onChange={(e) => setFloodPort(parseInt(e.target.value))}
                  className="w-full bg-black border border-red-600 p-2 text-red-500 focus:outline-none focus:border-red-400"
                />
              </div>
              <div>
                <label className="block text-xs mb-1 text-red-400">THREADS</label>
                <input
                  type="number"
                  value={floodThreads}
                  onChange={(e) => setFloodThreads(parseInt(e.target.value))}
                  className="w-full bg-black border border-red-600 p-2 text-red-500 focus:outline-none focus:border-red-400"
                />
              </div>
            </div>

            <button
              onClick={toggleFlood}
              className={`w-full font-bold p-4 text-xl tracking-widest border-2 ${flooding ? "bg-red-600 border-red-400 text-black animate-pulse" : "bg-black border-red-700 text-red-600 hover:bg-red-900/20"}`}
            >
              {flooding ? "STOP FLOOD ATTACK" : "INIT_FLOOD_ATTACK"}
            </button>

            {flooding && floodStats && (
              <div className="grid grid-cols-2 gap-4 mt-8">
                <div className="bg-black border border-red-800 p-6 text-center">
                  <div className="text-4xl font-bold text-red-500">{floodStats.sent}</div>
                  <div className="text-xs text-red-300">PACKETS SENT</div>
                </div>
                <div className="bg-black border border-red-800 p-6 text-center">
                  <div className="text-4xl font-bold text-red-500">{floodStats.errors}</div>
                  <div className="text-xs text-red-300">ERRORS/DROPS</div>
                </div>
              </div>
            )}
          </div>
        )}

      </div>
    </main>
  );
}
