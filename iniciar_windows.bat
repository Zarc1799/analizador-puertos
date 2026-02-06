@echo off
TITLE Analizador de Puertos - Iniciando...
echo ===================================================
echo   ANALIZADOR DE PUERTOS - HACKER EDITION (FLASK)
echo ===================================================
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    pause
    exit /b
)

echo [2/3] Instalando dependencias Backend (Flask)...
pip install -r backend\requirements.txt >nul 2>&1
pip install flask-cors >nul 2>&1

echo [3/3] Iniciando Sistema...
echo ---------------------------------------------------
echo  La interfaz se abrira automaticamente en:
echo  http://localhost:8000
echo ---------------------------------------------------

start http://localhost:8000
python -m backend.app.main

pause
