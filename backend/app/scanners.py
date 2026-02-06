import nmap
import platform
import asyncio
from typing import Dict, Any

class PortScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def scan_host(self, target: str, ports: str = "1-1000", arguments: str = "-sV") -> Dict[str, Any]:
        """
        Realiza un escaneo de puertos sobre el objetivo.
        """
        try:
            # Detectar SO para ajustes si es necesario
            system = platform.system()
            print(f"[*] Iniciando escaneo en {target} ({system})")
            
            self.nm.scan(hosts=target, ports=ports, arguments=arguments)
            
            result = {
                "host": target,
                "state": "unknown",
                "protocols": {}
            }
            
            if target in self.nm.all_hosts():
                result["state"] = self.nm[target].state()
                
                for proto in self.nm[target].all_protocols():
                    result["protocols"][proto] = {}
                    lport = self.nm[target][proto].keys()
                    for port in lport:
                        service = self.nm[target][proto][port]
                        result["protocols"][proto][port] = {
                            "state": service['state'],
                            "name": service['name'],
                            "product": service['product'],
                            "version": service['version'],
                            "cpe": service.get('cpe', '')
                        }
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def get_cve_for_service(self, product: str, version: str):
        # Placeholder para búsqueda de CVEs
        # En una implementación real, consultaría una base de datos local o API externa
        return []

scanner_instance = PortScanner()
