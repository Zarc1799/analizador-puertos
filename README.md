```text
███████╗ █████╗ ██████╗  ██████╗ ██╗███████╗██████╗ ██████╗ 
╚══███╔╝██╔══██╗██╔══██╗██╔════╝███║╚════██║██╔══██╗██╔══██╗
  ███╔╝ ███████║██████╔╝██║     ╚██║    ██╔╝╚██████╔╝╚██████╔╝
 ███╔╝  ██╔══██║██╔══██╗██║      ██║   ██╔╝  ╚════██║ ╚════██║
███████╗██║  ██║██║  ██║╚██████╗ ██║   ██║    ██████║  ██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ 
                                             NET-ANALYZER
```
# ZARC1799 NET-ANALYZER 🛡️
![Version](https://img.shields.io/badge/version-1.0.0-green.svg) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg) ![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
> **Herramienta profesional de auditoría de red de despliegue local.**  
> Escaneo de puertos (Nmap), detección de vulnerabilidades y pruebas de estrés (Network Flood) en una interfaz Cyberpunk unificada.
---
## 🚀 Características Principales
*   **🕵️ Port Scanner Avanzado**: Integración nativa con `Nmap` para detectar servicios, versiones y sistemas operativos. Visualización limpia y estructurada.
*   **🌊 Network Flood & Stress Test**: Módulo de auditoría de carga (TCP/UDP) con hilos concurrentes para verificar la resiliencia de servicios. **Uso autorizado únicamente.**
*   **📊 Monitorización en Tiempo Real**: Gráficos y estadísticas en vivo de paquetes enviados y tasa de error.
*   **💻 Cross-Platform**: 
    *   **Linux**: Funcionalidad completa (Escaneo + Flood).
    *   **Windows**: Funcionalidad de Flood completa. Escaneo requiere instalación manual de Nmap/Npcap.
## 🛠️ Instalación y Uso
### Opción Rápida (Windows)
Simplemente ejecuta el script incluido:
```powershell
.\iniciar_windows.bat
```
El sistema montará el entorno y abrirá automáticamente tu navegador en `http://localhost:8000`.
### Instalación Manual (Linux/Mac)
1. **Requisitos**: Python 3.10+, Nmap (`sudo apt install nmap`).
2. **Backend**:
   ```bash
   pip install -r backend/requirements.txt
   pip install flask-cors
   ```
3. **Ejecutar**:
   ```bash
   python -m backend.app.main
   ```
## 🏗️ Arquitectura del Proyecto
El sistema utiliza una arquitectura **Monolítica Local** para máxima portabilidad:
*   **Frontend**: Construido con **Next.js** y **Tailwind CSS**. Compilado estáticamente (`next build`).
*   **Backend**: **Flask (Python)** sirve tanto la API REST como los archivos estáticos del frontend.
*   **Core**: 
    *   `python-nmap`: Wrapper para el motor de escaneo.
    *   `scapy`: Generación de paquetes para pruebas de carga.
## ⚠️ renuncia de responsabilidad (Disclaimer)
Esta herramienta ha sido creada con fines **educativos y de auditoría ética**. 
El autor (**Zarc1799**) no se hace responsable del mal uso de las capacidades de inundación o escaneo. Asegúrate de tener permiso explícito antes de auditar cualquier red.
---
*Developed by Zarc1799 - 2026*
